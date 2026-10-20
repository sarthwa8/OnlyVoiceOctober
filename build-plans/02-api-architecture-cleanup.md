# Build plan 02: API architecture cleanup (safety first, then structure)

> v1 · 2026-10-20 · Owner: **Pranav** · Reviewer: **Sarthak** (most moved code is his: `main.py`, `guide.py`, `webhook.py`, `bolna.py`, `llm.py`)
> Based on a full read of the code at shared-branch commit `a28dcf6` (+ the archive commit `d455541` on `pranav`). Line numbers below refer to that state.
> **Rule for the whole plan: behaviour doesn't change unless a step says so.** Every phase ends with all tests green and the same public routes (except the deliberate changes listed in §6).
> Related: [01 invite page](01-invite-page.md) · [CLAUDE.md](../CLAUDE.md) · [ChurnCall spec](../docs/CHURNCALL.md)

---

## 0. Why this plan exists

The code is small (about 1,100 lines of app code, 31 tests), readable and has no circular imports. It doesn't need a rewrite. But a full review found:

| # | Severity | Problem | Where |
|---|---|---|---|
| C1 | 🔴 **Critical, live** | `POST /calls` dials **any phone number** with **free-text prompt content**, with no invite and no key. The Next.js rewrite forwards all of `/api/*`, so it's public whenever ngrok runs. Wallet drain, harassment calls, prompt injection. | `apps/api/churncall/main.py:34-63`, `apps/web/next.config.ts` |
| C2 | 🔴 Critical | **A webhook can be lost without trace.** `_process()` calls `invites.record_call_outcome()` with nothing catching its errors, *before* saving the transcript. Any exception there (e.g. a missing company file in `load_company`) kills the background task. Bolna doesn't resend. | `main.py:77-84`, `invites.py:76-80, 199-215` |
| C3 | 🟠 High | FastAPI internals (`/docs`, `/openapi.json`, `/healthz`) are public through the same catch-all rewrite. The admin key travels in the URL (`?key=`), so it lands in ngrok and uvicorn access logs. | `next.config.ts`, `invites.py:353-358` |
| S1 | 🟠 Structural | `invites.py` (434 lines) does 8 jobs: models, JSONL storage, CSV validation, the event log, the funnel, building Bolna `user_data`, webhook outcomes, HTTP routes. The next features (results page, cancel-flow demo, Stripe trigger) each need pieces of it. | `invites.py` |
| S2 | 🟠 Structural | Two storage layers that disagree: `main.py` fixes `DATA_DIR` at import and creates it as a side effect; `invites.py` reads the env var on every call. Two `_append`s. Tests have to patch `main.DATA_DIR`. | `main.py:27-28, 41-43`, `invites.py:52-73`, `test_core.py:139`, `test_invites.py` (`api` fixture) |
| S3 | 🟡 Structural | Webhook knowledge is split: `context_details` is parsed in `main.py:87` *and* differently in `invites.py:190-196`; Bolna statuses live in `main.py:82` and `invites.py:35`; three different "only once" checks (`main.py:66-70` searches raw JSON text). | as listed |
| S4 | 🟡 Structural | Config read ad hoc in 7 places with separate defaults; `load_dotenv()` runs as an import side effect; a missing `BOLNA_API_KEY` only shows up as a 502 on a user's tap. | `bolna.py:16-18`, `llm.py:24-45`, `main.py:25-27,127`, `invites.py:54,355`, `agents/sync.py`, `scripts/make_invites.py` |
| S5 | 🟡 Structural | Modules find each other through the filesystem: `guide.py:15` uses `parents[3]`; the scripts, the eval and both test files edit `sys.path`. | as listed |
| M* | ⚪ Minor | Trigger lookup repeated 4× · stale `VERIFY` comments · untyped event dicts · `sync.py` does a `{x}`→`{{x}}` conversion that's no longer needed · `pytest` in runtime deps with open-ended `>=` versions · `InviteClient.tsx` mixes API, SDK lifecycle and UI | see Phase 4–5 |

**Not a problem (deliberately left alone):** performance. Each webhook reads two JSONL files in full about 4 times, which takes microseconds at kill-test scale; the Supabase move fixes it anyway. Extraction (Opus, up to 16k output tokens, in a FastAPI background thread) costs money, not speed. No optimisation work in this plan.

---

## 1. What "done" means (whole plan)

- [ ] No public route can place a call without a valid invite token (C1).
- [ ] Every Bolna webhook is saved raw **before** any processing, and a failure in one step can't skip the others (C2).
- [ ] Only `/api/invites/*` and `/api/bolna/webhook` are reachable through Next.js. Docs are off outside local. The admin key is a header (C3).
- [ ] One storage module, one config module, no import-time side effects (S2, S4).
- [ ] No module over ~200 lines doing more than one job. Routes contain no business logic (S1, S3).
- [ ] `pip install -e apps/api` works. No `sys.path` hacks anywhere (S5).
- [ ] Characterization tests (§7.1) pass unchanged from Phase 1 to the end, which proves business logic didn't move.
- [ ] `uvicorn churncall.main:app`, `scripts/make_invites.py`, `agents/sync.py` and `eval/interviews/simulate.py` all still work with the same commands (the paths inside them may change).

---

## 2. Target structure

```
apps/api/
  pyproject.toml            package "churncall": pinned runtime deps; [dev] extra = pytest. Replaces requirements.txt
  churncall/
    __init__.py
    config.py               Settings loaded ONCE from env (.env loaded here only). Validates required keys.
    store.py                The only code that touches JSONL: append / read / has / read_json, data dir, write lock.
                            Supabase later = rewrite this file only.
    bolna.py                Everything that knows Bolna's API shapes: BolnaClient (call, web session, agent upsert),
                            parse_webhook + CallRecord/Turn (from webhook.py), call_variables(), status constants,
                            WEBHOOK_IPS.
    interview.py            Renamed from guide.py: Company, Contact, trigger_phrases(), opening_line(),
                            prompt_variables(), render_prompt().
    invites.py              Invite domain only: Invite model, create_invite() + validation, load_company(),
                            typed event log, status, start limits.
    calls.py                start_phone_call() / start_web_call(): build user_data → Bolna → log start event.
    webhooks.py             handle_bolna_webhook(): save raw → update funnel → store transcript → extract.
    funnel.py               funnel() analytics (the results page will reuse it).
    extraction.py           unchanged except imports
    llm.py                  unchanged except reading settings from config
    errors.py               Small domain exceptions (InviteNotFound, InviteFinished, TooManyAttempts,
                            ConsentRequired, InvalidPhone, BolnaUnavailable).
    api/
      __init__.py           create_app(): mounts routers, maps domain errors to HTTP, docs only when local
      public.py             GET /invites/{token}, POST /event, /optout, /web-session, /call
      admin.py              GET /admin/funnel, protected by an X-Admin-Key header dependency
      bolna_webhook.py      POST /bolna/webhook + auth (secret header or Bolna IPs)
    main.py                 app = create_app()     ← `uvicorn churncall.main:app` keeps working
  tests/
    conftest.py             shared fixtures: temp data dir + settings, FakeBolna, company file, client
    test_interview.py · test_invites.py · test_calls.py · test_webhooks.py · test_funnel.py
    test_bolna.py · test_extraction.py · test_llm.py · test_api.py
    test_characterization.py  snapshots that must never change during the refactor (§7.1)
    fixtures/               bolna_completed.json once captured
scripts/make_invites.py     imports the installed package
agents/sync.py              uses BolnaClient.upsert_agent()
eval/interviews/simulate.py imports the installed package
apps/web/
  app/i/[token]/page.tsx · InviteClient.tsx (UI only)
  lib/api.ts                fetch helpers + PublicInvite type
  lib/useWebCall.ts         Web Call SDK lifecycle hook
  next.config.ts            rewrites only /api/invites/* and /api/bolna/webhook
```

### Dependency flow (strictly downward)

```
 api/*  (HTTP: parse request, call one use case, map errors → status codes)
   │
   ▼
 calls · webhooks · funnel · invites          (use cases: the business rules)
   │
   ▼
 interview · extraction                       (domain logic, no I/O except through adapters)
   │
   ▼
 store · bolna · llm                          (adapters: files, Bolna HTTP, LLM HTTP)
   │
   ▼
 config · errors
```
- Routes never touch files, env vars or Bolna directly.
- Adapters never import use cases.
- `bolna.py` imports nothing from the app except `config`.

### Key design decisions

| Decision | Why | What we're not doing |
|---|---|---|
| Plain modules and functions | 1,100 lines, one store, one voice provider. Classes and interfaces would be ceremony. | No repository classes, DI container, ORM or "services" layer framework |
| `store.py` is the only file-I/O seam | The Supabase swap after a "go" touches one file. Tests point it at a temp dir through config. | No abstract `Storage` interface designed ahead of time |
| `bolna.py` holds all of Bolna's shapes | We still don't know where Bolna echoes `user_data` or whether payloads change; one place to fix. | No generic "voice provider" abstraction |
| Domain exceptions + one HTTP mapping | Use cases stay usable from scripts, the Stripe trigger and the demo without HTTP. Status codes are defined in one place. | No custom error middleware beyond one exception handler |
| `config.py` on stdlib + pydantic (already installed) | One place for defaults and validation | No `pydantic-settings` or other new dependency |
| Routes keep their paths, except the admin route | Web app and Bolna webhook URL don't change | — |

---

## 3. Where every current piece goes

| Today | Goes to | Change |
|---|---|---|
| `main.py` `load_dotenv()`, `DATA_DIR` (25-28) | `config.py`, `store.py` | Loaded once in `get_settings()`; no import-time `mkdir` |
| `main.py` `CallMeRequest`, `call_me_now` `/calls` (34-63) | **deleted** (Phase 0) | Replaced by `/invites/{t}/call` |
| `main.py` `_append` (41) · `invites.py` `_data_dir`/`_read`/`_append`/`_now` (52-73) | `store.append/read/has/read_json`, `store.now()` | One implementation with a lock |
| `main.py` `_already_extracted` (66-70) | `store.has("insights.jsonl", execution_id=…)` | Parses JSON instead of a substring match |
| `main.py` `BOLNA_WEBHOOK_IPS` (74) | `bolna.WEBHOOK_IPS` | — |
| `main.py` `_process` (77-101) | `webhooks.handle_bolna_webhook` | + saves raw first, + each step's errors caught and logged (Phase 0) |
| `main.py` `_source_ip`, `bolna_webhook` route (104-135) | `api/bolna_webhook.py` | Same auth rules |
| `main.py` `healthz` (46) | `api/__init__.py` | + reports config readiness (`bolna_configured: true/false`), no secrets |
| `webhook.py` (all) | `bolna.py` (`Turn`, `CallRecord`, `parse_webhook`) | `parse_bolna_webhook` → `parse_webhook` |
| `invites.py` `_call_variables` (190-196) · `main.py:87` | `bolna.call_variables(payload)` | One parser used by both funnel and extraction |
| `invites.py` `NOT_CONNECTED` (35) · `"completed"` in `main.py:82` | `bolna.COMPLETED`, `bolna.NOT_CONNECTED` | — |
| `guide.py` (all) | `interview.py` | + `trigger_phrases()`; `PROMPT_PATH` from config |
| `invites.py` `Invite`, `EMAIL_RE`, `PHONE_RE`, `load_company`, `create_invite`, `all_invites`, `get_invite` | `invites.py` (stays) | Uses `store` |
| `invites.py` event log: `log_event`, `events_by_token`, `events_for`, `status_of`, `starts_count`, `token_for_execution`, `_channel_for`, `mark_completed`, `_log_once` (126-221) | `invites.py` (stays) | Typed `Event`; one `log_event_once()`; `ensure_can_start()` raises domain errors (from `_require_startable`) |
| `invites.py` `record_call_outcome`, `MIN_USER_TURNS` (33, 199-215) | `webhooks.py` | — |
| `invites.py` `build_user_data` (224-235) | `calls.py` | — |
| `invites.py` bodies of `post_web_session`, `post_call` (393-434) | `calls.start_web_call`, `calls.start_phone_call` | Raise `InviteFinished` / `TooManyAttempts` / `ConsentRequired` / `InvalidPhone` / `BolnaUnavailable(status)` |
| `invites.py` `STAGES`, `_stages_reached`, `_summarise`, `funnel` (240-298) | `funnel.py` | — |
| `invites.py` `_mask_phone`, `PublicInvite`, `CallIn`, `EventIn`, routes (306-434) | `api/public.py`, `api/admin.py` | Thin: parse → call → return |
| `llm.py` env reads (`provider`, `model_for`, `_chat_openai_compat`) | `llm.py` reading `config` | Same behaviour |
| `agents/sync.py` raw `httpx` PUT/POST (69-101) | `BolnaClient.upsert_agent()` | Same requests |
| `agents/sync.py` `to_bolna_placeholders` (31) | removed | `prompt.md` already uses `{{x}}`; a test asserts no single-brace placeholders remain |

---

## 4. Coordination with Sarthak (read before starting)

- Phases 1–2 move most of Sarthak's files. **Ask him to push his pending API work first, then avoid editing `apps/api/` during the window** (about 3–4 hours), or the merges will hurt.
- **One PR per phase** into `claude/bold-allen-oicfqq`, each small enough to review in 10 minutes. Phase 0 can merge right away (security). Phases 1–4 get his review.
- After Phase 2, tell him the new homes of his code: `guide.py`→`interview.py`; `webhook.py`→`bolna.py`; `_process`→`webhooks.py`.

---

## 5. Phases

Each phase lists **what to build**, **how it works**, **how to check it**, and **exit criteria**. Don't start a phase until the previous one is merged and green.

### Phase 0: Safety (≈1 h) · fixes C1, C2, C3 · merge immediately

**Build**
1. **Delete `POST /calls`** (`main.py:34-63`, plus the `prompt_variables`/`render_prompt`/`BolnaClient` imports only it used). Update `apps/api/README.md`'s route list. Sarthak's test `test_guardrails_bypass_sent_on_user_requested_calls` (`test_core.py:150`) targets `BolnaClient` directly, so it keeps passing; any test that posts to `/calls` is rewritten against `/invites/{t}/call`.
2. **Narrow the Next.js rewrite** in `apps/web/next.config.ts`:
   ```ts
   async rewrites() {
     const api = process.env.API_URL ?? "http://localhost:8000";
     return [
       { source: "/api/invites/:path*", destination: `${api}/invites/:path*` },
       { source: "/api/bolna/webhook", destination: `${api}/bolna/webhook` },
     ];
   },
   ```
   The web app only calls `/api/invites/*` today (`InviteClient.tsx` `post()`), and Bolna only calls the webhook.
3. **Docs off by default:** `FastAPI(docs_url=None, redoc_url=None, openapi_url=None)` unless `CHURNCALL_ENV=local`. Add `CHURNCALL_ENV=local` to `.env.example` with a comment.
4. **Admin key as a header:** `GET /invites/funnel` reads `X-Admin-Key` instead of `?key=`. It keeps its path for now and moves to `/admin/funnel` in Phase 2. Update 01's checklist command to `curl -H "X-Admin-Key: …"`.
5. **Webhook can't lose data** (`main.py` `_process`):
   ```python
   def _process(payload: dict) -> None:
       _append("webhooks.jsonl", {"at": _now(), "payload": payload})      # 1. raw first, always
       record = parse_bolna_webhook(payload)
       _step("funnel", record, lambda: invites.record_call_outcome(payload, record))   # 2. can't block 3-4
       if record.status.lower() != "completed" or _already_extracted(record.execution_id):
           return
       _append("transcripts.jsonl", record.model_dump(exclude={"raw"}))   # 3.
       ...extraction as today, already guarded...                         # 4.

   def _step(name, record, fn):
       try:
           fn()
       except Exception as exc:  # one failing step must never lose the call
           _append("errors.jsonl", {"at": _now(), "step": name, "execution_id": record.execution_id, "error": repr(exc)})
   ```
   Bonus: the first real payload in `webhooks.jsonl` becomes `tests/fixtures/bolna_completed.json` (Sarthak's handoff item 4).

**How to check**
- New tests: `POST /calls` → 404 (or 405); webhook where `record_call_outcome` raises → `webhooks.jsonl`, `transcripts.jsonl` and an `errors.jsonl` entry with `step: "funnel"` all exist; funnel with `?key=` → 401, with header → 200; app built with `CHURNCALL_ENV` unset → `/docs` 404.
- Manual: `next dev` + uvicorn → `curl localhost:3000/api/docs` → 404; `curl localhost:3000/api/calls` → 404; `curl localhost:3000/api/invites/<token>` → 200.

**Exit:** all tests green · the route list (§7.2) differs only by `-/calls` · 01's checklist updated.

---

### Phase 1: Config + store (≈1.5 h) · fixes S2, S4

**Build**
1. `churncall/config.py`:
   ```python
   class Settings(BaseModel):
       env: Literal["local", "production"] = "local"
       data_dir: Path = Path("data")
       public_base_url: str = "http://localhost:3000"
       admin_key: str = ""
       webhook_secret: str = ""
       bolna_api_key: str = ""
       bolna_agent_id: str = ""
       bolna_api_base: str = "https://api.bolna.ai"
       llm_provider: str = "anthropic"; llm_base_url: str = ""; llm_api_key: str = ""
       llm_model: str = ""; llm_model_cheap: str = ""
       prompt_path: Path = <repo>/agents/interviewer/prompt.md

   @lru_cache
   def get_settings() -> Settings:   # loads .env once (repo root), then os.environ
       ...
   def missing_for_calls(s) -> list[str]:  # e.g. ["BOLNA_API_KEY"], used by /healthz and at startup (log a warning)
   ```
   Tests call `get_settings.cache_clear()` from a `conftest` fixture after setting env vars.
2. `churncall/store.py`: `append(name, row)`, `read(name) -> list[dict]`, `has(name, **match) -> bool`, `read_json(relpath)`, `now()`, and a module-level `threading.Lock` held during "check then write" (used by `mark_completed`, `log_event_once`, the extraction dedupe). Data dir from `get_settings().data_dir`, created on first write, not at import.
3. Switch `main.py`, `invites.py`, `bolna.py`, `llm.py` and `scripts/make_invites.py` to `get_settings()` and `store`. Delete `main.DATA_DIR`, both `_append`s, `_data_dir`, and the import-time `load_dotenv()`.
4. `_already_extracted` → `store.has("insights.jsonl", execution_id=execution_id)`.

**How to check**
- Remove the `monkeypatch.setattr(main, "DATA_DIR", …)` workarounds (`test_core.py:139`, the `api` fixture). The tests must pass **without** them; that's the proof S2 is gone.
- Characterization tests (§7.1) pass unchanged.
- New: a concurrency test that runs 20 threads × `mark_completed(same token)` → exactly one `completed` event.

**Exit:** green · `grep -rn "os.environ" apps/api/churncall` finds only `config.py` · `grep -rn "\.open(\"a\")" apps/api/churncall` finds only `store.py`.

---

### Phase 2: Split modules + app factory (≈2 h) · fixes S1, S3

**Build** (code moves per §3; logic edits only where noted)
1. `errors.py` with the six domain exceptions.
2. `bolna.py` gains `Turn`, `CallRecord`, `parse_webhook` (moved from `webhook.py`, which is deleted), `call_variables()`, `COMPLETED`, `NOT_CONNECTED`, `WEBHOOK_IPS`.
3. `interview.py` = `guide.py` renamed, plus `trigger_phrases(trigger) -> tuple[str, str]` replacing the 4 repeated lookups (`guide.py:52,70,83`, `invites.py:369`).
4. `funnel.py`, `calls.py`, `webhooks.py` per §3. `calls.start_*` raise domain errors instead of `HTTPException`.
5. `api/public.py`, `api/admin.py` (`/admin/funnel` with an `X-Admin-Key` dependency), `api/bolna_webhook.py`; `api/__init__.create_app()` mounts them and registers **one** exception handler:
   ```python
   STATUS = {InviteNotFound: 404, InviteFinished: 409, TooManyAttempts: 429,
             ConsentRequired: 400, InvalidPhone: 422}
   # BolnaUnavailable → its upstream status for the web session (e.g. 429 at capacity), 502 for phone
   ```
   This preserves today's exact status codes (01 §4), which the web app depends on (`stateForCallResponse` in `InviteClient.tsx`).
6. `main.py` → `from .api import create_app; app = create_app()`.
7. `invites.py:409` becomes `run_id = session.get("run_id")`. The SDK 3.0.1 `Session` type defines `run_id`.

**How to check**
- Route list (§7.2): identical to Phase 0 except `/invites/funnel` → `/admin/funnel`.
- Characterization tests unchanged; existing tests updated **only in imports and monkeypatch targets** (plus the funnel URL). Example: `test_invite_user_data_uses_channel_specific_opener` (`test_core.py:167`) patches `invites.load_company`; after the move it patches the name `calls.py` looks up.
- `wc -l apps/api/churncall/*.py apps/api/churncall/api/*.py`: no file over ~200 lines.
- Manual smoke (§7.3).

**Exit:** green · `rg "from fastapi" apps/api/churncall --glob '!api/*'` finds nothing (no HTTP outside `api/`) · Sarthak told where his code went.

---

### Phase 3: Packaging (≈1 h) · fixes S5

**Build**
1. `apps/api/pyproject.toml` (setuptools, package `churncall`), with dependencies **pinned to the versions in the current `.venv`** (`pip freeze` filtered to direct deps) and `[project.optional-dependencies] dev = ["pytest==…"]`. Delete `requirements.txt`; update `apps/api/README.md`: `pip install -e "apps/api[dev]"`.
2. Remove the `sys.path.insert` lines from `scripts/make_invites.py`, `eval/interviews/simulate.py` and all tests.
3. `tests/conftest.py`: shared `data_dir` (temp + settings reset), `company`, `fake_bolna`, `client` fixtures; delete the copies in the test files.
4. `interview.PROMPT_PATH` comes from `get_settings().prompt_path` (default computed once in `config.py`).

**How to check**
- Fresh venv in a temp dir: `pip install -e "apps/api[dev]" && pytest -q apps/api/tests` → green.
- `python scripts/make_invites.py --help`, `python agents/sync.py --dry-run`, `python eval/interviews/simulate.py --help` all run.

**Exit:** green from a fresh venv · `rg "sys.path" -g '*.py'` → nothing.

---

### Phase 4: Types + dedupe (≈1 h) · minor items

**Build**
1. Typed events in `invites.py`:
   ```python
   EventName = Literal["opened", "web_connected", "mic_denied", "call_ended_client", "started_web",
                       "started_phone", "completed", "call_too_short", "call_not_connected", "opted_out"]
   class Event(BaseModel):
       token: str; event: EventName; at: str; meta: dict[str, Any] = {}
   ```
   `log_event()` validates the name, so a typo fails a test instead of silently skewing the funnel. The JSONL format on disk is unchanged.
2. One `log_event_once(token, event, *, key: str | None = None, meta)` replaces the three idempotency patterns (`post_event` "opened" dedupe, `_log_once`, `mark_completed`'s check).
3. `bolna.py`: remove the stale `VERIFY` comments for `/call` fields (confirmed against Bolna's call API docs on 2026-10-20). Keep `[verify]` only where it's still true: the location of `user_data` in the webhook.
4. `BolnaClient.upsert_agent(payload, agent_id=None)`; `agents/sync.py` uses it; delete `to_bolna_placeholders`. **Keep** the "Opening (already spoken)" rewrite: Bolna speaks `{{opening_line}}` as the welcome message, while `simulate.py` needs the agent to say it as its first turn, so the two prompts must differ there. Document this in `sync.py`'s docstring.

**How to check:** green · a test sends an unknown event name to `log_event` → raises · `sync.py --dry-run` output is byte-identical to before (save it before the phase and `diff` after).

**Exit:** green · dry-run diff empty.

---

### Phase 5: Web (≈0.5 h) · do it together with the results page

**Build:** `apps/web/lib/api.ts` (`postInvite(path, body)`, `getInvite(token)`, the `PublicInvite` type) and `apps/web/lib/useWebCall.ts` (SDK lifecycle: load, events, `start`, `stop`, returns `{state, start, stop}`). `InviteClient.tsx` becomes UI only.

**How to check:** `npm run lint` · `npx tsc --noEmit` · `npm run build` · browser smoke (§7.3 steps 1–3).

**Exit:** same UI behaviour; `InviteClient.tsx` under ~120 lines.

---

### After a "go" (not in this plan, listed so the structure is ready for it)
- Supabase: rewrite `store.py` (and add migrations); nothing else should need to change.
- Stdlib `logging` with a request/execution id on every line.
- Extraction moved from FastAPI `BackgroundTasks` to a job queue (spec §5.1: Postgres-backed).
- Stripe webhook route in `api/`, calling `invites.create_invite()`.

---

## 6. Deliberate interface changes (everything else stays identical)

| Change | Phase | Who's affected | Why |
|---|---|---|---|
| `POST /calls` removed | 0 | Nobody (the invite flow replaced it) | C1 |
| Only `/api/invites/*` and `/api/bolna/webhook` forwarded by Next.js | 0 | Nobody (the only callers) | C3 |
| Docs/OpenAPI off unless `CHURNCALL_ENV=local` | 0 | Us when debugging (set the env var) | C3 |
| Funnel: `?key=` → `X-Admin-Key` header; `/invites/funnel` → `/admin/funnel` | 0 / 2 | Us (curl), the future results page | C3; admin routes in one place |
| `requirements.txt` → `pyproject.toml` | 3 | Setup command in the README | S5 |

---

## 7. Testing and validation plan

### 7.1 Characterization tests (write them first, in Phase 0; they must pass unchanged through Phase 4)
`tests/test_characterization.py`:
1. **`build_user_data` snapshot:** a fixed invite (`ASHA` fixture, company `acme`, CSV incentive) for `channel="phone"` and `"web"` → compare the exact dict to a stored JSON snapshot (`tests/snapshots/user_data_{phone,web}.json`).
2. **Funnel snapshot:** a fixed `invites.jsonl` + `invite_events.jsonl` covering every event type → the `funnel()` output equals `tests/snapshots/funnel.json`.
3. **Webhook replay:** feed `queued → ringing → in-progress → call-disconnected → completed → completed` for one invite, plus `no-answer` and a 1-turn `completed` for two others → assert the exact sequence of events and which files got which rows.
4. **Route contract:** for each public route, the status code for the main cases (01 §4 table) via `TestClient`.

A snapshot only changes in a phase that says so in §6. Any other diff is a regression.

### 7.2 Route list check (every phase)
```bash
python -c "from churncall.main import app; print('\n'.join(sorted(app.openapi()['paths'])))"
```
(with `CHURNCALL_ENV=local`). Compare to the previous phase's output; only §6 changes are allowed.

### 7.3 Manual smoke (5 min per phase, no real call, no cost)
1. `make_invites.py` with a 1-row CSV → open `localhost:3000/i/<token>` → page renders; `opened` is logged once.
2. `curl -X POST localhost:3000/api/invites/<token>/web-session` → 200 with `run_id` (mints a session; no call is placed); `started_web` is logged.
3. `curl -X POST localhost:3000/api/invites/<token>/call -d '{"consent":false}' -H 'Content-Type: application/json'` → 400.
4. POST a stored completed-webhook JSON to `localhost:3000/api/bolna/webhook` with `X-Webhook-Secret` → the funnel shows `completed`.
5. `curl localhost:3000/api/docs` and `/api/calls` → 404.

### 7.4 Always
- `.venv/bin/python -m pytest -q apps/api/tests` (31 tests today, more as phases add them).
- `apps/web`: `npm run lint && npx tsc --noEmit && npm run build`.
- Once Bolna sends a real webhook: save it as `tests/fixtures/bolna_completed.json` and add a test through `handle_bolna_webhook`. That turns our guess about where `user_data` lives into a test that fails if Bolna changes it.

---

## 8. Risks

| Risk | Mitigation |
|---|---|
| Merge conflicts with Sarthak's work | §4: he pushes first and pauses `apps/api/` edits; one small PR per phase |
| A move silently changes behaviour | Characterization snapshots + route list diff every phase |
| The admin route move breaks someone's curl | Only the two of us use it; change noted in 01 and the README |
| Phase 3 pins break a fresh install | Pins come from the working `.venv`; verified in a fresh venv |
| Running out of time before Oct 30 | Phases are independent after 0–1. Phase 0 is mandatory; stop after Phase 2 if needed, since 3–5 are polish |

---

## 9. Time

| Phase | Time | Must do before real invites? |
|---|---|---|
| 0 Safety | 1 h | **Yes** |
| 1 Config + store | 1.5 h | Strongly recommended (the lock prevents double counts) |
| 2 Split + app factory | 2 h | Before building the results page / demo |
| 3 Packaging | 1 h | No |
| 4 Types + dedupe | 1 h | No |
| 5 Web | 0.5 h | With the results page |
| **Total** | **≈7 h** | |

## 10. Not in this plan
New features (results page, cancel-flow demo, Stripe, Slack/Linear) · Supabase · performance work · new frameworks or dependencies · UI styling · changes to the interview prompt or extraction logic.
