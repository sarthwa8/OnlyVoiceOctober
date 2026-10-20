# Sarthak's plan: action plan v2, phone-only small pilot (Oct 20 → submit Oct 30)

> **Author: Sarthak** · committed 2026-10-20, 7:52 PM · moved here from `docs/ACTION_PLAN.md` (unchanged below, except this title).
> **Read the notes at the bottom** ([what's already built and what changed](#notes-whats-already-built-and-what-changed-since-this-plan-was-written)): parts of this plan were overtaken by work done the same evening.


> Replaces v1 (Oct 18). What changed: **no browser SDK needed** (phone only; if Bolna enables it later we flip one switch),
> and the "kill test" is now a **small private pilot**: 2 startups, 20–30 churned users each. No public launch.
> **S** = Sarthak (AI + voice) · **P** = Pranav (product + users). Tick boxes as you go and push.

## The goal in one line
By **Oct 30**: a working product, a demo video, and **real numbers from real calls** (how many people talked, what they said, whether a founder found it useful).

## Targets (small and realistic)
| What | Target |
|---|---|
| Startups in the pilot | 2 (3 if easy) |
| Invites sent | 40–60 |
| Completed interviews | **10+** (more is a bonus) |
| Founder says "this was useful" (written quote) | 1+ |
| Founder says what they'd pay | 1+ answer, even "nothing" |

---

## PART 1: Setup (do once, ~2 hours total). Today, Mon Oct 20

### Step 1. Get the code running on your laptop (S, 15 min)
1. Open a terminal and run:
   ```bash
   git clone https://github.com/sarthwa8/OnlyVoiceOctober.git   # skip if you already have it
   cd OnlyVoiceOctober
   git checkout claude/bold-allen-oicfqq
   git pull
   python3 -m venv .venv
   .venv/bin/pip install -r apps/api/requirements.txt
   cd apps/web && npm install && cd ../..
   .venv/bin/python -m pytest -q apps/api/tests
   ```
2. ✅ You should see **31 passed**. If not, stop and fix that first.

### Step 2. Get your keys (S, 20 min)
1. **Bolna:** log in at bolna.ai → find **API keys** in the dashboard → create one → copy it.
2. **AI model for extraction:** either
   - **Anthropic** (best quality): console.anthropic.com → API keys → create, **or**
   - **a free one**: e.g. Google AI Studio → "Get API key". Check its free limits on its own page.
3. **ngrok** (gives your laptop a public web address so people can open the invite link):
   - Sign up at ngrok.com → dashboard → **Domains** → claim your **free static domain** (looks like `something.ngrok-free.app`).
   - ⚠️ Free ngrok shows a "you are about to visit" warning page to visitors. **Before sending real invites**, upgrade to the cheapest paid ngrok plan for this week, or the warning will scare people off.

### Step 3. Fill in your settings file (S, 10 min)
1. In the repo root: `cp .env.example .env`, then open `.env` and fill in:
   ```
   BOLNA_API_KEY=<your Bolna key>
   BOLNA_AGENT_ID=            # leave empty; Step 4 fills it
   WEBHOOK_SECRET=<make up a long random word>
   ADMIN_KEY=<make up another long random word>
   PUBLIC_BASE_URL=https://<your-ngrok-domain>
   CHURNCALL_DATA_DIR=/full/path/to/OnlyVoiceOctober/data     # run `pwd` in the repo to get the path
   ```
   Plus **one** of these:
   ```
   # Option A: Anthropic
   ANTHROPIC_API_KEY=<key>
   LLM_PROVIDER=anthropic
   # Option B: free model (OpenAI-compatible)
   LLM_PROVIDER=openai_compat
   LLM_BASE_URL=<from the provider's docs>
   LLM_API_KEY=<key>
   LLM_MODEL=<model name>
   ```
2. Copy the web settings: `cp apps/web/.env.example apps/web/.env.local`, and make sure it says:
   ```
   API_URL=http://localhost:8000
   NEXT_PUBLIC_WEB_CALL_ENABLED=false     # phone only. Change to true only if Bolna enables the browser SDK.
   ```
3. ⚠️ Never commit `.env`. It's already ignored by git.

### Step 4. Create the AI interviewer in Bolna (S, 10 min)
1. Check what will be sent: `.venv/bin/python agents/sync.py --dry-run`
2. Send it: `.venv/bin/python agents/sync.py`
   - ✅ It prints `Created agent ...` and saves `BOLNA_AGENT_ID` into `.env` by itself.
   - If Pranav already created the agent, put **his** agent ID in `.env` first. Then the same command **updates** it instead of creating a duplicate.
3. In the Bolna dashboard, open the agent and check that the prompt starts with *"You are a friendly, curious research interviewer..."*.

### Step 5. Send Bolna the questions (S, 5 min)
- Paste `docs/BOLNA_QUESTIONS.md` into the Bolna Builders Slack (or email support@bolna.ai).
- The **only blocking question** now is #2: *which countries can our number call?* If your pilot users are in India, you're probably fine. Ask anyway.
- Don't wait for answers. Carry on.

### Step 6. Start everything (S, 5 min, every time you work)
Open **3 terminal windows** in the repo folder:
```bash
# Terminal 1: the API (brain)
cd apps/api && ../../.venv/bin/uvicorn churncall.main:app --reload --port 8000
# Terminal 2: the website (invite page)
cd apps/web && npm run dev
# Terminal 3: the public address
ngrok http 3000 --url https://<your-ngrok-domain>
```
✅ Open `https://<your-ngrok-domain>` in a browser. A page loads (a "not found" page is fine at this point).

### Step 7. Tell Bolna where to send call results (S, 5 min)
- In the Bolna dashboard, open your agent → find the **webhook URL** setting → paste:
  `https://<your-ngrok-domain>/api/bolna/webhook`
- Save.

### Step 8. Test call to yourself (S, 20 min). ⭐ The most important step today
1. Create a fake company file `data/companies/test.json`:
   ```json
   {"name": "Shoplytics", "product_description": "analytics dashboards for small online stores", "founder_name": "Priya", "incentive": "a $5 Amazon voucher"}
   ```
2. Create `pilots/test.csv` (the `pilots/` folder is for your own files; don't commit real people's data):
   ```
   name,email,phone_e164,plan,trigger
   Sarthak,<your email>,+91XXXXXXXXXX,Growth,cancelled
   ```
3. Make your invite link: `.venv/bin/python scripts/make_invites.py --company test --csv pilots/test.csv`
   - ✅ It prints a link, also saved in `data/links/test.csv`.
4. Open the link **on your phone** → type your number → tick the consent box → **Call me now**.
5. ✅ Your phone rings. The AI says *"Hi Sarthak, I'm an AI assistant calling on behalf of Priya at Shoplytics..."*
6. Pretend you cancelled. Talk for 2–3 minutes, then hang up.
7. Within a minute, check the `data/` folder:
   - `transcripts.jsonl` has your call
   - `insights.jsonl` has the extracted reasons and quotes
8. Save the real call result for the tests: copy the completed webhook body into `apps/api/tests/fixtures/bolna_completed.json` (remove your phone number first). If you don't know where to find it, tell Claude and we'll add a line that saves it automatically.
9. Check the funnel: open `http://localhost:8000/invites/funnel?key=<ADMIN_KEY>`. It should show 1 opened, 1 started, 1 completed.

**If something breaks:** copy the error from Terminal 1 and paste it to Claude.

---

## PART 2: Get 2 startups (P, start today, in parallel with Part 1)

### Step 9. Ask 6–8 startups (P, 30 min)
Message founders you know (WhatsApp, LinkedIn, email). Copy-paste:
> Hey ___! We're building an AI that calls churned users and finds out the real reason they left (not the "too expensive" checkbox).
> Free pilot this week: send us 20–30 users who cancelled or didn't convert in the last 90 days (just **name, email, and phone if you have it**).
> We email them a link from you, they get a 4-minute call, and you get a report with the real reasons and their actual quotes. Nothing goes out without your OK on the email wording.
> Can I send you a 1-page summary?

- **Goal:** 2 yeses by **Wed Oct 22**.
- Phone numbers help a lot (phone-only), but email-only users can still enter their number on the invite page.

### Step 10. For each startup that says yes (P, 20 min each)
1. Get their CSV (`name,email` minimum; `phone_e164,plan,mrr,trigger` if they have them).
2. Write their company file `data/companies/<slug>.json` (name, product description, founder name, optional incentive).
3. Run `make_invites.py` for them. You get `data/links/<slug>.csv`.
4. Write the invite email **from the founder** and get their OK:
   > Subject: Quick question about why you left [Product]
   > Hi {name}, I'm {founder}, founder of [Product]. You recently cancelled, and I'd really like to know what we got wrong. Would you give us 4 minutes? Tap here and our AI assistant will call you: {link}
   > (It's an AI, the call is recorded so we can learn, and you can opt out anytime.) Thank you! {founder}
5. Send it with **Gmail mail merge** (e.g. a free Gmail mail-merge add-on) using `links/<slug>.csv`, from the founder's email if they allow it, or yours.

---

## PART 3: The pilot (Wed Oct 22 → Sun Oct 26)

### Step 11. Dry run first (both, Tue Oct 21)
- [ ] Each of you gets an invite from **real Gmail**, opens it **on a phone**, and completes a call.
- [ ] No ngrok warning page (paid plan on).
- [ ] The funnel shows both calls.

### Step 12. Send wave 1 (P, Wed Oct 22)
- [ ] Invites go out for startup #1 (and #2 if ready). Send in the **morning** in the users' time zone.
- [ ] Keep the laptop **on, plugged in and awake** with all 3 terminals running (`caffeinate -dis` on Mac, or set sleep to "never").

### Step 13. Every evening (both, 30 min, Oct 22–26)
1. Open the funnel and write the numbers in `docs/pilot-log.md`: sent → opened → started → completed.
2. **Listen to 3–5 real calls** (the recording links are in `transcripts.jsonl`).
3. Write down the top 3 problems (e.g. "AI talks too much", "misheard the product name").
4. **S** fixes the prompt (`agents/interviewer/prompt.md`), then runs `agents/sync.py` to push it to Bolna.

### Step 14. Wave 2 (P, Fri Oct 24 or Sat Oct 25)
- A short reminder email to people who didn't open it, plus startup #2 if they weren't in wave 1.

### Step 15. Founder check-in (P, Sun Oct 26)
Send each founder their report: the top reasons, 5 quotes, and what they could fix. Ask 3 questions:
1. "Was anything here new to you?"
2. "Would you act on any of it?"
3. "What would you pay per month for this every time someone cancels?" (Koji charges ~€79/month, so note how their answer compares.)
→ Paste their answers into `docs/pilot-log.md`. **These are your best pitch material.**

---

## PART 4: Finish and submit (Mon Oct 27 → Thu Oct 30)

| Day | Sarthak | Pranav |
|---|---|---|
| **Mon Oct 27** | Simple results page: top reasons + quotes (from `insights.jsonl`) | Collect founder quotes + ask for a paid pilot / letter of intent |
| **Tue Oct 28** | Run `eval/interviews/simulate.py` on 6 personas → write a short quality report | Draft the written submission (problem → product → real numbers → Bolna features → business) |
| **Wed Oct 29** | Make the demo reliable (a fresh test call works every time) | Record the **2-minute video**: a real cancelled user's quote, the call, the report |
| **Thu Oct 30** | Final check, push everything | **Submit.** Oct 31 is the backup day. |

**Demo video outline (2 min):**
1. (0:00) "Exit surveys say 'too expensive'. That's rarely the real reason."
2. (0:15) Live: open an invite → phone rings → AI interviews.
3. (0:50) The report: real reasons, real quotes, from our pilot.
4. (1:30) Numbers: X invited, Y talked, what founders said.
5. (1:50) "ChurnCall, built on Bolna."

---

## If something goes wrong
| Problem | What to do |
|---|---|
| Bolna can't call your pilot users' country | Pick pilot users in India, or ask Bolna for a local number |
| No startup says yes by Wed | Use **your own network**: ask 20 friends who cancelled any subscription to do a call about that product. Still real calls. |
| Fewer than 10 completed calls | Submit anyway, be honest about the numbers, and lead with the quality of what people said |
| The AI behaves badly on calls | Fix the prompt that evening (Step 13). Don't send more invites until it's fixed. |
| Bolna enables the browser SDK | Set `NEXT_PUBLIC_WEB_CALL_ENABLED=true` in `apps/web/.env.local` and restart the website. Done. |

---

## Notes: what's already built and what changed since this plan was written

> Added by Pranav on 2026-10-20 (evening). The plan above is Sarthak's and stays as he wrote it. These notes record what was built the same day, so nobody redoes finished work or follows a step that no longer matches the code. Build plans: [01 invite page](01-invite-page.md) · [02 architecture cleanup](02-api-architecture-cleanup.md) · [03 results page](03-results-page.md).

### 1. "Phone only": both channels are already built and working
The plan assumes the Bolna browser SDK isn't available. It is: on 2026-10-20 our server minted a real browser session on our account (`POST /web-call/freeswitch-session` → 200 with a `run_id`). The invite page already offers both:
- **Talk in browser** (Bolna Web Call SDK): no phone number needed, works for any country, and is the spec's main channel.
- **Call me now** (Bolna outbound): consent checkbox, up to 3 attempts, calling-hours guardrails bypassed because the user asked.

Today `apps/web/.env.local` has `NEXT_PUBLIC_WEB_CALL_ENABLED=true`, so both buttons show.

**If we decide to run the pilot phone-only after all:**
1. Set `NEXT_PUBLIC_WEB_CALL_ENABLED=false` in `apps/web/.env.local` and restart the web app. The page then shows only the phone form. No other code changes.
2. These become **blockers** (they don't matter for browser calls):
   - **A phone number on the Bolna account.** The account currently lists **none**, and outbound calling is **untested**.
   - **Which countries that number can call** (question #2 in `docs/BOLNA_QUESTIONS.md`).
   - **One successful test call to a real phone** (Step 8) before any invite goes out.
   - Pilot CSVs need **phone numbers**, or users must type theirs on the page.
   - Phone calls use telephony minutes from the wallet (currently 500; unit unconfirmed).
3. **Recommendation:** keep both on. Browser removes the phone-number and country risks; phone stays for people who prefer it. Go phone-only only if browser calls misbehave in the dry run (Step 11).

### 2. Part 1 setup: status on Pranav's laptop
| Step | Status |
|---|---|
| 1 Code running | ✅ Setup is now `.venv/bin/pip install -e "apps/api[dev]"` (`requirements.txt` was replaced by `apps/api/pyproject.toml`). Tests: **55 passed** (not 31). |
| 2 Keys | ✅ Bolna key · ✅ **Groq** for extraction (`openai/gpt-oss-120b`; checked on two sample transcripts, about 2.4 s each, all quotes word for word) · ✅ ngrok free static domain. ⚠️ Paid ngrok (or a deploy) still needed before real invites. |
| 3 `.env` | ✅ Filled in (`CHURNCALL_ENV`, `ADMIN_KEY`, `WEBHOOK_SECRET`, `PUBLIC_BASE_URL`, absolute `CHURNCALL_DATA_DIR`, Groq settings). `apps/web/.env.local` also needs `ADMIN_KEY` now (for the results page). |
| 4 Bolna agent | ✅ Created (`churncall-interviewer-v1`) with `agents/sync.py`; the current prompt is live (welcome message `{{opening_line}}`: separate phone and browser openers). Use the existing `BOLNA_AGENT_ID` so `sync.py` updates it instead of creating a duplicate. |
| 5 Bolna questions | ⏳ Still to send. Account facts found via the API: web calls enabled, **max 2 concurrent calls**, **no phone numbers listed**. |
| 6 Start everything | Same 3 terminals. On Pranav's laptop the API runs on **port 8010** (8000 is taken by another app), so `apps/web/.env.local` uses `API_URL=http://localhost:8010`. |
| 7 Webhook URL | ✅ Set by `agents/sync.py` from `PUBLIC_BASE_URL` (no dashboard step needed). |
| 8 Test call | ⏳ **Not done yet. This is the most important next step.** Raw webhooks are now saved automatically to `data/webhooks.jsonl`, so the fixture in 8.8 is a copy from there (remove the phone number). |
| 9 Check the funnel | Changed: `/invites/funnel?key=…` no longer exists. Open **`/results`** (password = `ADMIN_KEY`) or run `curl -H "X-Admin-Key: $ADMIN_KEY" localhost:8010/admin/funnel`. |

### 3. Things in the plan to update when you follow it
- **Interview length is now "about 3 minutes" everywhere** (page, AI opener, prompt). Change "4-minute call" (Step 9 message) and "4 minutes" (Step 10 email) to 3.
- **Part 4, Mon Oct 27 "simple results page": already built** ([build plan 03](03-results-page.md)). `/results` shows the funnel with completion rates, reasons with MRR and verified quotes, every person, and each call's transcript, insight and recording. Use it for the pilot log (Step 13) and the founder reports (Step 15).
- **"Started" in the funnel** now means a phone call Bolna accepted, or a browser call that actually connected. Someone who blocked the mic no longer counts as started.
- **Safety and structure** ([build plan 02](02-api-architecture-cleanup.md)): the old open `POST /calls` route is gone, Next.js only exposes the invite routes and the webhook, and the API code moved (`guide.py` → `interview.py`, `webhook.py` → `bolna.py`, the webhook pipeline → `webhooks.py`).
- **Weekday labels:** Oct 20, 2026 is a **Tuesday**, so the plan's weekdays are one day off. Go by the dates: Wed Oct 21 dry run · Thu Oct 22 wave 1 · Sat–Sun Oct 24–25 wave 2 · Mon Oct 26 founder check-in · Tue–Fri Oct 27–30 finish and submit (Sat Oct 31 is the deadline).
- **Demo data:** `scripts/seed_results_demo.py --data-dir <scratch dir>` fills a separate folder with realistic fake calls for practising the results page or recording the demo. It refuses the real `data/` folder.
