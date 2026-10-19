# Build plan 01: Invite page (bare minimum, Next.js)

> v2.1 (verified against Bolna docs, the web-call README, ngrok v3.39 CLI and Sarthak's code on 2026-10-19) · Owner: **Pranav (Person B)** · Backend owner: **Sarthak (Person A)**
> Target: working end to end by **Mon Oct 20 morning**, so real invites go out before the **Tue Oct 21 go/no-go** ([ACTION_PLAN](../docs/ACTION_PLAN.md)).
> **No styling.** Default browser look, readable on a phone. The only job: **email link → user consents → interview starts → every step is counted correctly.**
> Product spec: [CHURNCALL.md](../docs/CHURNCALL.md) · Backend: [apps/api/README.md](../apps/api/README.md) · Bolna Web Call SDK: [docs](https://www.bolna.ai/docs/sdks/web-call)

---

## 0. Where the invite page sits in the whole system

```
   TRIGGER               INVITE                 INVITE PAGE (this plan)          CALL                    EVIDENCE
   ───────               ──────                 ───────────────────────          ────                    ────────
 pilot CSV ──► make_invites.py ──► links.csv ──► Gmail mail merge ──► user taps link
 (Stripe later)   data/invites.jsonl              (Resend later)            │
                                                                            ▼
                                                     https://<public-domain>/i/<token>
                                                                            │
                                                     ngrok ──► Next.js :3000 (apps/web)
                                                                │  page  /i/[token]
                                                                │  /api/* rewritten ──► FastAPI :8000 (apps/api)
                                                                ▼
                                          ┌─ "Talk in browser" ─► /invites/{t}/web-session ─► Bolna web-call session ─┐
                                          ├─ "Call me now"  ────► /invites/{t}/call ────────► Bolna outbound call ────┤
                                          └─ "Opt out" ─────────► /invites/{t}/optout                                  │
                                                                                                                       ▼
                                                                          Bolna agent "churncall-interviewer" (Sarthak)
                                                                                                                       │
                                     /bolna/webhook  ◄──── webhook on EVERY status change; only "completed" has it all ┘
                                         ├─► transcripts.jsonl
                                         ├─► extraction (Claude, verified quotes) ─► insights.jsonl      (Sarthak, done)
                                         └─► invite_events: "completed"                                   (this plan)
                                                                                     │
                                         /invites/funnel ◄───────────────────────────┘  ──► Oct 21 go/no-go numbers
```

**Who owns what**
| Piece | Owner | Status |
|---|---|---|
| Interviewer prompt, Bolna agent, outbound client, webhook parser, extraction, persona evals | Sarthak | Day-1 build merged (`apps/api`, `agents/`, `eval/`) |
| Invite generator, invite routes + funnel, Next.js page, ngrok setup | **Pranav (this plan)** | To build |
| Small edits to Sarthak's files: `main.py` (include router, mark completed), `bolna.py` (mint web session), `guide.py` (split out prompt variables) | Pranav, **agreed with Sarthak first** | To build |

**What survives after a "go" on Oct 21**
| Now (kill test) | After go | Changes needed |
|---|---|---|
| `apps/web` with one page | Same app grows into the dashboard (themes × MRR, quotes, audio) | Add routes and styling. The page stays. |
| JSONL files in `data/` | Supabase Postgres (`invites`, `sessions`, events become rows) | Swap the store module in `invites.py`. Routes stay the same. |
| CSV + `make_invites.py` | Stripe webhook creates invites automatically | A new trigger calls the same `create_invite()` function. |
| Gmail mail merge | Resend sends invites from code | Uses `links.csv` fields as template variables. |
| ngrok on a laptop | Vercel (web) + Render/Fly (API) | Change `API_URL` and the Bolna webhook URL. |

---

## 1. What "done" means (check every box before sending real invites)
- [ ] A pilot CSV becomes one private link per user, plus a `links.csv` ready for mail merge.
- [ ] Opening a link in a **real browser** logs `opened`. Email link scanners that only fetch the page **do not**.
- [ ] **Call me now** (phone + consent box ticked) makes Bolna ring the phone, and logs `started_phone`.
- [ ] **Talk in browser** starts a Bolna web call that knows who the user is, and logs `started_web`. (Can sit behind a flag until Bolna enables web calls on our account.)
- [ ] Mic blocked → the page switches to "we'll call you instead" by itself.
- [ ] The post-call webhook marks the invite `completed` (only if the user actually talked: ≥ 3 user turns) and records which channel it came from.
- [ ] `/funnel` shows **unique users** at each stage, **split by channel, incentive and email variant**. That's go/no-go criterion (1).
- [ ] Opt out works and hides the call buttons for good.
- [ ] The link works from a phone, opened from a real Gmail email, through the **stable public URL**, with **no ngrok warning page** in front of it.

---

## 2. Design decisions (and why)

| Decision | Why |
|---|---|
| **Next.js (App Router) in `apps/web`, the official stack** | No rewrite after Oct 21. The same app becomes the dashboard. |
| **All logic stays in FastAPI.** Next.js only renders the page and forwards `/api/*` | One source of truth. The Bolna API key and the prompt never reach the browser. Sarthak's code is reused as-is. |
| **One public URL:** ngrok → Next.js :3000; Next.js rewrites `/api/*` → FastAPI :8000 | Same origin, so there's no CORS setup. The mic needs HTTPS, and ngrok provides it. |
| **`opened` is logged by client-side JS, not when the page is served** | Gmail/Outlook link scanners fetch links but don't run JS. Logging on page load would inflate "opened". |
| **`user_data` is built on the server** from the invite. Anything the browser sends is ignored | Nobody can change the interviewer prompt or impersonate another invite. |
| **Prompt template lives in the Bolna agent; we send only the variables** (plus `system_prompt` as a fallback until verified) | Bolna's call API and SDK docs describe `user_data` as "dynamic variables as defined in the agent prompt" (max 50 KB). A whole per-call prompt is probably not supported. **Bolna's placeholder syntax is `{{variable}}` (double braces)**; our `prompt.md` uses `{variable}`, so the copy in the Bolna agent must be converted. |
| **Only the `completed` webhook counts** | Bolna POSTs the execution to the webhook **at every status change** (queued, ringing, in-progress, call-disconnected, completed, …). Transcript, recording and duration are only complete on `completed`. |
| **No ngrok warning page in front of users** | Free ngrok puts an "are you sure?" anti-phishing page in front of all browser traffic. A churned user seeing a phishing warning before an AI interview will bounce, which would poison the completion rate. Free ngrok is fine for building; the public URL used in real invites must not have it (Step 0). |
| **Events log, not a status field** | Append-only `invite_events.jsonl`. Status and funnel are worked out from events, so nothing gets out of sync. |
| **Count unique tokens per stage** | Someone may press start twice. The go/no-go needs people, not clicks. |
| **Consent checkbox for phone calls; server refuses without it** | User-initiated calls are our legal line (US TCPA treats AI voices as artificial voices). |

---

## 3. Data (JSONL in `data/`, which is **gitignored**: it holds real emails, phones and transcripts)

**Input CSV** (from a pilot startup), one row per churned user:
```csv
name,email,phone_e164,plan,mrr,trigger,tenure_days,incentive,email_variant
Asha,asha@example.com,+919800000000,pro,49,cancelled,140,$5 Amazon voucher,founder
Ben,ben@example.com,,starter,19,trial_ended,,,generic
```
- Required: `name`, `email`. Everything else is optional.
- `incentive` overrides the company default for A/B testing incentive vs no incentive. `email_variant` (`founder`/`generic`) tags which email version they got. Both feed the funnel split.
- `mrr` isn't used by the page. It's stored now so revenue-weighted themes work later without asking pilots again.

**`data/companies/<slug>.json`**: Sarthak's `Company` model:
```json
{"name": "Acme", "product_description": "invoicing software for freelancers", "founder_name": "Priya", "incentive": null, "win_back_offer": null}
```

**`data/invites.jsonl`**, one row per user:
```json
{"token": "k3J9xQ2pLm0a", "company_slug": "acme",
 "contact": {"name": "Asha", "trigger": "cancelled", "plan": "pro", "tenure_days": 140},
 "email": "asha@example.com", "phone_e164": "+919800000000", "mrr": 49,
 "incentive": "$5 Amazon voucher", "email_variant": "founder", "created_at": "2026-10-19T10:00:00Z"}
```
`contact` matches Sarthak's `Contact` model exactly, so `render_prompt` and the prompt variables work unchanged.

**`data/invite_events.jsonl`**, append-only:
```json
{"token": "k3J9xQ2pLm0a", "event": "started_phone", "at": "2026-10-19T11:02:00Z", "meta": {"execution_id": "exec_9f2"}}
```
| Event | Logged by | When |
|---|---|---|
| `opened` | page JS → `/event` | First time the page renders in a real browser (deduped on the server) |
| `started_web` | `/web-session` | A Bolna web session was minted |
| `web_connected` | page JS → `/event` | SDK `call-start` fired (meta: `execution_id` from `call.getRunId()`) |
| `started_phone` | `/call` | Bolna accepted the outbound call (meta: `execution_id`, which `POST /call` returns) |
| `mic_denied` | page JS → `/event` | Mic permission refused |
| `call_ended_client` | page JS → `/event` | The SDK reported the call ended (meta: `reason`) |
| `opted_out` | `/optout` | User clicked opt out |
| `completed` | webhook | A webhook with `status == "completed"` arrived with ≥ 3 user turns (meta: `execution_id`, `channel`). Logged once per token. |

**Derived status** (latest wins): `invited → opened → started → completed`, or `opted_out` at any point.

---

## 4. Routes

FastAPI defines the routes below **without** `/api`. The browser calls them **with** `/api`, and Next.js strips it when forwarding.

| Browser calls | FastAPI route | Does | Rules |
|---|---|---|---|
| (page render, server side) | `GET /invites/{t}` | Public view of the invite: `{first_name, company_name, founder_name, trigger_short, incentive, phone_hint, status}` | Unknown → 404. `phone_hint` is masked (`+91 ••••• ••000`); the full number is never sent to the browser. No event logged. |
| `POST /api/invites/{t}/event` | same | Body `{event, meta?}`. Allowed: `opened`, `web_connected`, `mic_denied`, `call_ended_client` | `opened` stored only once per token. |
| `POST /api/invites/{t}/web-session` | same | Builds `user_data` on the server → `BolnaClient.mint_web_session()` → returns Bolna's JSON **unchanged**. Logs `started_web`. | 404 / 409 (completed or opted out) / 429 after 3 starts. |
| `POST /api/invites/{t}/call` | same | Body `{phone_e164?, consent}`. Empty phone → use the number from the CSV. Starts the outbound call with the same `user_data`. Logs `started_phone`. | `consent != true` → 400. Phone must match `^\+[1-9]\d{7,14}$` → else 422. 409 / 429 as above. |
| `POST /api/invites/{t}/optout` | same | Logs `opted_out`. | Idempotent. |
| `GET /api/invites/funnel?key=…` | same | Unique-user counts per stage, overall and grouped by `company`, `channel`, `incentive` (`yes`/`none`), `email_variant` | Wrong or missing key → 401. |
| (Bolna) `POST /api/bolna/webhook` | existing | Sarthak's handler + mark completed | Existing `X-Webhook-Secret` check. |

**`user_data` sent to Bolna** (both channels). Every key except `invite_token`, `channel` and `system_prompt` must match a `{{placeholder}}` in the Bolna agent's prompt:
```json
{"invite_token": "k3J9xQ2pLm0a", "channel": "web",
 "company_name": "Acme", "founder_name": "Priya", "contact_name": "Asha", "product_description": "…",
 "trigger_description": "cancelled their subscription", "trigger_short": "cancelled", "research_goals": "1. …",
 "offer_rule": "…", "plan": "pro", "tenure_days": 140, "usage_facts": "none provided", "incentive_line": "…",
 "example_vague": "it wasn't working for us",
 "system_prompt": "<fully rendered prompt; fallback until we confirm whether Bolna uses it>"}
```

---

## 5. Step by step

Each step says **what you build**, **how it works**, **how it connects to the rest**, and **how to check it**.

### Step 0: Unblock (10–20 min, do first, mostly waiting on others)
1. **Bolna:** in the Builders Slack or at support@bolna.ai, ask:
   - to **enable the Web Call SDK** (beta, off by default)
   - whether `user_data` can override the whole system prompt, or only fill `{{variables}}`
   - where `user_data` shows up in the webhook payload: `context_details` directly, or `context_details.recipient_data`
   - whether webhooks support a custom secret header (otherwise we check the three published Bolna source IPs)
   - which countries our default outbound number can call (pilot users may be in India, the US, or elsewhere)
2. **Sarthak:** agree on the three small edits to his files (§0 table). Also ask him to:
   - put `agents/interviewer/prompt.md` into the Bolna agent **as the template**, with every `{variable}` changed to **`{{variable}}`** (Bolna's syntax), and the same for the welcome message in `config.json`
   - make his webhook handler skip extraction unless `status == "completed"`. Bolna sends a webhook on every status change, so today extraction could run (and cost money) more than once per call.
   - check the agent's **calling-hours guardrails**. A user who taps "call me now" at 11 pm shouldn't be blocked; Bolna's `/call` has a `bypass_call_guardrails` flag for user-requested calls.
   - write a web-call version of the opener: it currently says *"I'm … calling on behalf of…"* and *"this call is recorded"*. Fine on the phone, slightly off in a browser.
3. **Public URL (decide now):**
   - **For building and the dry run:** free ngrok account + **claim the free static domain** (dashboard → Domains). Without it, the URL changes on every restart.
   - **For real invites:** free ngrok shows every browser visitor an anti-phishing warning page first, which you can't turn off from your app. Pick one before sending: **(a) upgrade to the cheapest paid ngrok plan** for the invite window (simplest; nothing else changes), or **(b) deploy** (Next.js on Vercel + FastAPI on Fly/Railway). (a) is the recommendation for this week.
4. Put in `.env` (root):
   - `BOLNA_API_KEY`, `BOLNA_AGENT_ID`, `WEBHOOK_SECRET`, `ANTHROPIC_API_KEY` (Sarthak has these)
   - the new `ADMIN_KEY`
   - `PUBLIC_BASE_URL=https://<your-static-domain>` (Step 1 builds links from it)
   - `CHURNCALL_DATA_DIR=/absolute/path/to/repo/data`. Sarthak's `main.py` defaults to `data` **relative to wherever uvicorn is started** (his README starts it from `apps/api`), while `make_invites.py` runs from the repo root. An absolute path keeps both on the same files.

**Check:** you have the static domain and a decision on (a) or (b), `.env` is filled, the Bolna questions have been sent, and Sarthak's existing tests pass (`pytest -q apps/api/tests`: 4 passed on 2026-10-19).

---

### Step 1: Invite store + generator (45 min)
**Build**
- `.gitignore`: add `data/` and `apps/web/.next/`, `apps/web/node_modules/`.
- `apps/api/churncall/invites.py`, the storage half (routes come in Step 2):
  - `Invite` pydantic model (fields as in §3); `contact: Contact` reuses Sarthak's model.
  - `create_invite(company_slug, row) -> Invite`: token = `secrets.token_urlsafe(9)`, append to `invites.jsonl`.
  - `get_invite(token)`, `log_event(token, event, meta)`, `events_for(token)`, `status_of(token)`.
  - `load_company(slug) -> Company` from `data/companies/<slug>.json`.
  - All file paths come from `CHURNCALL_DATA_DIR` (same as `main.py`), so tests can use a temp dir.
- `scripts/make_invites.py`:
  ```bash
  python scripts/make_invites.py --company acme --csv pilots/acme.csv
  ```
  → validates rows (email present, phone E.164 if given), calls `create_invite` per row, writes `data/links/acme.csv` with `name,email,link,email_variant` where `link = $PUBLIC_BASE_URL/i/<token>`. Prints `"Created 47 invites, skipped 2 (bad email on rows 5, 19)"`.

**Connects to:** `create_invite()` is the single way invites get made. The Stripe trigger calls it after a "go".

**Check:** run it on a 3-row sample CSV → 3 lines in `invites.jsonl`, 3 links in `links/acme.csv`, and `git status` shows nothing in `data/`.

---

### Step 2: Invite routes in FastAPI (1 h)
**Build**
- In `invites.py`: `router = APIRouter(prefix="/invites")` with the routes from §4, **except** `/call` and `/web-session` (Steps 4 and 6).
- The `/funnel` route is declared **before** `/{token}` routes so `funnel` isn't read as a token.
- In `main.py` (Sarthak's file): `from .invites import router as invites_router` and `app.include_router(invites_router)`.

**How the funnel works**
- Load all invites + events. For each token, collect the set of stages reached.
- `channel` = the channel of the **last start event before `completed`** (or from `user_data.channel` in the webhook, if Bolna echoes it).
- `incentive` group = `"yes"` if the invite's incentive (or the company default) is set, else `"none"`.
- Output:
  ```json
  {"overall": {"invited": 50, "opened": 31, "started": 14, "completed": 9, "opted_out": 2,
               "started_by_channel": {"web": 9, "phone": 5}, "completed_by_channel": {"web": 5, "phone": 4}},
   "by_company": {"acme": {...}}, "by_incentive": {"yes": {...}, "none": {...}}, "by_email_variant": {"founder": {...}, "generic": {...}}}
  ```

**Check:** `uvicorn` running → `curl localhost:8000/invites/<token>` returns the public view with a masked phone; `POST …/event {"event":"opened"}` twice → one `opened` line; `curl "localhost:8000/invites/funnel?key=…"` shows `opened: 1`.

---

### Step 3: Next.js app + page shell (1 h)
**Build**
```bash
cd apps && npx create-next-app@15 web --ts --app --eslint --no-tailwind --no-src-dir --import-alias "@/*" --use-npm --yes
```
- `apps/web/next.config.ts`:
  ```ts
  const nextConfig = {
    async rewrites() {
      return [{ source: "/api/:path*", destination: `${process.env.API_URL ?? "http://localhost:8000"}/:path*` }];
    },
  };
  export default nextConfig;
  ```
- Delete the starter content and CSS. Keep only a minimal root `layout.tsx` with `<meta name="viewport" …>` (Next adds it by default).
- `app/i/[token]/page.tsx`, a **server component**:
  ```tsx
  import InviteClient from "./InviteClient";

  export default async function InvitePage({ params }: { params: Promise<{ token: string }> }) {
    const { token } = await params;
    const res = await fetch(`${process.env.API_URL}/invites/${token}`, { cache: "no-store" });
    if (res.status === 404) return <p>This link isn't valid.</p>;
    const invite = await res.json();
    if (invite.status === "completed") return <p>Thanks, you've already shared your feedback.</p>;
    if (invite.status === "opted_out") return <p>Got it. You won't hear from us about this again.</p>;
    return <InviteClient token={token} invite={invite} />;
  }
  ```
- `app/i/[token]/InviteClient.tsx` (`"use client"`): renders the copy (§6). On mount: `useEffect(() => { fetch(\`/api/invites/${token}/event\`, {method: "POST", body: JSON.stringify({event: "opened"}), headers: {"Content-Type": "application/json"}}) }, [])`. Buttons are placeholders for now.
- `apps/web/.env.local`: `API_URL=http://localhost:8000`, `NEXT_PUBLIC_WEB_CALL_ENABLED=false`.

**Connects to:** the server component calls FastAPI directly (`API_URL`). The browser only ever calls `/api/*` on its own origin, which Next.js forwards. This is the same pattern the dashboard will use.

**Check:** `npm run dev` + uvicorn → `localhost:3000/i/<token>` shows "Hi Asha…"; the events file gets **one** `opened`. `curl localhost:3000/i/<token>` (no JS, like a scanner) → **no** new `opened`. Bad token → "This link isn't valid."

---

### Step 4: Phone path, "Call me now" (1 h)
**Build**
- `guide.py` (Sarthak's file): split `render_prompt` into `prompt_variables(company, contact) -> dict` and `render_prompt(...)`, which uses it. Behaviour unchanged; his tests must still pass.
- `invites.py`: helper `build_user_data(invite, channel) -> dict` = `prompt_variables(company, invite.contact)` + `invite_token` + `channel` + `system_prompt` (§4).
  - **Per-invite incentive:** `prompt_variables` reads `company.incentive`, so pass `company.model_copy(update={"incentive": invite.incentive})` when the CSV row set one. Otherwise the A/B incentive never reaches the interviewer's closing line.
- `POST /invites/{t}/call`:
  1. Check status (404 / 409) and starts so far (429 at 3).
  2. `consent is True` else 400. Phone = body phone or the CSV phone; validate E.164 else 422.
  3. `BolnaClient().start_outbound_call(phone, user_data=build_user_data(invite, "phone"))`. That's Sarthak's client, unchanged.
  4. Log `started_phone` with `execution_id` from Bolna's response (`POST /call` returns `{message, status: "queued", execution_id}`), and also append to `calls.jsonl` as his `/calls` does.
  5. Return `{ok: true}`. Bolna errors → 502 with a friendly message; log the error to `errors.jsonl`.
- `InviteClient.tsx`: phone input (placeholder shows `phone_hint`, so empty means "use the number you have"), consent checkbox, **Call me now** disabled until ticked. On success: *"Your phone will ring in a few seconds."*

**Connects to:** Bolna places the call with the agent Sarthak configured. Our `invite_token` rides along in `user_data`, so the webhook (Step 5) can link the call back to the invite.

**Check:** `POST` without consent → 400 (test). With your own number via the page → **your phone rings**, the agent greets you by name, and `started_phone` is logged.

---

### Step 5: ngrok + webhook → "completed" (45 min)
**Build**
- Run `ngrok http 3000 --url https://<your-static-domain>` (ngrok v3 syntax; checked against `ngrok http --help`, v3.39).
- In the Bolna agent settings: webhook URL = `https://<your-static-domain>/api/bolna/webhook`.
  - **Webhook auth:** use the `X-Webhook-Secret` header if Bolna supports custom headers. If not, accept webhooks only from Bolna's three published source IPs (13.203.39.153, 13.126.9.249, 13.202.133.53), read from `X-Forwarded-For`, which ngrok and Next.js pass along.
- `main.py` `_process()` (Sarthak's file), after the transcript is saved:
  ```python
  if record.status != "completed":          # Bolna sends a webhook on every status change
      return
  ctx = payload.get("context_details") or payload.get("user_data") or {}
  ctx = ctx if isinstance(ctx, dict) else {}
  vars_ = {**ctx.get("recipient_data", {}), **ctx}   # user_data may sit at either level [verify]
  token = vars_.get("invite_token") or invites.token_for_execution(record.execution_id)
  user_turns = sum(1 for t in record.turns if t.speaker == "user")
  if token and user_turns >= 3:
      invites.mark_completed(token, record.execution_id, channel=vars_.get("channel"))   # no-op if already completed
  ```
  - `token_for_execution()` looks up the `execution_id` saved on `started_phone` (from `POST /call`) or `web_connected` (from `getRunId()`), in case Bolna doesn't echo `user_data`.
  - If `channel` isn't echoed, `mark_completed` takes it from whichever start event holds that `execution_id`.
  - The status guard goes **before** extraction too (Sarthak's part, Step 0), so a call is only extracted once.
- **Save one real webhook payload** to `apps/api/tests/fixtures/` (Sarthak's checklist item). Then adjust where `invite_token` actually appears.

**Connects to:** this closes the loop. The same webhook also triggers Sarthak's extraction, so a completed invite has a matching row in `insights.jsonl` (joined on `execution_id`).

**Check:** finish a real phone call from Step 4 → within a minute, `transcripts.jsonl` + `insights.jsonl` get rows, and the event log shows `completed` with `channel: "phone"`. Reloading the page now shows "Thanks, you've already shared your feedback."

---

### Step 6: Browser path, "Talk in browser" (1.5 h, needs web-call access)
**Build**
- `bolna.py` (Sarthak's file): add
  ```python
  def mint_web_session(self, user_data: dict, timeout: float = 15.0) -> dict:
      payload = {"agent_id": self.agent_id, "user_data": user_data}
      resp = httpx.post(f"{self.base_url}/web-call/session", json=payload, headers=self._headers(), timeout=timeout)
      resp.raise_for_status()
      return resp.json()
  ```
- `POST /invites/{t}/web-session`: same checks as `/call` (no consent box: tapping "Talk in browser" after the disclosure *is* the request, and the agent repeats the disclosure first). Ignore the request body. `mint_web_session(build_user_data(invite, "web"))`. Log `started_web` (with any id in the response). Return Bolna's JSON **unchanged**. Bolna `at_capacity` or other errors → pass the status through.
- `apps/web`: `npm i @bolna/web-call@3.0.1` (latest on npm as of 2026-10-19). In `InviteClient.tsx`:
  ```tsx
  import { BolnaWebCall } from "@bolna/web-call";

  const callRef = useRef<BolnaWebCall | null>(null);
  useEffect(() => {
    const call = new BolnaWebCall({ sessionUrl: `/api/invites/${token}/web-session` });
    call.on("state-change", (s) => s === "connecting" && setState("connecting"));
    call.on("call-start", () => {
      setState("live");
      logEvent("web_connected", { execution_id: call.getRunId() });   // links the webhook back to this invite
    });
    call.on("call-end", ({ reason }) => { setState("ended"); logEvent("call_ended_client", { reason }); });
    call.on("error", (e) => {
      if (e.code === "microphone_denied") { logEvent("mic_denied"); return setState("mic_denied"); }  // reveal phone form
      if (e.code === "at_capacity") return setState("busy");          // "use Call me now instead"
      if (e.code === "already_active") return;
      setState("error");   // mint_failed, connect_failed, call_rejected, autoplay_blocked
    });
    callRef.current = call;
    return () => call.stop();   // stop() is idempotent per the README
  }, [token]);
  // button: onClick={() => callRef.current?.start()}   ← must be the click handler itself (autoplay rule)
  ```
  - SDK facts used here (from the [web-call README](https://github.com/bolna-ai/web-call)): states `idle / connecting / ringing / active / ended`; six events (`state-change`, `media-permission`, `call-start`, `call-end`, `error`, `volume-level`); seven error codes (`mint_failed`, `at_capacity`, `microphone_denied`, `connect_failed`, `call_rejected`, `autoplay_blocked`, `already_active`); `getRunId()` returns the execution id used in webhooks.
  - In dev, React StrictMode runs the effect twice, so one extra client is created and stopped right away. That's harmless, and `opened` is deduped on the server anyway.
- Only show the button when `NEXT_PUBLIC_WEB_CALL_ENABLED=true`.

**Connects to:** the browser never sees the API key. It gets a single-use session (~120 s) from our server, which already holds the right `user_data`. The call ends → Bolna sends the same webhook as phone calls → Step 5 marks it `completed` with `channel: "web"`.

**Check:** desktop Chrome and a real phone (through ngrok): tap → mic prompt → agent speaks with your name → hang up → thank-you screen → `completed` with `channel: "web"`. Block the mic → the phone form appears and `mic_denied` is logged.

**If access hasn't arrived:** leave the flag off and ship phone-only. The kill test still runs, and you note it in the go/no-go.

---

### Step 7: Tests + dry run (1 h)
**Tests**: `apps/api/tests/test_invites.py`, temp `CHURNCALL_DATA_DIR`, Bolna mocked (monkeypatch `BolnaClient`):
- generator: 3-row CSV → 3 unique URL-safe tokens and 3 links; a bad email row is skipped and reported
- `GET /invites/{bad}` → 404; the public view masks the phone and never contains the email
- `opened` posted twice → stored once; an unknown event name → 422
- `/call`: no consent → 400; bad phone → 422; valid → Bolna called with `invite_token` and `channel: "phone"` in `user_data`; 4th start → 429; after `opted_out` → 409
- `/web-session`: request body ignored (send a fake `system_prompt`, assert Bolna got ours); Bolna's JSON returned unchanged
- webhook: `status: completed` + `invite_token` + 3 user turns → `completed`; 1 user turn → not completed; `status: call-disconnected` or `in-progress` → ignored (no event, no extraction); the same `completed` webhook sent twice → one event; `invite_token` under `context_details.recipient_data` → still found; no token but a known `execution_id` (from `started_phone` or `web_connected`) → `completed` via the fallback
- per-invite incentive: a CSV incentive overrides the company default in the `user_data` Bolna receives
- funnel: no key → 401; unique counting (2 starts → `started: 1`); grouping by channel / incentive / variant is correct
- Sarthak's existing `test_core.py` still passes after the `guide.py` refactor

**Dry run** (both of you, about 20 min):
1. CSV with you and Sarthak, one with an incentive and one without, different `email_variant`.
2. `make_invites.py` → mail-merge two **real Gmail emails** to yourselves.
3. Each opens the link **on a phone from the Gmail app**: one does web, one does phone.
4. `/funnel` must show `invited 2 · opened 2 · started 2 · completed 2`, split correctly by channel, incentive and variant.

---

## 6. Page content (the words matter; styling doesn't)
Top to bottom, plain HTML elements:
1. **"Hi {first_name}, I'm {founder_name} from {company_name}."**
   *"You recently {trigger_short}. Would you give us about 3 minutes to tell us what we got wrong? You'll talk with our AI interviewer, and I read every answer myself."*
2. **Disclosure (required):** *"This is an AI, not a person. The conversation is recorded and transcribed. You can stop at any time."*
3. **[ Talk in browser ]** (if enabled)
4. **"Or we'll call you":** phone input (placeholder `phone_hint`) · ☐ *"Yes, call me now about my feedback"* · **[ Call me now ]** (disabled until ticked)
5. **Status line:**

   | State | Text |
   |---|---|
   | connecting | Connecting… |
   | live | You're live. Talk whenever you're ready. (plus **[ End call ]**) |
   | ended | Thank you! {incentive} is on its way. (or just "Thank you!") |
   | mic_denied | We couldn't use your microphone. No problem, we'll call you instead. ↓ |
   | busy | Lots of people right now. Tap "Call me now" instead. |
   | ringing | Your phone will ring in a few seconds. |
   | error | Something went wrong. Reply to the email and we'll sort it out. |
6. Footer: **[ Opt out ]** · *"Questions, or want your data deleted? Just reply to the email."*

---

## 7. Running it (3 terminals)
```bash
# 1. API
cd apps/api && ../../.venv/bin/uvicorn churncall.main:app --reload --port 8000
# 2. Web
cd apps/web && npm run dev
# 3. Public URL (static domain)
ngrok http 3000 --url https://<your-static-domain>
```
FastAPI and `make_invites.py` read the root `.env` (`load_dotenv()` searches upward from the calling file; the script must call it too), and `CHURNCALL_DATA_DIR` points both at the same `data/`. Next.js reads only `apps/web/.env.local` (`API_URL`, `NEXT_PUBLIC_WEB_CALL_ENABLED`) and holds no secrets.
Keep the laptop awake while invites are live: `caffeinate -dis` on macOS.

---

## 8. Before sending real invites (checklist)
- [ ] Static ngrok domain in use, and `PUBLIC_BASE_URL` matches it (links are generated from it)
- [ ] **No warning page:** open a link on a phone in a private tab. It must go straight to "Hi …", with no ngrok "You are about to visit" screen (paid ngrok plan or deployed, Step 0)
- [ ] Sarthak's prompt is in the Bolna agent with `{{double_brace}}` placeholders, and a test call greets you by name (not "Hi {{contact_name}}")
- [ ] Bolna webhook URL points at `/api/bolna/webhook` on that domain; one real payload saved in `tests/fixtures/`
- [ ] Dry run passed (§5 Step 7) from real Gmail on real phones
- [ ] `data/` doesn't appear in `git status`
- [ ] `ADMIN_KEY` set; `/funnel` works with it and returns 401 without it
- [ ] Laptop on power, `caffeinate` running, all 3 terminals up
- [ ] Sarthak has reviewed the edits to `main.py`, `bolna.py`, `guide.py`

---

## 9. Time
| Step | Time |
|---|---|
| 0 Unblock | 15 min |
| 1 Store + generator | 45 min |
| 2 FastAPI routes + funnel | 1 h |
| 3 Next.js + page shell | 1 h |
| 4 Phone path | 1 h |
| 5 ngrok + webhook | 45 min |
| 6 Browser path | 1.5 h |
| 7 Tests + dry run | 1 h |
| **Total** | **about 7 h** (5.5 h if web-call access is late and Step 6 waits) |

**Order matters:** Steps 1 → 2 → 3 → 4 → 5 give a fully working **phone-only** funnel. That's enough to start the kill test even if Step 6 is blocked on Bolna.

---

## 10. Open questions for Bolna (⛔ = blocks a step)
| Question | Blocks | Fallback if the answer is bad |
|---|---|---|
| ⛔ Web Call SDK enabled on our account? | Step 6 | Phone-only kill test |
| ⛔ Can our default outbound number call the pilots' countries? | Step 4 for those users | Browser-only for those users, or buy a local number in Bolna |
| Can `user_data` override the whole system prompt? | Nothing (we send both) | Template in the agent + variables (already the plan) |
| Where does `user_data` appear in the webhook (`context_details` or `.recipient_data`)? | Nothing (we check both) | `execution_id` → token lookup (Step 5) |
| Do webhooks support a custom secret header? | Nothing | Allow only Bolna's three source IPs |

**Answered by the docs on 2026-10-19 (no need to ask):**
- `POST /call` returns `execution_id` immediately ([call API](https://www.bolna.ai/docs/api-reference/calls/make.md)).
- Webhooks fire on **every status change**; only `completed` has the full data ([call flow](https://www.bolna.ai/docs/concepts/call-flow.md)).
- Prompt variables use **`{{name}}`** syntax and are filled from `user_data` ([call API](https://www.bolna.ai/docs/api-reference/calls/make.md)).
- The web call's execution id comes from `getRunId()`, and the mic error code is `microphone_denied` ([web-call README](https://github.com/bolna-ai/web-call)).
- Transcript format is one string, `assistant: …` / `user: …` per line, which Sarthak's parser already handles ([executions API](https://www.bolna.ai/docs/api-reference/executions/get_execution.md)).

---

## 11. Not in this plan
Styling, Tailwind or shadcn · scheduled "call me at 5 pm" · inbound number + code · sending email from code (Gmail mail merge for the pilot) · paying out incentives · Supabase · login · the dashboard · Hinglish or other languages · deploying (ngrok only).
