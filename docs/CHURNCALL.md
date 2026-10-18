# ChurnCall: the AI that calls your churned users and tells you why they left

> v1.0 · 2026-10-18 · Team of **2** · Status: **🔒 LOCKED: this is what we're building**
> Decision history: [CareCall](DECISION.md) → [FieldLog](FIELDLOG.md) → [PagerCall](PAGERCALL.md) → **ChurnCall**. Earlier docs are kept for reference.
> **[verify]** = confirm in Bolna or vendor docs, or with a real test, before relying on it. Numbers marked *(est.)* are assumptions to validate with pilots.

---

## 0. One paragraph

Every SaaS company loses users and almost none of them know why. Cancellation surveys get a click on "too expensive" (which usually isn't the real reason), and exit-survey response rates are tiny. Founders *know* they should talk to churned users, but nobody has time to chase 40 people a week for a call.

**ChurnCall does it for them.** When a user cancels, downgrades or quietly stops using the product, ChurnCall invites them to a 4-minute voice conversation: by phone at the moment they choose, or in the browser with one tap. An AI interviewer runs a real research-grade conversation with follow-up questions. ChurnCall then turns every call into structured evidence:
- churn reasons
- competitors they switched to
- missing features
- price sensitivity
- whether they could be won back

It rolls them up into **themes weighted by revenue at risk**, with the actual quotes and audio clips. Users who can be won back get routed to the founder the same day. Product gaps become Linear/Jira tickets with evidence attached.

> **Tagline:** *Your churned users will tell you exactly why they left. Someone just has to call them.*

---

## 1. Why we locked this

| Question | Answer |
|---|---|
| Is it a tech-industry, B2B, venture-scale product? | Yes. Every subscription software company has churn, and retention is directly tied to revenue. It expands into win-loss interviews, onboarding research, NPS follow-ups and expert calls (see §10). |
| Does voice genuinely make it better? | Yes. People skip surveys and text, but a short conversation produces the *real* reason with follow-ups ("too expensive" → "we only used it for one report a month, so it wasn't worth it"). Voice gives depth and completion rates text can't. |
| Founder–market fit for **us**? | Strong. We did GTM and marketing work for startups and saw first-hand that nobody talks to churned customers. Our AI-research background is the moat: interview quality, synthesis you can trust, evaluation. |
| Real users by Oct 31? | Yes. A few startups we already know lend us their churned and trial-dropped users. Churn happens every day, so the call volume is real. |
| Bolna fit / not overlapping their customers? | Bolna customers make sales, support, collections and recruiting calls. Research calls are new ground. We'll use outbound calls, the **Web Call SDK**, inbound, multilingual, extraction, webhooks, call transfer, and possibly a custom LLM. |
| Riskiest assumption | **Will churned users actually talk to an AI?** We test it in the first 48 hours (§8.1). |

---

## 2. The customer and the problem

### Who buys
- **Wedge:** product-led SaaS and subscription startups with **100 to 5,000 paying customers**, where the founder or head of product is the buyer. At that stage churn kills growth, and there's no research team.
- **Users inside the company:** founder, product manager, head of growth/marketing, customer success.
- **Geography:** global from day one (English). Indian SaaS and consumer subscription apps are a strong second segment, and Hinglish works, which plays to Bolna's strength.

### The workflow today
1. A user cancels → maybe fills a one-click exit survey → "Too expensive" / "Other".
2. The founder occasionally emails churned users "can we chat?" and gets few replies. *(est.; validate)*
3. Product decisions are made from gut feel, loud users and support tickets.
4. Retention tools (cancellation-flow tools like Churnkey, discount offers) try to *stop* churn with offers but don't *explain* it.
5. A proper research programme (recruit, schedule, interview, code transcripts, synthesise) costs a researcher days per cycle, which startups don't have.

### What it costs them
- Every percentage point of monthly churn compounds into lost revenue. At $50k MRR, 5% monthly churn is $2.5k MRR lost every month. *(illustrative)*
- They fix the wrong thing: pricing changes when the real issue is onboarding, or features when the real issue is reliability.
- They miss users who could be won back with a single founder call.

---

## 3. Product

### 3.1 How it works

```
 trigger                invite                 conversation              evidence                  action
 ───────                ──────                 ────────────              ────────                  ──────
 Stripe cancel    →  email / in-app / SMS  →  AI interview, 3–6 min  →  per-call record        →  Slack digest
 Downgrade            "Got 4 min? Tell us      • phone: "call me now"     reasons, competitor,      Linear/Jira tickets
 Trial ended           what we got wrong"      • browser: 1-tap talk      gaps, price, savable,     win-back alert to founder
 Inactive 14d         + optional $5 thanks    • inbound number            quotes + timestamps       CRM note (HubSpot)
 CSV / manual                                  (adaptive follow-ups)    → themes × MRR at risk    (optional) live transfer
```

### 3.2 Triggers (how users get into the funnel)
- **Stripe webhooks:** subscription cancelled, downgraded, payment failed and then cancelled.
- **Product analytics** (PostHog / Segment / Mixpanel): trial ended without converting, inactive for N days, key feature abandoned.
- **CSV upload** or a manual "invite these 30 people" for back-catalogue churn. **This is the pilot fast path.**
- A rules page sets who to invite, delay, frequency cap, and exclusions (enterprise accounts, already-contacted users).

### 3.3 Invite and consent (designed for compliance *and* a high completion rate)
**Default: the user chooses to start the conversation.** We do not cold-call people.

- **Invite** by email (default), in-app message or SMS/WhatsApp (if the company has consent). Short, personal, sent from the founder: *"I'm Priya, founder of X. You cancelled yesterday. Would you give us 4 minutes to tell us what we got wrong? Talk to our AI interviewer now, or pick a time."*
- **Three ways to talk:**
  1. **"Talk in browser":** Bolna **Web Call SDK** [verify], one tap, no phone number needed. *Primary for global users.*
  2. **"Call me now / at 5 pm":** the user enters or confirms a phone number. That click is their consent. Bolna outbound call.
  3. **"Call us":** an inbound number with a short code that identifies them.
- **Thank-you incentive** (optional, set by the company): a $5–10 gift card or one free month, sent after the call is completed.
- **In the first sentence of every call:** AI disclosure, recording notice, and an easy opt-out.
- **Why this matters:** in the US, AI-voice outbound calls fall under robocall consent rules (the FCC treated AI-generated voices as "artificial" voices under the TCPA in 2024) [verify current status]. India and the EU have their own rules on commercial calls and data. User-initiated calls + browser voice keep us on the right side *and* convert better than a surprise call.

### 3.4 The interview
**The interview guide is auto-generated per company from:**
- product description
- pricing plans
- known competitors
- the team's current hypotheses ("we think onboarding is too long")
- research goals ("why do trial users not convert?")

**Structure** (switch-interview / jobs-to-be-done style, 3–6 minutes):
1. **Warm open and permission:** "We'd love your honest take. Nothing you say will hurt anyone's feelings."
2. **The story:** "Take me back to when you first signed up. What were you hoping it would do?"
3. **The moment it broke:** "When did you start thinking about cancelling? What happened that day?"
4. **Forces:**
   - *push:* what was frustrating
   - *pull:* what they switched to and why
   - *anxiety:* what almost kept them
   - *habit:* what they do now instead
5. **Probe and ladder:** at least 2 follow-ups on the main reason ("When you say too expensive, expensive compared to what?"). Never suggest an answer.
6. **Win-back probe** (only if the company enables it): "If X were fixed, would you consider coming back?" → savable score.
7. **Close:** thank them, explain what happens next (incentive), and offer "Want the founder to call you personally?"

**Interviewer behaviour rules:**
- the user talks at least 70% of the time
- one question at a time
- mirror their words back
- no leading or double-barrelled questions
- detect short, low-effort answers and re-ask from a different angle
- respect a hard time limit
- never argue
- never pitch more than the configured offer

**Coverage tracking:** the interviewer tracks which research goals have been answered and steers toward gaps before the time runs out. This is a technical differentiator (§5.3).

### 3.5 Per-call output (structured, with evidence)
```json
{
  "completed": true,
  "duration_s": 247,
  "primary_reason": {"code": "onboarding_friction", "confidence": 0.86,
                     "evidence": [{"quote": "I never figured out how to connect my Shopify store", "t": 63.2}]},
  "secondary_reasons": [{"code": "price_value_mismatch", "evidence": [...]}],
  "switched_to": {"name": "Competitor Y", "why": "had a one-click Shopify import"},
  "feature_gaps": ["shopify_import", "bulk_edit"],
  "price_sensitivity": "value_not_price",
  "savable": {"score": 0.72, "condition": "if Shopify import existed"},
  "sentiment_arc": ["positive", "frustrated", "neutral"],
  "best_quotes": [{"quote": "...", "t": 112.4}],
  "summary": "2-line summary for Slack"
}
```
- The reason codes come from a **taxonomy**: a default SaaS churn taxonomy plus company-specific codes that are learned (§5.4).
- **Every quote must appear word for word in the transcript.** This is enforced in code, so we have zero invented evidence.

### 3.6 Cross-call insights (the dashboard)
- **Themes × MRR at risk:** e.g. "Onboarding friction: 38% of churned users, $4.2k MRR. Trend ↑ since the v2 release."
- **Theme detail:** definition, the users in it, plan mix, and the 5 most representative quotes with **playable audio clips**.
- **Competitor board:** who they left for and why.
- **Savable list:** sorted by MRR × savable score, with one-click "founder call" (or a live transfer during the call [verify]).
- **Trends:** themes over time, before and after releases.
- **Weekly digest** to Slack and email: top 3 themes, biggest change, 3 quotes, 2 recommended actions.
- **Close the loop:** "Create Linear issue" attaches the evidence (quotes, number of users, MRR).

---

## 4. Demo (2-minute video and the finale stage)
1. **0:00–0:12 Hook:** a cancellation-survey screen with "Too expensive" ticked. Voiceover: *"This is all most companies learn when you leave. It's usually not even true."*
2. **0:12–0:50 Live trigger:** on stage, a judge cancels a subscription in our demo SaaS app. Within 20 seconds an email arrives; the judge taps **Talk in browser** (or their phone rings after they tap "call me"). The AI interviews them with real follow-ups.
3. **0:50–1:20 The insight appears:** the dashboard updates live and the judge's quote lands in a theme. Then cut to the **real pilot data**: "We interviewed 47 churned users from 3 startups this month," with the top themes, MRR at risk, and real (consented) audio clips.
4. **1:20–1:40 Action:** a savable-user alert goes to the founder's Slack; one click creates a Linear issue with evidence; a founder quote: "We changed our onboarding because of this."
5. **1:40–2:00 Proof and ask:** completion rate, interviews done, themes found, and one pilot paying. "ChurnCall: every churned user, interviewed. Built on Bolna."

---

## 5. Architecture

```
 ┌──────────── Triggers ───────────┐      ┌───────────────────── apps/api (FastAPI · Python 3.12) ─────────────────────┐
 │ Stripe webhooks                 │      │ /webhooks/stripe, /webhooks/posthog, /contacts/import (CSV)                │
 │ PostHog / Segment / Mixpanel    │ ───► │ rules engine → invite queue → email (Resend) / SMS / in-app link           │
 │ CSV upload / manual             │      │ /sessions/{token}: invite landing → start web call OR schedule phone call  │
 └─────────────────────────────────┘      │ guide generator (LLM) · interview context builder (user_data)              │
                                          │ /bolna/webhook → transcript → EXTRACTION → per-call record                 │
 ┌──────────── Bolna ──────────────┐      │ SYNTHESIS worker: embeddings → clustering → theme labels → MRR weighting  │
 │ Agent "interviewer"             │ ◄──► │ integrations: Slack, Linear/Jira, HubSpot; incentives (gift-card API)     │
 │  • Web Call SDK (browser)       │      │ (v2) /v1/chat/completions: custom-LLM interviewer brain w/ coverage state │
 │  • outbound (on user request)   │      └───────────────┬─────────────────────────────────────────────────────────────┘
 │  • inbound number + code        │                      │
 │ STT: Deepgram / Sarvam (Hinglish)│     ┌───────────────▼──────────────┐      ┌──────── apps/web (Next.js 15) ─────────┐
 │ TTS: Cartesia / ElevenLabs      │      │ Postgres (Supabase) + pgvector│ ◄──► │ invite landing + web-call page         │
 └─────────────────────────────────┘      │ Storage: recordings, clips    │      │ dashboard: themes, quotes, audio, MRR  │
                                          └──────────────────────────────┘      │ onboarding: connect Stripe, guide setup │
                                                                                └────────────────────────────────────────┘
```

### 5.1 Stack
| Layer | Choice | Why |
|---|---|---|
| Voice | **Bolna:** Web Call SDK + outbound + inbound | Browser voice avoids phone-consent problems and telephony cost for global users. Phone for those who prefer it. |
| STT / TTS | Deepgram (English, multiple accents) and Sarvam (Hinglish) · Cartesia or ElevenLabs Turbo | Choose on Day 1 by quality + latency tests. A warm, unhurried, "researcher" voice. |
| Interviewer LLM | v1: Bolna-hosted LLM with a structured prompt. v2: **our custom LLM endpoint** with coverage state. | Ship fast, then add the research-grade brain once evals show v1's gaps. |
| Extraction & synthesis LLM | Claude Sonnet 5.5 (extraction, theme labels), Haiku 5.5 (cheap passes) | Structured JSON output, long-transcript quality |
| Backend | **FastAPI** + a Postgres-backed job queue (e.g. Procrastinate or RQ) | Python fits our AI/ML synthesis work. One process to start. |
| DB | **Supabase** Postgres + pgvector + Storage + Auth | Embeddings, clips, realtime dashboard, multi-tenant RLS |
| Web | **Next.js 15** + Tailwind + shadcn/ui, Recharts | Dashboard + invite and call pages |
| Email | Resend (or Postmark) | Deliverability for invites |
| Hosting | Vercel (web), Render/Fly (API, worker) | Free or cheap tiers |

### 5.2 Bolna specifics
- **Agent `interviewer`:**
  - prompt = methodology + behaviour rules
  - `user_data` = company context, interview guide, the user's plan/tenure/usage facts ("you used reports 3 times last month"), and the company's offer settings
- **Channels:** Web Call SDK session from the invite page [verify how the SDK passes context]; outbound call API when the user taps "call me"; inbound number with a 4-digit code (DTMF) to link the caller to their record.
- **Settings:** long end-of-speech pause (people think before answering), interruptions on, gentle re-prompts, hard limit ~6 minutes, warm wrap-up at 5.
- **Call transfer:** "Want to talk to the founder right now?" → transfer to the founder's number if they're available [verify]. Otherwise a scheduled callback.
- **Webhooks:** transcript + recording + metadata → extraction pipeline.
- **Languages:** English by default; Hinglish/Hindi for Indian products, switching automatically.

### 5.3 The research-grade interviewer (our technical edge)
- **Guide compiler:** company context + research goals → a guide of *goals* (not fixed questions). Each goal has probes and a "satisfied when" test.
- **Coverage tracker** (v2, custom LLM endpoint): after each user turn, a fast model updates `{goal: covered|partial|open, depth}` and picks the next move (probe deeper / move on / ladder / wrap up). The voice LLM gets only the next move plus style rules, which keeps answers short and quick.
- **Anti-bias guardrails:** a leading-question detector checks the agent's draft turn ("Was it the price?" is rejected in favour of "What made you start looking elsewhere?").
- **Low-effort detection:** one-word answers or "I don't know" trigger a reframe ("If a friend asked you whether to use it, what would you tell them?").

### 5.4 Synthesis pipeline (trustworthy insights)
1. **Extraction:** per-call JSON (§3.5) with reason codes + evidence spans. Quotes are checked word for word against the transcript; anything that fails is dropped and the call is re-extracted.
2. **Reason statements:** each call yields 1–4 atomic "reason statements" (e.g. "couldn't connect Shopify store").
3. **Embeddings → clustering** (HDBSCAN over statement embeddings) → an LLM labels each cluster (name, definition, inclusion rule). Clusters are mapped onto the taxonomy; new themes are proposed when a cluster doesn't fit.
4. **Weighting:** theme share by user count *and* by MRR (from Stripe). Trend over weekly windows.
5. **Representative evidence:** the quotes closest to each cluster's centre, with audio clips cut from the timestamps (ffmpeg).
6. **Human-in-the-loop:** PMs can merge, split or rename themes, and the taxonomy learns from it.

### 5.5 Data model
```sql
orgs            (id, name, plan, stripe_account_id, settings jsonb)            -- settings: offers, incentive, limits
integrations    (org_id, kind, encrypted_creds, status)                         -- stripe, posthog, slack, linear, hubspot
research_goals  (id, org_id, text, active)
guides          (id, org_id, version, compiled jsonb, created_at)
contacts        (id, org_id, external_id, email, phone, name, plan, mrr_cents, tenure_days, usage jsonb, locale)
triggers        (id, org_id, contact_id, kind, payload, occurred_at)            -- cancel, downgrade, trial_end, inactive
invites         (id, org_id, contact_id, trigger_id, channel, token, sent_at, opened_at, started_at, status)
sessions        (id, invite_id, channel ('web','phone_out','phone_in'), bolna_execution_id, started_at, ended_at,
                 duration_s, consent_at, recording_path, transcript jsonb, talk_ratio, completed bool)
call_insights   (session_id pk, primary_reason jsonb, secondary jsonb, switched_to jsonb, feature_gaps text[],
                 price_sensitivity, savable_score, savable_condition, quotes jsonb, summary)
reason_statements(id, session_id, text, embedding vector(1024), theme_id)
themes          (id, org_id, name, definition, taxonomy_code, status, created_from ('auto','human'))
theme_snapshots (theme_id, week, users, mrr_cents)
actions         (id, org_id, kind ('linear_issue','slack_alert','founder_callback','crm_note'), ref, payload, created_at)
incentives      (id, session_id, kind, status, sent_at)
audit_log       (id, actor, action, entity, at, meta)                           -- consent, deletions, exports
```
- **Privacy:** recordings in a private bucket with signed URLs. Retention is configurable (default 90 days). A delete-my-data endpoint is linked from every invite. Payment and card details are redacted from transcripts.

### 5.6 Repository layout
```
apps/
  api/        FastAPI: routers/(webhooks, invites, sessions, bolna, insights, integrations), services/, workers/, tests/
  web/        Next.js: app/(marketing), app/i/[token] (invite → web call), app/dashboard, app/settings
agents/       interviewer/{prompt.md, config.json}, sync.py (push config to Bolna via API)
research/     taxonomy.yaml, guide_compiler/, coverage_tracker/, leading_q_detector/
eval/         interviews/ (persona sims + rubric), synthesis/ (gold-coded transcripts + metrics)
supabase/     migrations/, seed.sql
docs/         this doc + history + pilot-log.md
```

---

## 6. Quality and evaluation (where our research background shows)

| What | How | Target by Oct 31 |
|---|---|---|
| **Interview quality** | 12 simulated churned-user personas (LLM-played: terse, rambling, angry, polite-but-vague, non-native English, Hinglish) run against the interviewer in text. A rubric scores goal coverage, probe depth, leading questions, talk ratio and time. A human spot-checks real calls. | Coverage ≥ 80%, leading-question rate ≤ 5%, user talk ratio ≥ 70% |
| **Extraction accuracy** | 30 real or role-played transcripts coded by both of us independently → agreement with model output | Primary-reason agreement ≥ 80% |
| **Quote faithfulness** | Word-for-word substring check (automated, every call) | **100%** |
| **Theme quality** | Compare auto-themes with our manual affinity mapping on the pilot data | ≥ 80% of the manual themes recovered |
| **Funnel** | Invite → open → start → complete, per channel | ≥ 15% of invited complete *(go/no-go, §8.1)* |
| **Latency** | End of user speech → agent audio | p50 ≤ 1.2 s |

**Added from the open-source landscape:**
- **Transcript reliability gate:** before verifying quotes, flag likely speech-to-text inventions (low-confidence spans, phrases repeated in silence, text that doesn't fit the context) and drop or re-transcribe those spans.
- **Evidence binding everywhere:** every field on an insight card and every sentence in a summary links to its source transcript turn and timestamp.
- **Synthetic end-to-end calls:** a nightly run where a scripted "churned user" line calls the interviewer, with assertions on coverage, schema and timing, and differences against the last run flagged in CI.
- **Honest funnel:** invited → reached → refused → unreached → completed. Silence is never consent.

The evals run in CI on every prompt or guide change. **Publishing our interview-quality benchmark** ("how good are AI interviewers?") is also a great launch and credibility asset.

---

## 7. Business model
- **Pricing:**
  - **Starter $199/month:** 25 completed interviews
  - **Growth $599/month:** 100 interviews, integrations, Slack/Linear
  - **Scale:** custom
  - Extra interviews at about $6–8 each
  - India pricing at about half
  - *(est.; validate with pilots)*
- **Why they'll pay:**
  - versus a human researcher (recruiting + scheduling + interviewing + coding often costs well over $100 per interview)
  - versus win-loss firms that charge hundreds per interview
  - versus the cost of fixing the wrong thing
  - One saved customer often pays for the month.
- **Cost to serve** *(est.)*: about 4 minutes of voice + LLM extraction per interview. Measure the real cost per minute on Day 0. We need **≥ 80% gross margin** at the Growth tier.
- **Go-to-market** (our home turf):
  - founder-led sales to startups we know
  - content: "We interviewed 500 churned SaaS users: the real reasons people leave"
  - a free "churn audit" (we interview 20 of your churned users for free)
  - integrations listings (Stripe App Marketplace, PostHog)
  - YC/indie-hacker communities

### Competition and how we're different
| Category | Examples | Their gap |
|---|---|---|
| Exit surveys / cancellation flows | Churnkey, ProfitWell Retain, Typeform | Checkboxes and discounts. Shallow "why", no follow-ups. |
| AI interview platforms (text/video) | Listen Labs, Outset and others [verify current players] | Built for scheduled research studies with recruited panels. Need a link, a camera and effort. Not triggered by churn or tied to revenue. |
| Product analytics | PostHog, Mixpanel, Amplitude | Shows *what* users did, never *why* |
| Win-loss services | Clozd, consultants | Expensive, human, slow, enterprise-only |

### Open-source landscape: [awesome-phone-call-agents](https://github.com/CALLE-AI/awesome-phone-call-agents) (read in full, 2026-10-18)
- **Nobody is doing real churn interviews.** The closest items:
  - *Churn-Rescue AI*: a browser simulation with no verified outcomes
  - *recover*: calls when a card payment fails, to get a retry, card update or pause. That's a dunning flow, not a "why".
  - *Tokito*: phones people who ignored a Google Form
  - *researchcall-survey*: fixed-script surveys
  
  These validate the demand and leave our gap open: adaptive interviews + revenue-weighted synthesis.
- **Patterns we'll adopt** (see §6):
  - **evidence binding**: every insight field links to the transcript turn behind it (from *relaygoal*, *asheard*, *callproof*)
  - **transcript reliability gate**: catch words the speech-to-text made up before we verify quotes
  - **synthetic test calls** run in CI (from *linecanary*, *otherend*)
  - **funnel honesty**: count answered, refused and unreached separately against everyone invited, and never treat silence as consent (from *ringedingeding*, *researchcall-survey*)
  - **consent gates**: call windows, do-not-contact list, attempt caps, tamper-evident audit log (from *callguardian*)
  - **read-back before acting** (from *one-more-story*, *verity*)
  - a pitch line against pushy retention tactics (from *call-cancellation-respect-auditor*)
- **Avoid:** recruiting screens (*hirecall*, *openline-screening*). That space is crowded.

**Our position:** event-triggered, voice-first, revenue-weighted, and closing the loop (win-back + tickets). We're the **"why" layer next to your analytics.**

---

## 8. Execution plan (team of 2, Oct 18 → Oct 31 → Nov 20)

### 8.1 The 48-hour kill test (Sat Oct 18 – Mon Oct 20)
- Before building much, **ask 3–5 startups** (from our freelance and GTM network) to lend us **50–100 churned or trial-dropped users** each, through CSV export.
- Build a minimal version: invite email → landing page → Bolna web call / "call me" → transcript.
- **Go/no-go on Tue Oct 21 evening:**
  - ✅ **Go** if ≥ 15% of invited users complete (or ≥ 25% of those who open the email start a call) **and** the founders say at least 3 insights were new to them.
  - 🟡 **Adjust** if 5–15%: test a stronger incentive, founder-voice invites, SMS, or a smaller time ask ("2 minutes").
  - ❌ **Kill** if < 5% after adjusting → pivot the same engine to **win-loss interviews** (B2B buyers who already took sales calls, so higher willingness) or to the PagerCall backup.

### 8.2 Roles
- **Person A: AI + voice.** Bolna interviewer agent, guide compiler, coverage tracker (v2), extraction, synthesis/clustering, evals.
- **Person B: Product + GTM.** Recruiting pilot startups, invite copy and funnel (our GTM strength), Stripe/CSV/PostHog triggers, dashboard, Slack/Linear integrations, demo SaaS app, pitch and video.
- **Both, every night (30 min):** listen to 5 real interviews, update `docs/pilot-log.md`, pick tomorrow's top 3 fixes.

### 8.3 Day by day
| Dates | Person A (AI + voice) | Person B (product + GTM) | Exit check |
|---|---|---|---|
| **Sat Oct 18** | Bolna account + number; spikes: Web Call SDK with per-session context, outbound on request, webhook payloads, STT/TTS choice, cost per minute | Message 8–10 startups for pilot slots; repo scaffold; Supabase + Vercel; invite email copy v1 | ≥ 3 startups said yes |
| **Sun Oct 19** | Interviewer prompt v1 + guide template; extraction v1 (JSON + quote verification) | Invite landing page `/i/[token]` → web call / "call me"; CSV import; send the **first invites** | First real interview recorded |
| **Mon Oct 20** | Fix interview issues from the first calls; persona-sim eval harness v0 | Invites to all pilot lists; funnel tracking (sent/opened/started/completed) | ≥ 10 completed interviews |
| **Tue Oct 21** | Per-call insight view; Slack per-call summary | Pilot founders review insights → collect "new to me?" feedback | **Go/no-go (§8.1)** |
| **Wed Oct 22 – Thu Oct 23** | Synthesis v1: reason statements → embeddings → clustering → theme labels → MRR weighting; audio-clip cutter | Dashboard v1 (themes, quotes, audio, savable list); Stripe webhook trigger | Themes for ≥ 1 pilot look right to its founder |
| **Fri Oct 24 – Sun Oct 26** | Custom-LLM interviewer brain with coverage tracking (v2) if evals show v1 gaps; leading-question guard; Hinglish path | Linear issue creation + Slack weekly digest; incentive delivery; 2nd wave of invites; win-back founder alert | ≥ 40 completed interviews across pilots |
| **Mon Oct 27 – Tue Oct 28** | Eval report (interview quality, extraction agreement, theme recovery); latency tuning; hardening (retries, idempotency, PII redaction) | **Pricing conversations → ≥ 1 paid pilot / LOI**; collect founder quotes; launch post draft | Metrics exported; ≥ 1 commitment |
| **Wed Oct 29 – Thu Oct 30** | Demo reliability: demo SaaS app cancel → invite → web call → live dashboard | 2-min video + written submission | **Submitted Oct 30** (Oct 31 buffer) |
| **Nov 1 – Nov 20** | Coverage brain v2 polished; win-loss mode; benchmark write-up | More pilots → paying; public launch ("500 churned users" report); interview prep; stage rehearsal with a backup recording | Finale-ready |

### 8.4 Scope cuts for 2 people
- **In v1:** CSV + Stripe triggers, email invites, web call + "call me", English (Hinglish if a pilot needs it), Slack + Linear.
- **Later:** PostHog/Segment triggers, HubSpot, SMS/WhatsApp invites, live transfer to founder, gift-card API (send incentives by hand during the pilot).

---

## 9. Success criteria for Oct 31
- [ ] ≥ 3 pilot startups, ≥ 150 invites sent, **≥ 40 completed interviews**
- [ ] Completion rate ≥ 15% of invited (or a documented, honest number plus what we learned)
- [ ] At least 1 pilot founder made or committed to a change because of ChurnCall (with a quote)
- [ ] ≥ 1 paid pilot or signed LOI
- [ ] Eval report: coverage ≥ 80%, extraction agreement ≥ 80%, quote faithfulness 100%
- [ ] Live demo path working end to end, with a backup recording
- [ ] Repo clean: README, setup, CI green

## 10. Where it goes (the venture story)
1. **Churn and trial-drop interviews** (wedge) →
2. **Every customer moment:** onboarding check-ins, NPS-detractor follow-ups, feature-launch feedback, pricing research →
3. **Win-loss for B2B sales teams** (bigger contracts, CRM-triggered) →
4. **Expert and market-research calls** for investors and consultants →
5. **The customer-voice system of record:** the largest corpus of real "why" data across software companies → benchmarks ("your onboarding churn is 2× the median for dev tools") → recommendations and automatic fixes.

## 11. Risks and mitigations
| Risk | Mitigation |
|---|---|
| Churned users won't talk to an AI | 48-hour kill test; founder-voiced invites; incentive; 2-minute option; browser one-tap; honest framing |
| Low-quality, generic insights | Research-grade guide + coverage tracker + evals; insights tied to company context; human-editable themes |
| Phone and AI-call regulation | User-initiated calls only; browser voice by default; disclosure + recording notice; opt-out; data deletion |
| Pilot startups have too few churned users | Include trial drop-offs + inactive users + back-catalogue churn from the last 90 days |
| "It's a feature of PostHog / Churnkey" | Voice interviewing + synthesis quality is the hard part; integrate *with* them (be the "why" next to their "what") |
| Voice latency / awkward turn-taking | Day-1 STT/TTS choice, tuned pause timings, short agent turns, persona-sim testing |
| Data sensitivity of the companies' customers | Per-org isolation, RLS, encryption, retention controls, DPA template |

## 12. Open items for the team
1. Names of the startups to ask (target 8–10 asks → 3–5 yeses).
2. Who's Person A and who's Person B?
3. Keep the name **ChurnCall**, or go broader now (e.g. *Exit*, *WhyLeft*, *Echo*)? Recommendation: ChurnCall for the hackathon, rebrand when we expand beyond churn.
