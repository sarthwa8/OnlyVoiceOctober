# CareCall + Kavach: Build Document & Execution Plan

> v0.1 · 2026-10-18 · Status: **awaiting approval** · Why this idea: [DECISION.md](DECISION.md)
> Anything marked **[verify]** is a Bolna/vendor behaviour we must confirm in the docs or by testing before relying on it.

---

## 0. Goals and success criteria

### By Oct 31 (submission)
| Metric | Target |
|---|---|
| Real parents onboarded (not teammates acting) | **≥ 15** |
| Real check-in calls completed | **≥ 150** |
| Answer rate (calls picked up / attempted) | ≥ 70% |
| Families who'd pay (pre-paid ₹99 "founding family" or written intent) | **≥ 5** |
| Kavach on the scam eval set (offline) | recall ≥ 0.9 on scams, false-alarm rate ≤ 10% on benign calls |
| Kavach live role-play calls (merged) | ≥ 10, with time-to-warning measured |
| Voice latency (end of user speech → first agent audio), check-in agent | p50 ≤ 1.5 s |
| 2-min demo video + written submission | Done by **Oct 30** (1-day buffer) |

### By Nov 20 (finale)
Pilot still running (retention curve), 25–40 parents, Kavach+ classifier v1, a rehearsed live stage demo, and the interview deck.

### Non-goals (for now)
No medical advice or diagnosis. No parent-side app. No payments inside calls. No Haath browser agent before Oct 31.

---

## 1. Users and core flows

### Personas
- **Parent ("Amma", 62–85):** lives alone or with a spouse in Chandigarh/Mohali/Ludhiana or a smaller town. Speaks Hindi/Punjabi, some English. Has a basic Android or feature phone. Takes 3–8 medicines.
- **Child ("Rahul", 28–45):** in Bengaluru, Gurgaon or abroad. Busy and guilty. Pays. Wants to know "is Mom OK today?" in five seconds.

### Flow A: Onboarding (child, ~3 min on a web form)
1. Child enters their name, WhatsApp, relation; parent's name, honorific (Mummy/Papa ji/Biji/Amma), phone, language, preferred call time(s), and interests (bhajans, cricket, grandchildren's names).
2. Medicines: name, the *nickname the parent uses* ("BP wali choti goli", the small BP pill), and time slot.
3. Emergency contacts (ordered), plus a toggle for 112/1930 guidance.
4. Consent checkboxes (child). The parent's consent is captured verbally on the first call.
5. On submit, CareCall places an **intro call** to the parent within 1 minute. It introduces itself, asks for consent, teaches the parent to save the number as "Kavach", and runs a **merge drill**: "If anyone calls saying they're police or a bank, press Add Call and call me."

### Flow B: Daily check-in (outbound, ~3 min)
```
greet by honorific + memory hook ("Kal aapne bataya tha ghutne mein dard tha, ab kaisa hai?" — yesterday you said your knee hurt, how is it now?)
→ how are you feeling (mood 1–5, inferred)
→ medicines for this slot, by nickname ("BP wali goli li?" — did you take the BP pill?) → yes / no / later
→ symptom screen (dizziness, chest pain, breathlessness, fall, fever, not eating/sleeping)
→ scam screen ("Aaj koi anjaan call aaya? Kisi ne OTP, paise ya police ki baat ki?" — any unknown call today? did anyone mention an OTP, money or the police?)
→ 1–2 min companionship (interests, family news supplied by the child)
→ close + reminder ("Shaam ki dawai 8 baje" — evening medicine at 8)
```
- **Red flag mid-call** (chest pain, fall, can't breathe, confusion): the agent stays calm, says it is connecting the child now, **transfers** to emergency contact #1 [verify transfer tool], and the backend fires an urgent alert in parallel. If the transfer fails, the agent tells the parent to call 112 and repeats the number.
- **No answer:** 2 retries 15 minutes apart. Two consecutive missed check-ins trigger a "couldn't reach Mom" alert to the child.

### Flow C: Kavach live (inbound, merged call)
1. A suspicious call arrives. The parent taps *Add call → Kavach → Merge*.
2. Bolna answers. The caller ID is the parent's number, so we identify the family [verify CLI on conference legs].
3. **Welcome (spoken immediately):** *"Kavach family suraksha line jud gayi hai. Yeh call record ho rahi hai."* ("Kavach family safety line has joined. This call is being recorded.") This is both consent and a deterrent.
4. Kavach **stays silent** while our custom LLM endpoint scores each transcript turn.
5. When risk crosses the threshold, Kavach **speaks to the parent by honorific**: *"Mummy ji, main Kavach hoon. Police ya CBI kabhi phone ya video call par arrest nahi karti, na paise maangti hai. Yeh fraud hai. Abhi phone kaat dijiye. Main Rahul ko bata raha hoon."* ("Mummy ji, this is Kavach. Police or CBI never arrest anyone over a phone or video call, and they never ask for money. This is fraud. Please hang up now. I'm telling Rahul.") Optionally it then addresses the caller: "This call is being reported to 1930."
6. The backend sends the family a WhatsApp message with the risk score, scam type, impersonated agency, amount demanded, the scammer's number if captured, and a transcript snippet. If enabled, it also places a voice-alert call to the child.
7. After the call: a summary, plus "what to do now" (call your bank, 1930, cybercrime.gov.in) sent to the child.

### Flow D: Kavach "afterwards" (inbound, parent alone)
The parent calls Kavach after a scary call: "Mujhe ek call aaya tha…" ("I got a call…"). Same number, same endpoint. The endpoint detects that the speaker is addressing Kavach directly and switches to **counsel mode**. It asks what happened, compares it with the playbook (and web search **[verify tool in custom-LLM mode]**), and gives a clear verdict and next steps. It alerts the family if money moved or an OTP was shared.

### Flow E: Family dashboard (child, web/mobile)
A "Today" card (✅ called · mood · meds ✓/✗ · flags), a 14-day mood and adherence grid, a timeline with summaries, recordings and transcripts, alerts with acknowledgement, the Kavach events list, and settings (meds, times, contacts).

---

## 2. System architecture

```
                         ┌──────────────────────────── Bolna ─────────────────────────────┐
 Parent's phone ◄──PSTN──┤  Agent 1: carecall-checkin (outbound, Bolna-hosted LLM)        │
                         │  Agent 2: kavach (inbound number, CUSTOM LLM → our API)        │
                         │  Sarvam saaras v4 STT (keyword bias) · Bulbul v4 TTS            │
                         └───────┬───────────────▲───────────────┬────────────────────────┘
                     exec webhooks│   POST /call   │ OpenAI-style  │ tool/function calls
                                 ▼   (user_data)   │ /chat/completions (SSE)
 ┌──────────────────────────── apps/api (FastAPI, Python 3.12) ────────────────────────────┐
 │ scheduler (APScheduler, 1-min tick) → dial due check-ins, retries                       │
 │ /bolna/webhook → store transcript + extraction → rules engine → alerts                  │
 │ /v1/chat/completions → Kavach gate: redact → rule scorer → LLM classifier → speak/silent│
 │ /tools/* → mid-call functions (urgent_alert, log_med)                                   │
 │ alerts: WhatsApp (Twilio/Meta) · Telegram bot · voice-alert call via Bolna              │
 └───────┬─────────────────────────────────────────────────────────────────────────────────┘
         │ supabase-py (service role)
 ┌───────▼──────────────┐      realtime + RLS      ┌──────────── apps/web (Next.js 15) ─────┐
 │ Supabase Postgres    │ ◄──────────────────────► │ landing · onboarding · family dashboard │
 │ + Storage (records)  │                          │ · ops console (us)  — Vercel            │
 └──────────────────────┘                          └─────────────────────────────────────────┘
```

### Stack decisions
| Layer | Choice | Why |
|---|---|---|
| Voice orchestration | **Bolna** | Required by the hackathon. Telephony + STT/TTS + turn-taking. |
| STT | **Sarvam saaras v4**, keyword biasing | Best Hindi/Punjabi/Hinglish. Bias for med names and scam terms. Deepgram as A/B fallback. |
| TTS | **Sarvam Bulbul v4 Flash** | Natural code-mixed voice, low latency. A warm, slower voice for elders. |
| Check-in LLM | Bolna-hosted fast model (e.g. GPT-4.1-mini class) | Lowest latency, no infra. Decide on Day 1 from latency + Hindi quality. |
| Kavach LLM | **Our OpenAI-compatible endpoint**, inner call to a fast classifier model | We need control over *when to speak*, plus server-side side effects. |
| Backend | **FastAPI** + APScheduler, on Render/Fly in an India or Singapore region | Python for the ML path (Kavach+). Region close to Bolna to cut custom-LLM latency. |
| DB | **Supabase** (Postgres, Auth via magic link/OTP, Realtime, Storage) | Realtime dashboard for free. RLS per family. |
| Web | **Next.js 15 + Tailwind + shadcn/ui** on Vercel, Recharts for trends | Fast to build, mobile-first. |
| Alerts | WhatsApp (Twilio sandbox or Meta Cloud API test number), **Telegram bot** fallback, **voice-alert call** via Bolna | Indian SMS needs DLT registration, so avoid it for the pilot. |
| Observability | Structured logs + a `call_events` table + an ops page, Sentry free tier | We need to debug calls fast. |

**Why our own scheduler instead of Bolna Workflows/Campaigns:** each call needs fresh per-parent context (last 3 summaries, today's meds slot, family news), different times per parent, and custom retry rules. Our scheduler calls Bolna's call API with `user_data`. If Bolna campaigns support per-recipient dynamic variables and webhooks well [verify], we can show them in the pitch for the scale story.

---

## 3. Bolna agent specifications

Agent configs and prompts live in the repo (`agents/`) and are pushed through the Bolna API or MCP by a script. **The dashboard is never the source of truth.**

### 3.1 Agent `carecall-checkin`
- **Type:** single-prompt agent. Use a graph agent only if evals show the model skipping the meds or symptom steps.
- **Language:** `agent_language` from `parents.language`. Allow switching (Hindi⇄Punjabi⇄English).
- **Voice settings:** slightly slower speaking rate. Generous end-of-speech timeout (elders pause mid-sentence). Interruptions enabled. Long silence timeout before hangup (~20 s) with a gentle "Aap sun rahe hain?" ("Are you still there?") re-prompt.
- **Keyword biasing:** the parent's med names and nicknames, family names, and common symptoms (chakkar/dizziness, saans/breath, seene mein dard/chest pain, gir gaye/fell).
- **Injected `user_data` per call:** `honorific, parent_name, slot, meds_for_slot[], recent_summaries[3], open_followups[], family_news[], interests[], emergency_contact_name, call_kind (intro|checkin)`.
- **Prompt skeleton** (`agents/carecall-checkin/prompt.md`):
  - *Identity:* a warm, respectful companion from the family's care service. **Always discloses it's an AI assistant** on the intro call, and whenever asked.
  - *Must-cover checklist:* mood → each med in `meds_for_slot` → symptom screen → scam screen → close. Companionship comes after the checklist, max ~2 minutes.
  - *Hard rules:* never give medical advice or dose changes. On red flags, call `urgent_alert` and say it is calling the contact. Never ask for OTPs, bank details or Aadhaar. Keep sentences short, use one question at a time, and match the parent's language.
- **Tools:** `urgent_alert(reason, severity)` → `/tools/urgent_alert`. Call transfer to `emergency_contact_phone` [verify per-call dynamic transfer number].
- **Post-call extraction schema** (Bolna extraction [verify JSON schema support], otherwise our own LLM pass over the transcript in the webhook):
```json
{
  "reached": true,
  "consent_given": true,
  "mood": 1-5,
  "meds": [{"med_id": "uuid", "status": "taken|missed|later|unknown"}],
  "symptoms": ["dizziness", "knee_pain"],
  "red_flags": ["chest_pain|fall|breathlessness|confusion|none"],
  "scam_mention": {"present": false, "details": ""},
  "followups": ["asked to remind about eye checkup Friday"],
  "summary_en": "2 lines for the child",
  "summary_native": "2 lines in parent's language"
}
```

### 3.2 Agent `kavach` (inbound)
- **Number:** a dedicated inbound number (Bolna/Plivo/Exotel, Indian DID).
- **LLM:** **custom** → `https://api.<domain>/v1/chat/completions` (OpenAI-compatible, streaming). Bolna sends the conversation so far, and our server decides what is said.
- **Welcome message:** the fixed announcement (Flow C step 3), localised by caller → family → language lookup. Unknown caller → Hindi + English.
- **Voice settings:** interruptions **off** for Kavach's warning (it must finish). Very long silence timeout (calls can last 30+ min) [verify max]. VAD tuned for a two-speaker channel.
- **Keyword biasing:** CBI, ED, TRAI, RBI, customs, FedEx/DHL/parcel, Aadhaar, PAN, "money laundering", "digital arrest", "arrest warrant", narcotics/drugs, "video call", Skype, AnyDesk/TeamViewer, "verification account", "safe account", OTP, "don't tell anyone".
- **Knowledge base:** `kb/scam_playbook.md` (scam families, tell-tale lines in Hindi/English/Punjabi, official facts like "no agency arrests over video call", next steps, helpline 1930 / cybercrime.gov.in). It is used by *our* classifier prompt, and uploaded to the Bolna KB too for the counsel mode.

---

## 4. Kavach detection design (the part that makes or breaks the demo)

### 4.1 Request handling in `/v1/chat/completions`
```
on request(messages, call_meta):
  turn = last user message (both speakers arrive as "user" on a merged leg)
  redact(turn)                         # mask 4–12 digit runs (OTP/Aadhaar/account)
  state = session[call_id]             # rolling transcript, scores, mode, spoke_at
  mode = detect_mode(state)            # "guard" (merged, 2 voices) vs "counsel" (parent addressing Kavach)
  if mode == counsel: stream LLM counsel answer (playbook-grounded); return
  r = rule_score(turn, state)          # weighted lexicon, Devanagari + romanised, ~1 ms
  l = cached/async llm_classify(state) # fast model, JSON {risk, scam_type, agency, amount, evidence}, ≤ 700 ms budget
  risk = combine(r, l, history)        # EMA across turns; hard triggers bypass
  if should_speak(risk, state): 
       fire alert_family(...) async; stream localized warning; mark spoke_at
  else: return SILENCE                 # see 4.4 for what "silence" means on Bolna
```

### 4.2 Signals
- **Hard triggers** (speak immediately once an authority claim is also present): a money transfer to a "verification/safe account", screen-share apps (AnyDesk/TeamViewer), "don't disconnect/don't tell family", a request to switch to a Skype/WhatsApp video call, an arrest-warrant threat, a request for OTP/PIN.
- **Soft signals:** agency claims (CBI/ED/TRAI/RBI/customs/police/courier), Aadhaar/SIM "misuse", a parcel with drugs, "your number will be disconnected in 2 hours", urgency and fear language, a monologue-heavy caller.
- **Benign guards:** a known family number in the conference, genuine bank-call patterns (no money movement, no OTP), deliveries asking for the address only.

### 4.3 Offline evaluation (before trusting it live)
- `eval/kavach/`: **40 scam transcripts** (written from I4C/RBI advisories and news cases, in Hindi, Hinglish, Punjabi and English) and **40 benign transcripts** (genuine bank, relatives, delivery, doctor's office, telemarketing). Stored as turn lists.
- A script replays each through the endpoint turn by turn. It reports recall, false-alarm rate and **turns-to-detection** (target: by turn 4 of the scammer's pitch).
- Run in CI on every prompt or lexicon change.

### 4.4 The "stay silent" fallback ladder (Day-0 spike decides)
| Rung | Mechanism | If it fails… |
|---|---|---|
| 1 | Endpoint returns an empty completion → Bolna speaks nothing | go to 2 |
| 2 | Return a minimal no-op token Bolna drops (e.g. whitespace / a configured ignore token) [verify] | go to 3 |
| 3 | Return a tiny backchannel ("hmm") rate-limited to once per 45 s; still a visible presence | go to 4 |
| 4 | **Announce-only Kavach:** speak the welcome plus a fixed advisory every ~60 s ("Yaad rakhiye, koi bhi agency phone par paise nahi maangti" — remember, no agency asks for money over the phone), with alerts from transcripts | the demo still works, and the announcement alone deters |
| 5 | Merge unsupported entirely → Flow D (call afterwards) + check-in scam screen only | pitch as roadmap: "telco-level Kavach" |

---

## 5. Data model (Supabase / Postgres)

```sql
families        (id uuid pk, name, plan text default 'pilot', created_at)
caregivers      (id, family_id fk, auth_user_id, name, phone, whatsapp, telegram_chat_id,
                 relation, priority int, wants_voice_alerts bool)
parents         (id, family_id fk, name, honorific, phone unique, language, tz default 'Asia/Kolkata',
                 checkin_times time[], interests text[], conditions text[], family_news text,
                 consent_verbal_at timestamptz, kavach_enabled bool, active bool)
medications     (id, parent_id fk, name, nickname, dose, slot text check (slot in ('morning','afternoon','night')), active)
calls           (id, parent_id fk, kind text check (kind in ('intro','checkin','kavach','kavach_after','alert')),
                 bolna_execution_id unique, status, attempt int, scheduled_for, started_at, ended_at,
                 duration_s, recording_path, transcript jsonb, summary_en, summary_native, latency_p50_ms)
checkin_results (call_id pk fk, mood int, meds jsonb, symptoms text[], red_flags text[],
                 scam_mention jsonb, followups text[])
scam_events     (id, call_id fk, parent_id fk, risk numeric, scam_type, agency, amount_demanded,
                 scammer_number, evidence jsonb, spoke_at, outcome)
alerts          (id, family_id, parent_id, call_id, type, severity, channel, payload jsonb,
                 sent_at, delivered bool, acked_at, acked_by)
audit_log       (id, actor, action, entity, entity_id, at, meta jsonb)   -- consents, data access
```
RLS: caregivers see only rows where `family_id` matches their own. The API uses the service role. Recordings go in a private bucket with signed URLs and **30-day retention**.

---

## 6. Backend API surface (`apps/api`)

| Method & path | Purpose |
|---|---|
| `POST /onboarding` | Create family, caregiver, parent, meds; schedule intro call |
| `POST /bolna/webhook` | Execution status/transcript/extraction → upsert `calls`, run post-call extraction if needed → rules → alerts. Idempotent on `execution_id`. |
| `POST /v1/chat/completions` | Kavach custom LLM (SSE streaming, OpenAI schema) |
| `POST /tools/urgent_alert` | Mid-call function from check-in agent |
| `POST /calls/{parent_id}/now` | "Call Mom now" button (dashboard / demo) |
| `POST /alerts/{id}/ack` | Child acknowledges |
| `POST /telegram/webhook` | Link a caregiver's Telegram, ack via button |
| `GET /healthz`, `GET /ops/metrics` | Health + pilot metrics for the submission |

**Rules engine (v1, plain Python):**
- `red_flags ≠ none` → URGENT (voice call + WhatsApp + Telegram)
- same med missed 2 slots in a row → WARN
- mood ≤ 2 two days running → WARN
- 2 consecutive unreachable check-ins → WARN
- `scam_mention.present` → WARN, plus a Kavach guidance message to the child
- Kavach intervention → URGENT

**Security:** shared-secret header plus an IP allow-list on Bolna-facing routes [verify Bolna webhook signing]. Secrets via env. No PII in logs (phone numbers hashed).

---

## 7. Repository layout

```
OnlyVoiceOctober/
├─ apps/
│  ├─ api/            FastAPI: routers/, services/{bolna,scheduler,alerts,kavach,rules}, tests/
│  └─ web/            Next.js: app/(marketing), app/onboard, app/dashboard, app/ops
├─ agents/
│  ├─ carecall-checkin/{prompt.md, config.json}
│  ├─ kavach/{config.json, welcome.json}
│  └─ sync.py         push configs to Bolna via API (idempotent)
├─ kb/                scam_playbook.md, lexicon.yaml (hi/pa/en, Devanagari + romanised)
├─ eval/
│  ├─ kavach/         scam & benign transcripts + replay.py
│  └─ checkin/        simulated parent personas + rubric (LLM-judge) for prompt regressions
├─ supabase/          migrations/, seed.sql
├─ docs/              DECISION.md, BUILD_PLAN.md, research/, pitch/
└─ .github/workflows/ ci.yml (lint, typecheck, pytest, kavach eval)
```

---

## 8. Execution plan, day by day

Assumes a team of 2–4: **V** = voice/agents, **B** = backend, **F** = frontend, **O** = users/ops/pitch. A solo builder follows the same order, with the ✂️ items cut.

### Phase 0: Spikes & setup (Sat Oct 18 – Sun Oct 19) → **Gate on Mon Oct 20, 10:00**
| # | Task | Owner | Done when |
|---|---|---|---|
| 0.1 | Bolna account, credits ask on Builders Slack, apply form submitted | O | Credits confirmed |
| 0.2 | Indian inbound number live (Bolna/Plivo/Exotel). Outbound to an Indian mobile works. | V | Two test calls logged |
| 0.3 | **Spike T1: merged call.** Parent phone calls a friend, then adds the Kavach number. Does Bolna hear *both* voices? What's the STT quality on conference audio? What's the caller ID? | V | Recording + transcript reviewed |
| 0.4 | **Spike T2: silence.** Minimal custom-LLM endpoint (ngrok) returning empty / whitespace / text. Does Bolna stay quiet? Does it hang up on silence? Max call length? | V+B | Ladder rung chosen (§4.4) |
| 0.5 | **Spike T3: elderly voice quality.** 3 real elders, 5-minute Hindi/Punjabi chat with a draft check-in prompt. Compare Sarvam vs Deepgram STT, and the TTS voice. | V+O | Stack picked, latency measured |
| 0.6 | **Spike T4: outbound `user_data` + webhook payload + extraction format** | B | Sample payloads saved to `apps/api/tests/fixtures/` |
| 0.7 | **Spike T5: cost.** Per-minute all-in cost from 0.2–0.5 → unit-economics sheet | O | ₹/call known |
| 0.8 | Recruit pilot list: 25 parents (team families, PG/college friends' parents, RWA/gurudwara/temple senior groups) | O | Names + consent to be called |
| 0.9 | Repo scaffold, Supabase project, Vercel + Render projects, CI skeleton | B+F | `main` deploys a hello-world |

**Gate decision (Oct 20):**
- T3 fails (elders can't be understood) → switch to **Awaaz Research**. Unlikely.
- T1/T2 fail → Kavach drops to rung 4/5. CareCall continues unchanged.
- All pass → full plan.

### Phase 1: CareCall core (Mon Oct 20 – Tue Oct 21)
- **V:** check-in prompt v1 + `agents/sync.py`; keyword biasing; red-flag `urgent_alert` tool.
- **B:** DB migrations; `/onboarding`; scheduler + retries; `/bolna/webhook` → `calls` + `checkin_results` (post-call LLM extraction if Bolna's isn't enough).
- **F:** onboarding form (mobile-first, Hindi/English UI).
- **O:** onboard the **first 5 real parents** by Tue night. Listen to every recording.
- ✅ *Exit:* 5 parents get a real daily call; transcripts + extraction land in the DB.

### Phase 2: Family value (Wed Oct 22 – Thu Oct 23)
- **B:** rules engine; WhatsApp + Telegram alerts; voice-alert call to the child; alert ack.
- **F:** dashboard v1 (Today card, timeline, recording player, alerts).
- **V:** prompt v2 from real transcripts (pacing, honorifics, Punjabi switching, memory hooks); check-in eval personas.
- **O:** reach **12 parents**; collect child feedback after 2 days.
- ✅ *Exit:* a child receives a real alert from a real call and opens the dashboard.

### Phase 3: Kavach (Fri Oct 24 – Sun Oct 26)
- **V+B:** `/v1/chat/completions` gate (redaction, rule scorer, LLM classifier, combine, chosen silence rung); localised warnings; `scam_events`; family alert.
- **V:** `kb/scam_playbook.md` + `lexicon.yaml`; 40+40 eval transcripts; `replay.py` in CI; counsel mode (Flow D).
- **F:** Kavach events page; intro-call merge drill copy.
- **O:** **10 live role-play merged calls** (teammate "CBI officer" → real phones); reach **20 parents**; ask families for "founding family" ₹99 pre-pay.
- ✅ *Exit:* eval targets met (§0). A live merged call triggers a warning plus WhatsApp in under ~10 s from the hard trigger.

### Phase 4: Hardening & proof (Mon Oct 27 – Tue Oct 28)
- Fix the top 10 issues from transcripts (mishearings, over-long calls, missed meds questions).
- Idempotency, retry/backoff, timezone checks, webhook replay tool, Sentry.
- `/ops/metrics` + an ops page: calls, answer rate, durations, adherence, alerts, latency p50/p95, Kavach eval scores.
- Weekly voice digest to the child (✂️ if solo).
- Security pass: RLS tests, secret scan, PII-in-logs check, retention job.

### Phase 5: Submission (Wed Oct 29 – Thu Oct 30) → **submit Oct 30, buffer Oct 31**
- **Demo video (2 min).** Script in §10. Record real calls with families' permission; blur numbers.
- Written submission: problem → product → real pilot numbers → Bolna features used → business model → what's next.
- Answer "Since when have you been working on this?" honestly with commit history and the pilot timeline.

### Phase 6: Shortlist → finale (Nov 1 – Nov 20)
- Keep the pilot running daily and track the **retention curve** (the YC question).
- **Kavach+:** fine-tuned scam-script classifier on our own transcripts; cloned-voice detection research spike (phone-band audio).
- Interview prep (Nov 5–7): architecture walk-through, latency numbers, failure stories, unit economics.
- Stage demo rehearsal with a **backup recording** in case venue telephony fails.
- Optional: Haath (phone-in chores) prototype on 1 portal, only if everything else is solid.

---

## 9. Testing & quality

| Layer | How |
|---|---|
| Unit | pytest: rules engine, redaction, rule scorer, scheduler due-time math (IST), webhook idempotency |
| Contract | Saved Bolna payload fixtures from Spike T4 → webhook parser tests |
| Kavach | `eval/kavach/replay.py`: recall / false-alarm / turns-to-detect, run in CI; fails the build below thresholds |
| Check-in | Simulated parent personas (LLM-played, text) + LLM-judge rubric: covered all meds? asked symptoms? no medical advice? language match? |
| Live | Daily review of 5 random real recordings (O), plus an issue log in `docs/pilot-log.md` |
| Latency | Per-call p50/p95 time-to-first-audio from Bolna metadata [verify], plus our endpoint's own timing |

---

## 10. Demo script (2-minute video, also the stage base)

1. **0:00–0:15 Hook:** a news headline ("Retired professor loses ₹1.2 cr to 'digital arrest'"), then: "Our parents are alone with these calls."
2. **0:15–0:50 CareCall:** a real morning call (Punjabi/Hindi, subtitled). "BP wali goli li?" ("Did you take the BP pill?") Mom mentions dizziness. Cut to the son's phone: WhatsApp alert, then the dashboard Today card turns amber.
3. **0:50–1:30 Kavach:** a "CBI officer" calls Mom. She taps Add call → Kavach → Merge. Kavach announces itself. The scammer pushes "Aadhaar money laundering… transfer to verification account". Kavach cuts in: "Mummy ji, yeh fraud hai…" ("Mummy ji, this is fraud…"). The son's phone rings with a voice alert, and WhatsApp shows the scam card.
4. **1:30–1:50 Proof:** pilot numbers (parents, calls, answer rate, alerts that mattered, families paying) and one real quote from a child.
5. **1:50–2:00 Ask:** "₹999/month. Any phone, any language. Built on Bolna."

---

## 11. Risks & mitigations (engineering view)

| Risk | Mitigation | Owner |
|---|---|---|
| Merged-call behaviour (T1/T2) | Spike Day 0, fallback ladder §4.4 | V |
| Custom-LLM latency → Kavach speaks too late | Silent turns return in < 50 ms. Classifier async with a budget. Hard triggers via rules (no LLM wait). Host near Bolna. | B |
| Elderly ASR errors (accent, dentures, TV in background) | Sarvam + keyword bias, slower pacing, confirm critical answers ("Matlab dawai le li, sahi?" — so you took the medicine, right?) | V |
| Agent skips meds or rambles | Checklist in prompt + check-in eval; graph agent fallback | V |
| Wrong-person pick-up / pocket dial | Verify by honorific + name at greeting; abort gracefully | V |
| Alert fatigue | Severity tiers, daily digest for non-urgent items, ack loop | B |
| WhatsApp sandbox limits (opt-in, recipient caps) | Telegram fallback, voice alerts | B |
| Costs exceed credits | Track ₹/day on the ops page; cap check-in to 4 min; 1 call/day default | O |
| Single point of failure: scheduler on one instance | Persist jobs in DB, scheduler reads `calls.scheduled_for`; restart-safe | B |
| Consent / DPDP | Recorded verbal consent, audit_log, 30-day retention, delete-my-data button | O |

---

## 12. Budget (estimate, finalise after Spike T5)
- Voice minutes: ~20 parents × 1 call/day × ~3.5 min × 13 days ≈ **~900 min**, plus ~200 min of Kavach and testing. Price from Bolna's rates once measured.
- LLM (classifier + post-call extraction): a few hundred ₹.
- Infra: free tiers (Supabase, Vercel, Render starter ≈ $7), plus domain ≈ ₹800.
- Numbers: 1 Indian DID (rental per vendor).

---

## 13. Definition of done for the Oct 31 submission
- [ ] ≥ 15 real parents, ≥ 150 real check-in calls, metrics exported from `/ops/metrics`
- [ ] At least one real, valuable alert story (with permission)
- [ ] Kavach working on live merged calls (or rung 4/5, honestly described), eval report attached
- [ ] Dashboard live on a public URL with a demo family
- [ ] ≥ 5 families pre-paid or committed in writing
- [ ] 2-min video + written submission sent by Oct 30
- [ ] Repo clean: README, setup steps, CI green
