# CLAUDE.md: project context

## The one goal
We are building **ChurnCall** for the Bolna Buildathon, and nothing else. ChurnCall is an AI voice interviewer (on Bolna) that talks to a SaaS company's churned users and turns those conversations into churn reasons weighted by revenue at risk, with verbatim quotes.
- Spec: `docs/CHURNCALL.md`. This week's plan: Sarthak's plan `build-plans/00-sarthaks-plan.md` (read the notes at its end). Build plans: `build-plans/`.
- **`archive/` holds dropped ideas (CareCall, FieldLog, PagerCall, Awaaz Relay, idea brainstorms). Never build from it, suggest those ideas, or treat it as current.** Only open it if someone asks about the history.
- New features get a build plan in `build-plans/NN-name.md` first (steps, how each connects to the system, how to check it), like `01-invite-page.md`.

## Team and dates
- Sarthak: AI + voice (Bolna agent, prompt, extraction, evals). Pranav: product + GTM (invite flow, web app, pilots, pitch).
- Shared repo `sarthwa8/OnlyVoiceOctober`. Default/shared branch: `claude/bold-allen-oicfqq`. Pranav works on `pranav` and merges via PRs.
- Kill-test go/no-go Oct 21 · submit Oct 30 (deadline Oct 31) · finale Nov 20.

## How the system fits together
CSV of churned users → `scripts/make_invites.py` → private links → user opens `/i/<token>` (Next.js, `apps/web`) → "Talk in browser" (Bolna Web Call SDK) or "Call me now" (Bolna outbound) → Bolna agent (`agents/interviewer/`) → Bolna webhook → FastAPI (`apps/api`) saves the raw payload, marks the invite completed, saves the transcript, runs extraction → `/results` page (Next.js server components call FastAPI `/admin/funnel`, `/admin/reasons`, `/admin/calls` with `X-Admin-Key`).
- API layers (build plan 02): `api/` (HTTP only) → `calls`, `webhooks`, `funnel`, `invites` (use cases) → `interview`, `extraction` → `store`, `bolna`, `llm` (adapters) → `config`. Only `config.py` reads env vars; only `store.py` touches files; only `bolna.py` knows Bolna's shapes; use cases raise `errors.py` exceptions that `api/` maps to status codes.
- Next.js forwards only `/api/invites/*` and `/api/bolna/webhook` to FastAPI (one public origin; docs and admin stay private). Secrets live in the root `.env` (gitignored); `apps/web/.env.local` holds one server-only secret, `ADMIN_KEY`, for the `/results` pages (Basic Auth + server-side calls to `/admin/*`; never `NEXT_PUBLIC_`).
- Storage is JSONL in `CHURNCALL_DATA_DIR` (`data/`, gitignored: real emails, phones and transcripts). It moves to Supabase after a "go" by rewriting `store.py`.
- Push agent changes with `python agents/sync.py` (`--dry-run` first). `prompt.md` is the Bolna template and `config.json` holds Bolna's v2 agent schema.

## Bolna facts we've verified (don't re-guess these)
- Prompt variables use `{{name}}` and are filled from a call's `user_data`.
- Webhooks fire on **every status change**; only `status == "completed"` has the full transcript and recording.
- `POST /call` returns `execution_id`. Browser sessions are minted with `POST /web-call/freeswitch-session` (per `@bolna/web-call` 3.0.1), and the response includes `run_id`.
- Webhook source IPs: 13.203.39.153, 13.126.9.249, 13.202.133.53.
- Our account (2026-10-20): web calls enabled, max 2 concurrent calls, no phone numbers listed (outbound untested).

## Rules
- Users always start the conversation (tap in the browser or ask for a call). Never cold-call. The server refuses calls without consent.
- Never commit `.env`, `data/` or real user data. Every quote in an insight must appear word for word in the transcript.
- Setup: `python3 -m venv .venv && .venv/bin/pip install -e "apps/api[dev]"` (the API is the installed package `churncall`; no `sys.path` hacks). Run tests with `.venv/bin/python -m pytest -q apps/api/tests` (they never read the real `.env`). Characterization snapshots in `apps/api/tests/snapshots/` only change on purpose. For the web app: `npm run lint` and `npx tsc --noEmit` in `apps/web`.
