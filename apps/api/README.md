# ChurnCall API

Structure and the reasons behind it: [build-plans/02-api-architecture-cleanup.md](../../build-plans/02-api-architecture-cleanup.md).
Dependencies only point downward: `api/` → use cases → domain → adapters → `config`.

## What's here
| Path | Layer | What it does |
|---|---|---|
| `churncall/api/` | HTTP | `create_app()`; `public.py` (invite routes), `admin.py` (`/admin/funnel`, `X-Admin-Key` header), `bolna_webhook.py` (auth: secret header or Bolna IPs). Thin: parse → call one use case → return. Domain errors → HTTP status in one place. |
| `churncall/calls.py` | use case | Start "Talk in browser" / "Call me now": checks the invite may start, builds `user_data` on the server, calls Bolna, logs the start |
| `churncall/webhooks.py` | use case | Bolna webhook pipeline: save raw → update funnel → store transcript once → extract. A failing step never stops the next |
| `churncall/funnel.py` | use case | Funnel numbers (unique users per stage, by company / channel / incentive / email variant) |
| `churncall/invites.py` | domain | Invite creation + validation, event log, status, start limits |
| `churncall/interview.py` | domain | Company/Contact, opening line, prompt variables, local prompt rendering (formerly `guide.py`) |
| `churncall/extraction.py` | domain | Structured extraction through `llm.py`, then **drops any quote not found word for word in the user's lines** |
| `churncall/bolna.py` | adapter | Everything that knows Bolna's API shapes: client, webhook parsing (formerly `webhook.py`), statuses, source IPs |
| `churncall/llm.py` | adapter | Provider switch: Anthropic (default) or any OpenAI-compatible endpoint, including free tiers |
| `churncall/store.py` | adapter | The only code that reads/writes data (JSONL in `CHURNCALL_DATA_DIR`), with a lock for "check then write". Supabase later = this file |
| `churncall/config.py` | config | All env vars, read in one place; `.env` loaded once |
| `churncall/errors.py` | — | Domain errors that `api/` maps to status codes |
| `churncall/main.py` | entry | `app = create_app()` for `uvicorn churncall.main:app` |
| `../../agents/interviewer/` | — | The Bolna agent prompt (`{{variables}}`) and settings; push with `agents/sync.py` |
| `../../eval/interviews/simulate.py` | — | Text simulation: our interviewer vs 6 churned-user personas |

## Run
```bash
python3 -m venv .venv && .venv/bin/pip install -e "apps/api[dev]"   # pinned deps in apps/api/pyproject.toml
cp .env.example .env   # fill ANTHROPIC_API_KEY, BOLNA_API_KEY, BOLNA_AGENT_ID, WEBHOOK_SECRET
.venv/bin/python -m pytest -q apps/api/tests
cd apps/api && ../../.venv/bin/uvicorn churncall.main:app --reload
# public URL: run the web app too and `ngrok http 3000`; Next.js forwards /api/bolna/webhook to FastAPI
curl -H "X-Admin-Key: $ADMIN_KEY" localhost:8000/admin/funnel   # funnel numbers (not reachable through Next.js)
python eval/interviews/simulate.py --persona price_cover   # costs API money; keep runs small
```
Results go to `data/*.jsonl` (webhooks raw, transcripts, insights, invite events, errors). That's enough for the kill test; Supabase comes after it.
Tests never read the real `.env` (`tests/conftest.py`). `tests/test_characterization.py` pins behaviour with snapshots; a snapshot only changes on purpose (`UPDATE_SNAPSHOTS=1`).

## Day-0 checklist: confirm against the Bolna docs or dashboard (I couldn't reach bolna.ai from my environment)
- [ ] Outbound call endpoint path + field names (`/call`, `agent_id`, `recipient_phone_number`, `user_data`) in `bolna.py`
- [x] Prompt is a `{{variable}}` template; paste `prompt.md` into the agent and pass variables via `user_data` (no whole-prompt override needed). Still [ ] confirm where `user_data` shows up in the webhook.
- [ ] Web Call SDK: how to start a browser session and pass per-session context
- [ ] Webhook payload: copy the first real one from `data/webhooks.jsonl` to `apps/api/tests/fixtures/` and adjust `bolna.parse_webhook` / `bolna.call_variables`
- [ ] Webhook auth: does Bolna sign webhooks or support a custom header? Wire it into `WEBHOOK_SECRET`.
- [ ] Turn-taking settings in `config.json` (endpointing, silence re-prompt, hangup, max duration)

## Using a free LLM instead of Claude
Set `LLM_PROVIDER=openai_compat`, `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` (and optionally `LLM_MODEL_CHEAP`) in `.env`. See `.env.example`.
Free models are weaker at structured output, so `llm.py` asks for JSON, validates it against the schema and retries once; the verbatim-quote check still runs. Compare the free model's extraction against Claude on the same 5 transcripts before trusting it. Free tiers have rate limits and may use your data for training, so don't send real customer transcripts to a provider whose terms you haven't read.

**Questions to send Bolna:** `docs/BOLNA_QUESTIONS.md` (paste-ready). **Handoff status:** `docs/HANDOFF_2026-10-20.md`.
