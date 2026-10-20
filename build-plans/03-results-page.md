# Build plan 03: Results page (funnel, reasons, every call)

> v1 · 2026-10-20 · Owner: **Pranav** · Builds on [01 invite page](01-invite-page.md) and the layered API from [02 architecture cleanup](02-api-architecture-cleanup.md) (this plan also finishes 02's Phase 5).
> Goal: one private page where we see **whether churned users talk** (funnel), **why they left** (reasons, verified quotes) and **each conversation** (transcript, insight, recording). That's what we look at for the go/no-go, and what we show pilot founders.
> **Still minimal styling:** readable tables and a tiny bit of inline CSS. The real dashboard design (themes × MRR, charts) comes after a "go" (spec [§3.6](../docs/CHURNCALL.md)).

## Progress (2026-10-20)
| Step | Status | Verified by |
|---|---|---|
| 1 Web helpers (02 Phase 5) | ✅ | `lib/api.ts`, `lib/useWebCall.ts`; `InviteClient.tsx` 116 lines, UI only; lint/tsc/build; invite page in the browser: renders, consent gating, `opened` logged once for two loads |
| 2 `results.py` + tests | ✅ | 7 tests in `test_results.py` (rows, detail, retries, failed extraction, start errors, unlinked calls, filters, reasons) |
| 3 Admin routes | ✅ | `/admin/reasons`, `/admin/calls`, `/admin/calls/{token}`: 401 without key, 200 with, 404 unknown; route-list test updated |
| 4 Seed script | ✅ | `scripts/seed_results_demo.py`: 12 invites, 6 analysed interviews (quotes asserted word for word), 1 failed extraction, 1 unlinked call; refuses the real data dir (tested) |
| 5 Results pages | ✅ | Basic Auth (401 without / wrong password); `/results` funnel + reasons + people + unlinked; `/results/<token>` timeline, insight, quotes, transcript, error box; 404 for unknown; `/api/admin/*` 404 through Next.js; admin key not in the client bundle; no sideways page scroll at phone width |
| 6 Real-data check + recording fallback | ⏳ after the first real interview | |
| 7 CSV export (stretch) | ⏳ | |

53 API tests pass; plan 02's characterization snapshots unchanged.

---

## 0. Where it sits in the system

```
 invites.jsonl ─┐
 invite_events ─┼─► results.py (NEW use case: joins invites, events, transcripts, insights, errors)
 transcripts   ─┤        │                          funnel.py (exists)
 insights      ─┤        ▼                               │
 errors        ─┘   api/admin.py:  GET /admin/funnel (exists) · /admin/reasons · /admin/calls · /admin/calls/{token}
                         │            all behind the X-Admin-Key header (require_admin, exists)
                         │  server-to-server only (http://localhost:8000); NOT in the Next.js /api rewrite
                         ▼
 apps/web:   middleware.ts  ── Basic Auth on /results/* (password = ADMIN_KEY) ──►  browser
             lib/admin.server.ts  (server components fetch FastAPI with X-Admin-Key; the key never reaches the browser)
             app/results/page.tsx          funnel · reasons · calls table
             app/results/[token]/page.tsx  one invite: timeline · each call's insight, quotes, recording, transcript
```

**Why this shape**
- The data already exists: plan 01/02 write every event, transcript, insight and error. This plan only **reads and joins**; nothing in the call path changes.
- The admin API stays private: Next.js still forwards only `/api/invites/*` and `/api/bolna/webhook` (02 Phase 0). The results pages call FastAPI **from the Next.js server**, so the browser never sees the admin key or the admin API.
- One new use-case module (`results.py`) next to `funnel.py`, following 02's layering: routes stay thin, files are only read through `store`.

---

## 1. What "done" means

- [ ] `/results` (after a password prompt) shows the **funnel**: invited → opened → started → completed → opted out, overall and split by channel, incentive and email variant, with **completion rate** (completed ÷ invited, completed ÷ opened).
- [ ] It shows **why people left**: completed calls grouped by primary reason, with a count, total MRR, how many are savable, and 1–2 verified quotes per reason.
- [ ] It shows **every invite** in a table: name, company, status, channel, primary reason, savable score, duration, with a link to its detail page. Filter by company and status.
- [ ] `/results/<token>` shows the invite's **timeline** (each event with time) and, for **each call**: duration, talk ratio, a recording player, the insight card (reason, detail, quotes, switched to, feature gaps, price sensitivity, savable + condition, summary) and the full transcript.
- [ ] Calls whose extraction failed still show their transcript, with the error, instead of disappearing.
- [ ] Without the password: `/results` → 401. Through ngrok: `/api/admin/*` → 404 (not forwarded).
- [ ] `InviteClient.tsx` is UI only: the invite API calls live in `lib/api.ts`, the Web Call SDK lifecycle in `lib/useWebCall.ts` (02 Phase 5). The invite page behaves exactly as before.
- [ ] A seed script fills a **separate** data dir with realistic fake calls, so the page can be built and demoed before real interviews exist.

---

## 2. Design decisions

| Decision | Why | Not doing |
|---|---|---|
| **Basic Auth in Next.js middleware** on `/results/*`, password = `ADMIN_KEY` | About 20 lines, no new dependency, works over ngrok HTTPS, the browser remembers it for the session | No login page, sessions, users or roles |
| **Server components fetch FastAPI with `X-Admin-Key`** (from `apps/web/.env.local`, server-only, no `NEXT_PUBLIC_` prefix) | The key never ships to the browser; the admin API stays off the public rewrite | No client-side fetching of admin data |
| **Group by invite, show each call inside it** | The funnel counts people (invites); one invite can have up to 3 calls (retries) | No separate "calls" list for now |
| **Reasons grouped by the extraction's `primary_reason.code`** (the fixed taxonomy in `extraction.py`) | Good enough to answer "why did they leave?" for 10–50 calls; deterministic and cheap | No clustering, embeddings or theme labelling (spec §5.4, after a "go") |
| **Recording plays from Bolna's `recording_url` directly** in an `<audio>` tag | Simplest. Whether Bolna's URLs are public or signed isn't confirmed **[verify with the first real call]**; fallback in Step 6 | No downloading or re-hosting recordings |
| **New use case `results.py`, read-only** | Keeps the layering from plan 02; `funnel.py` stays as it is | No new storage files |
| **Seed script writes to a data dir you name** (refuses the real `data/` unless `--force`) | Build and demo the page without real users; never mixes fake rows into real results | No fake data in the repo |

---

## 3. Data: what gets joined

All of it exists today (plans 01–02). Linking key: Bolna's **`execution_id`**.

| Source (in `CHURNCALL_DATA_DIR`) | Fields used | Written by |
|---|---|---|
| `invites.jsonl` | token, company_slug, contact (name, trigger, plan, tenure_days), email, phone_e164, mrr, incentive, email_variant, created_at | `invites.create_invite` |
| `invite_events.jsonl` | token, event, at, meta.execution_id, meta.channel, meta.status, meta.reason | `invites.log_event*` |
| `transcripts.jsonl` | execution_id, status, duration_s, recording_url, turns | `webhooks._store_transcript_once` |
| `insights.jsonl` | execution_id, user_talk_ratio, quotes_dropped, insight (`CallInsight`) | `webhooks._extract` |
| `errors.jsonl` | webhook steps: execution_id, step, error, at · start failures: token, where, error, at (no execution_id, since the call never started) | `webhooks._step`, `calls._log_error` |
| `companies/<slug>.json` | name (display) | us, by hand |

**execution_id → invite:** every `execution_id` that appears in an invite's events (`started_phone`, `started_web`, `web_connected`, `completed`, `call_too_short`, `call_not_connected`). A transcript whose `execution_id` belongs to no invite (e.g. a test call from Bolna's dashboard) is listed under **"Unlinked calls"** on the overview, so nothing is silently dropped.

**Response shapes** (`results.py`):
```python
class CallView(BaseModel):          # one Bolna call
    execution_id: str
    channel: str | None             # from the start event / completed meta
    status: str | None              # Bolna's final status, or the not-connected status
    started_at: str | None
    duration_s: float | None
    recording_url: str | None
    user_talk_ratio: float | None
    turns: list[Turn]               # bolna.Turn
    insight: CallInsight | None
    quotes_dropped: int | None
    errors: list[dict]              # webhook-step errors for this execution_id

class InviteRow(BaseModel):          # one line in the calls table
    token: str; name: str; company: str; email_variant: str | None; incentive: bool; mrr: float | None
    status: str                     # invited / opened / started / completed / opted_out
    channel: str | None; primary_reason: str | None; savable_score: float | None
    duration_s: float | None; last_event_at: str | None

class InviteDetail(InviteRow):
    email: str; phone_e164: str | None; trigger: str; plan: str; tenure_days: int | None
    events: list[dict]              # the timeline, oldest first
    calls: list[CallView]           # newest first
    start_errors: list[dict]        # "couldn't start the call" failures (errors.jsonl rows with this token)

class ReasonGroup(BaseModel):
    code: str; count: int; mrr: float; savable: int   # savable = savable_score >= 0.6
    quotes: list[str]               # up to 2 verified quotes (from primary_reason.evidence, then best_quotes)
    tokens: list[str]
```

---

## 4. API routes (all in `api/admin.py`, all behind `require_admin`)

| Route | Returns | Notes |
|---|---|---|
| `GET /admin/funnel` | exists | Unchanged; the page adds the rates |
| `GET /admin/reasons?company=` | `list[ReasonGroup]`, biggest first | Only invites whose completed call has an insight |
| `GET /admin/calls?company=&status=` | `{"invites": list[InviteRow], "unlinked": list[CallView]}` | Newest activity first. `status` is one of the derived statuses |
| `GET /admin/calls/{token}` | `InviteDetail` | 404 via `InviteNotFound` (02's error mapping) |
| `GET /admin/calls.csv?company=` *(stretch)* | CSV: name, company, status, channel, reason code, reason detail, savable, summary, top quote | For the side-by-side with a pilot's exit survey (go/no-go criterion 2) |

---

## 5. Step by step

### Step 1: Web helpers, finishing 02 Phase 5 (≈45 min)
**Build**
- `apps/web/lib/api.ts`:
  - `type PublicInvite` (moved from `InviteClient.tsx`)
  - `postInvite(token, path, body?)`, which wraps `fetch('/api/invites/...')`
  - `logEvent(token, event, meta?)`, fire-and-forget
  - `callMe(token, phone, consent) → "ringing" | "bad_phone" | "finished" | "error"` (moves `stateForCallResponse`)
  - `optOut(token)`
- `apps/web/lib/useWebCall.ts`: `useWebCall(token, enabled) → { state, start, stop }`. It holds the dynamic `import("@bolna/web-call")`, the `useRef`, the event wiring (`state-change`, `call-start` + `web_connected` with `getRunId()`, `call-end`, `error` → `microphone_denied` / `at_capacity` / …) and cleanup. Moved as-is from `InviteClient.tsx`.
- `InviteClient.tsx` keeps only state, copy and buttons (target: under ~120 lines).

**Check:** `npm run lint && npx tsc --noEmit && npm run build`; open an invite locally: "opened" logged once, consent gating works, "Talk in browser" mints a session (`started_web` logged), opt-out works. Same behaviour as before.

### Step 2: `results.py` + tests (≈1.5 h)
**Build** `apps/api/churncall/results.py` (read-only):
- `_index()` reads all five files once per request and builds `execution_id → token`, `execution_id → transcript / insight / errors`, and `token → events`. One pass; fine at kill-test scale.
- `list_invites(company=None, status=None) -> list[InviteRow]`, `invite_detail(token) -> InviteDetail` (raises `InviteNotFound`), `reasons(company=None) -> list[ReasonGroup]`, `unlinked_calls() -> list[CallView]`.
- Uses `invites.all_invites`, `invites.events_by_token`, `invites.status_of`, `invites.load_company`, `store.read`. **No writes.**

**Tests** (`apps/api/tests/test_results.py`, fixed data files written in `tmp_path` like `test_characterization.py`):
- an invite with a completed call + insight → its row has the reason, savable score and duration; detail has the call with turns, insight and recording URL
- extraction failed → the call is listed with `insight: None` and the error
- an invite with 2 calls (a retry) → both in detail, newest first; the row uses the completed one
- a transcript with an unknown `execution_id` → appears in `unlinked_calls()`
- `reasons()` groups by code, sums MRR, counts savable (≥ 0.6), takes ≤ 2 quotes, sorts by count
- filters by company and status
- `invite_detail("nope")` → `InviteNotFound`

### Step 3: Admin routes (≈30 min)
**Build:** in `api/admin.py`: `GET /admin/reasons`, `GET /admin/calls`, `GET /admin/calls/{token}`, each one line calling `results.*`. Return the Pydantic models.

**Tests** (in `test_invites.py` or `test_results.py`):
- each route returns 401 without `X-Admin-Key` and 200 with it
- `/admin/calls/nope` → 404
- update `test_main_app_exposes_exactly_the_expected_routes` with the 3 new paths (the only route-list change)

### Step 4: Seed script for building and demos (≈30 min)
**Build** `scripts/seed_results_demo.py --data-dir <dir> [--force]`:
- Refuses `settings.data_dir` (the real one) unless `--force`.
- Writes: company `demo` (+ incentive); about 12 invites across 2 email variants; events covering every funnel stage (opened, mic denied, phone and web starts, no-answer, too short, completed, opted out); about 6 completed transcripts (realistic 8–14 turn churn interviews, written by hand in the script, ~3 reasons); matching `insights.jsonl` rows whose quotes **appear word for word** in the transcripts (assert this in the script); one extraction error; one unlinked transcript. `recording_url` points to a short public sample MP3, or `null`.

**Check:** run it into a scratch dir, point the API at it with `CHURNCALL_DATA_DIR`, and `curl -H "X-Admin-Key: …" localhost:8000/admin/reasons` returns sensible groups.

### Step 5: Results pages (≈2 h)
**Build**
- `apps/web/.env.example` gains `ADMIN_KEY=` (server-only; must match the API's). `.env.local` likewise. Update CLAUDE.md, which currently says `apps/web/.env.local` holds no secrets.
- `apps/web/middleware.ts`:
  ```ts
  export const config = { matcher: ["/results/:path*", "/results"] };
  export function middleware(req: NextRequest) {
    const expected = process.env.ADMIN_KEY;
    const [scheme, encoded] = (req.headers.get("authorization") ?? "").split(" ");
    const password = scheme === "Basic" ? atob(encoded ?? "").split(":").slice(1).join(":") : "";
    if (expected && password === expected) return NextResponse.next();
    return new NextResponse("Authentication required", {
      status: 401, headers: { "WWW-Authenticate": 'Basic realm="ChurnCall results"' },
    });
  }
  ```
  Fails closed: no `ADMIN_KEY` → always 401.
- `apps/web/lib/admin.server.ts`: `adminGet<T>(path)`, which does `fetch(\`${process.env.API_URL}/admin${path}\`, { headers: { "X-Admin-Key": process.env.ADMIN_KEY! }, cache: "no-store" })` and throws on non-200. Plus the TS types mirroring §3 (`InviteRow`, `InviteDetail`, `CallView`, `ReasonGroup`, `CallInsight`). Only imported by server components; the file name says so.
- `app/results/page.tsx` (server component; in Next 15 `searchParams` is a Promise, so `const { company, status } = await searchParams`, same as `params` in `app/i/[token]/page.tsx`):
  1. **Funnel table**: columns invited / opened / started / completed / opted out / **completion % (of invited, of opened)**; rows: overall, then by channel, incentive, email variant (from `/admin/funnel`).
  2. **Why they left**: one row per `ReasonGroup`: reason (readable label from the code), count, MRR, savable, the quotes in "…".
  3. **Calls table**: `InviteRow`s; the name links to `/results/<token>`; filter links (`?company=…`, `?status=completed`) at the top.
  4. **Unlinked calls** (only if any): execution id, status, duration.
- `app/results/[token]/page.tsx`: header (name, company, plan, tenure, MRR, status, email, phone); a **timeline** list; then one block per call:
  - `<audio controls src={recording_url}>` if present
  - duration, talk ratio, channel
  - **insight card:** reason + detail, quotes as blockquotes, switched to, feature gaps, price sensitivity, savable score + condition, summary, "N quotes dropped (not word for word)"
  - an extraction error box if present
  - the transcript (speaker labels, one turn per line)
- `app/results/layout.tsx`: `robots: noindex`; slightly wider max-width than the invite page for tables.
- Basic readability CSS only (table borders, padding, monospace for IDs).

**Check:** with the seed data: `/results` asks for a password, then shows all four sections with plausible numbers; filters work; each detail page shows timeline, insight, quotes, transcript; the failed-extraction call shows its transcript and error. `npm run lint && npx tsc --noEmit && npm run build`.

### Step 6: Real-data check + recording fallback (≈30 min, after the first real interview)
- Do one real browser interview (plan 01 flow). Confirm the call appears on `/results` with transcript, insight and recording.
- **If the recording doesn't play** (Bolna's URL needs auth or expires): add `GET /admin/calls/{token}/recording/{execution_id}` in FastAPI, which streams the file with our Bolna key, and a Next.js route `app/results/recording/[token]/[id]/route.ts` (behind the same Basic Auth) that proxies it. `<audio src>` points there.
- Save that first real webhook (`data/webhooks.jsonl`) as `apps/api/tests/fixtures/bolna_completed.json` and add a test that runs it through the webhook handler and `results.invite_detail` (02 §7.4).

### Step 7 (stretch): CSV export (≈20 min)
`GET /admin/calls.csv` + a "Download CSV" link (`app/results/export/route.ts`, Basic Auth, proxies with the key). For sending a pilot founder their results next to their exit-survey data.

---

## 6. Testing and validation

| Layer | What | How |
|---|---|---|
| `results.py` | Joins, filters, reason grouping, failed extraction, retries, unlinked calls | `pytest` with fixed data files (Step 2) |
| Admin routes | Auth (401 / 200), 404, response shape | `TestClient(create_app())` (Step 3) |
| Route list | Only the 3 (+1 CSV) new admin paths appear | Update the route-list test |
| Regression | Plan 02's characterization snapshots unchanged; all existing tests pass | `pytest -q apps/api/tests` |
| Invite page | Same behaviour after the helper split | Manual: open, mint session, opt out; lint/tsc/build |
| Results pages | Password gate; all sections render with seed data; detail pages | Manual with `seed_results_demo.py` data; lint/tsc/build |
| Privacy | `/api/admin/*` → 404 through Next.js; `/results` → 401 without the password; no `ADMIN_KEY` in the client bundle | `curl`; `grep -r ADMIN_KEY apps/web/.next/static` finds nothing |
| Real data | First real call shows up completely (Step 6) | Manual, then a fixture test |

---

## 7. Risks

| Risk | Mitigation |
|---|---|
| Bolna recording URLs aren't directly playable | Step 6 proxy fallback |
| The admin key leaks to the browser | Server components only; no `NEXT_PUBLIC_`; grep the build output (§6) |
| Seed data mixed into real results | The script refuses the real data dir without `--force` |
| Reading all files per request gets slow | Not at kill-test scale (hundreds of rows). Supabase replaces it after a "go" |
| Reason codes too coarse for real insight | Fine for go/no-go criterion 2 with 10–50 calls; `detail` + quotes carry the specifics; clustering is the post-"go" step |

---

## 8. Time

| Step | Time |
|---|---|
| 1 Web helpers (02 Phase 5) | 45 min |
| 2 `results.py` + tests | 1.5 h |
| 3 Admin routes | 30 min |
| 4 Seed script | 30 min |
| 5 Results pages | 2 h |
| 6 Real-data check + recording fallback | 30 min (after the first real call) |
| 7 CSV export (stretch) | 20 min |
| **Total** | **≈5.5 h** (+20 min stretch) |

## 9. Not in this plan
Themes × MRR clustering, charts, trends · Slack digest, Linear tickets, win-back alerts · user accounts or roles · editing or deleting data from the page · styling beyond basic readability · Supabase.
