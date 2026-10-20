# Suggested improvements

> v1 · 2026-10-20 (evening) · Written by Pranav after the **first real end-to-end interview**, plus the improvement backlog collected while building plans 01–03.
> Evidence comes from the real call's data (`data/transcripts.jsonl`, `data/insights.jsonl`, `data/webhooks.jsonl`, which are gitignored) and from the code. Nothing here is built yet; each item says how to check the fix.
> Related: [Sarthak's plan](../build-plans/00-sarthaks-plan.md) · [build plans](../build-plans/) · [spec](CHURNCALL.md)

---

## TL;DR: do these before the pilot
| # | Improvement | Why (evidence) | Effort |
|---|---|---|---|
| 1 | **Get the Bolna trial limit lifted** (or upgrade) | Phone calls failed: *"Trial accounts can only make calls to verified phone numbers."* No real pilot user can be phoned until this is fixed | Ask Bolna / add funds |
| 2 | **Make the interviewer talk less** | User spoke only **29%** of the words (goal ≥ 70%); the AI averaged **28.7 words per turn** vs the user's **9.5**; the user interrupted it **3 times** | Prompt edit + 1 test call |
| 3 | **Strictly one question per turn, no framing** | Two double questions and one leading question in a 9-turn interview (details below) | Prompt edit |
| 4 | **Boost the product name in transcription** | "Shoplytics" came out as *shoplitics*, *shoplitex*, *shoprelix* | Agent config |
| 5 | **Remove the ngrok warning page** (paid ngrok or deploy) | Free ngrok shows every visitor an anti-phishing page first, which will hurt completion rates | Decision + ~10 min (paid) or ~2–3 h (deploy) |
| 6 | **Browser calls as the main channel** | They work on the trial account (first interview was a browser call); phone is blocked by item 1 | Already built; keep `NEXT_PUBLIC_WEB_CALL_ENABLED=true` |

---

## 1. The first real interview (2026-10-20, 8:49 PM IST)

**Setup:** invite for "Pranav" from the test company *Shoplytics* (`data/companies/test.json`), opened through the public ngrok URL. **Call me now** failed twice (trial limit), then **Talk in browser** worked.

### Timeline (from `invite_events.jsonl`, UTC)
| Time | Event |
|---|---|
| 15:18:05 | `opened`: page ran in a real browser |
| 15:18:28, 15:18:48 | "Call me now" → **502**: Bolna said *"Trial accounts can only make calls to verified phone numbers."* Logged in `errors.jsonl`; the failed attempts didn't count toward the 3-attempt limit or the funnel |
| 15:19:31 | `started_web`: our server minted a Bolna browser session |
| 15:19:37 | `web_connected`: call connected **6 s** after the tap |
| 15:22:24 | `call_ended_client` (`local-hangup`) · Bolna webhook `call-disconnected` (ignored, as designed) |
| 15:22:26 | Bolna webhook `completed` → invite marked **completed** (channel: web) → transcript stored → Groq extraction → insight stored |

### What worked
| Area | Result |
|---|---|
| Invite page → browser call | ✅ Mint, mic, connect, hang-up all fine |
| Opener | ✅ Browser version (*"thanks for joining… about three minutes… recorded"*), AI disclosure up front |
| Webhook auth | ✅ Bolna posted from `13.203.39.153` and `13.126.9.249` (its published IPs), passing our IP check through ngrok → Next.js → FastAPI without a secret header |
| Linking the call to the invite | ✅ Bolna echoes our `user_data` under **`context_details.recipient_data`** (one of the two places `bolna.call_variables()` checks) |
| Only-once handling | ✅ The `call-disconnected` webhook was saved raw and ignored; transcript stored and extraction run exactly once on `completed` |
| Extraction (Groq `openai/gpt-oss-120b`) | ✅ Reason `price_value_mismatch` with a sensible detail, missing feature *"AI analysis quality"*, `price_is_the_issue`, savable 0.2, an accurate summary; **both quotes word for word, 0 dropped** |
| Results page | ✅ `/results` and `/results/<token>` show it: funnel 1 → 1 → 1 → 1 |
| Recording | ✅ `telephony_data.recording_url` (`https://api.bolna.ai/recordings/call/<execution_id>`) forwards (307) to a **signed S3 link** (`bolna-recordings-india`) serving a FLAC file (5.4 MB, 48 kHz stereo). **Plays without our API key**, so plan 03's recording proxy (Step 6) isn't needed |
| Phone call | ❌ Trial-account restriction (see §3.1) |

### Conversation metrics
| Metric | Value | Target / note |
|---|---|---|
| Duration | 162 s (2 min 42 s) | ✅ "about 3 minutes" |
| Turns | 9 AI · 11 user | |
| Words | AI 258 · user 105 | |
| **User share of words** | **29%** (`user_talk_ratio` 0.29) | ❌ goal ≥ 70% (spec §6) |
| Avg words per turn | AI **28.7** (max 50) · user 9.5 | AI turns should be ≤ ~15 words |
| User interrupted the AI | 3 times (Bolna `interruption_stats`) | A sign the AI's turns are too long |
| AI turns with 2+ questions | 2 of 9 (one by `?` count, one joined with "and") | ❌ the prompt says never |
| Leading or framing questions | 1 | ❌ the prompt says never suggest an answer |
| LLM time to first token (gpt-4.1-mini) | median **478 ms**, max 702 ms | |
| Voice time to first audio (ElevenLabs) | median **108 ms**, max 163 ms | |
| Estimated response delay | ≈ 900 ms endpointing + 478 ms LLM + 108 ms voice ≈ **1.5 s** | Spec target p50 ≤ 1.2 s |
| Cost | **16.5** (Bolna `total_cost`; unit not confirmed, likely US cents ≈ $0.17): voice 13.91 (**84%**), transcription 2.55, LLM 0.49 | See §2.6 |

> Bolna's `interruption_stats` also reports `agent_speaking_ms: 4340` and `user_speaking_ms: 56551`. That contradicts the transcript (258 AI words is ~90 s of speech), so we don't rely on those two numbers.

---

## 2. Analysis and suggested fixes

### 2.1 The interviewer talks too much (priority: before pilot)
**Evidence:** user share 29%, AI 28.7 words per turn, 3 barge-ins. Most AI turns repeat the user's answer back *and then* ask a long question, e.g.:
> *"So the price difference compared to those other alternatives was the main trigger for you to consider cancelling. When you say those alternatives offer similar features for less, what was missing or not working well enough in Shoplytics for you day to day?"* (50 words)

**Why:** the prompt says "keep your turns to one or two sentences" *and* "mirror their words back before asking the next thing". The model does both at full length. `max_tokens: 150` doesn't constrain spoken length meaningfully.

**Fix (in `agents/interviewer/prompt.md`):**
- Hard rule: **"Each turn is at most 2 short sentences and at most 20 words. Usually just the question."**
- Mirroring becomes optional and short: *"Mirror in 3–6 words at most ('Too expensive, got it.'), then ask."*
- Lower `max_tokens` in `agents/interviewer/config.json` from 150 to ~60 as a backstop.

**Check:** one 2-minute test call → user share ≥ 60% and AI turns ≤ 20 words; or run `eval/interviews/simulate.py --persona rambler` and `--persona terse`, which report talk ratio automatically.

### 2.2 Double questions and a leading question (priority: before pilot)
**Evidence:**
- *"When did you first start thinking about cancelling? **Was there a specific moment** or experience that made you feel…"* (two questions)
- *"What do you use now instead of Shoplytics, **and what about that works better** for you?"* (two questions joined with "and")
- *"…made you feel Shoplytics was **too expensive for what it offered**?"* (frames the answer; it echoes the user's word "expensive" but adds a judgment)

**Why:** the prompt's own example lines contain double questions (*"When did you first start thinking about cancelling? What happened that day?"*), so the model copies the pattern.

**Fix:** rewrite the example questions in `prompt.md` as **single** questions, and add: *"Never add a second question, even after 'and'. Never describe their reason for them; use only their exact words."*

**Check:** `simulate.py` already counts `multi_question_turns` and `leading_questions`; both should be 0 across the 6 personas.

### 2.3 Product name misheard (priority: before pilot)
**Evidence:** transcript has *shoplitics*, *shoplitex*, *shoprelix*. Extraction still worked, but quotes show the wrong name and founders will notice.

**Fix:** Deepgram nova-3 supports boosting key terms. Add the company and product names to the transcriber config in `agents/interviewer/config.json` **[verify the exact Bolna field: `keywords` / `keyterm`]**. Since the company changes per pilot, either sync the agent per pilot company or check whether Bolna fills `{{company_name}}` in that field.

**Check:** a test call saying the product name 3 times → spelled right in `transcripts.jsonl`.

### 2.4 Extraction quality (priority: during pilot)
- ✅ Accurate on the real call and on 2 sample transcripts (about 2.4 s each), with all quotes word for word.
- **Repeated quotes:** fixed already (each quote kept once per insight).
- **Reason codes can be debatable:** a broken Shopify import was labelled `reliability_bugs` instead of `onboarding_friction` on a sample transcript. The real call had a mixed reason (price *and* AI-analysis quality): primary = price, the AI quality only showed up as a feature gap. **Suggestion:** after the first 10 pilot calls, read the reasons side by side with the transcripts; if mixed reasons keep getting flattened, ask the extractor to fill `secondary_reasons` more often.
- **Privacy:** Groq's free tier may treat data differently from a paid API. Fine for test calls and friends; **read Groq's data terms before sending a pilot startup's real customer transcripts**, or switch to a paid provider for the pilot.

### 2.5 Response speed (priority: during pilot)
Estimated ≈ 1.5 s from the user stopping to the AI starting, of which **900 ms is our endpointing setting** (how long to wait for silence before replying). That was chosen so people can pause to think.
- **Try 600–700 ms** and listen for whether the AI starts cutting people off. That saves 200–300 ms per turn.
- The LLM's ~480 ms first token is fine; the voice's 108 ms is excellent.

### 2.6 Cost (priority: before pilot, for budgeting)
- One 2.7-minute browser interview = **16.5** cost units, and **84% of that is the ElevenLabs voice**.
- If the unit is US cents (likely; **confirm with Bolna/Sarthak**), that's ≈ $0.06 per minute, and the wallet's **500** covers only **~30 calls** of this length. Plan the pilot budget, or ask Bolna for hackathon credits.
- Cheaper option: Bolna's Deepgram `aura-2` or Cartesia `sonic` voices, at the cost of voice quality. Worth an A/B listen.

### 2.7 Webhook facts we now know (record in CLAUDE.md, add a test fixture)
- `context_details = {"recipient_data": {...our user_data...}}`
- `telephony_data.provider = "web-call"` for browser calls; `call_type = "outbound"` even for browser calls
- `telephony_data.recording_url` → 307 → signed S3 FLAC (public while signed; going through Bolna's URL each time gets a fresh link)
- Also sent: `latency_data` (per-turn LLM/voice/transcriber latency), `cost_breakdown`, `usage_breakdown`, `interruption_stats`
- **To do:** copy this webhook into `apps/api/tests/fixtures/bolna_completed.json` (it contains no phone number for a browser call) and add a test that runs it through `webhooks.handle_bolna_webhook` and `results.invite_detail` (plan 03 Step 6).

---

## 3. Pilot blockers and risks

| # | Item | Status | Suggested action |
|---|---|---|---|
| 3.1 | **Phone calls blocked by the trial account** | ❌ Confirmed by the real attempt | For tests: verify our numbers in the Bolna dashboard. For the pilot: lift the trial limit or upgrade, or run the pilot **browser-first** (works today) |
| 3.2 | **Phone number on the account / which countries** | ❓ None listed | Ask Bolna (`docs/BOLNA_QUESTIONS.md` #2) |
| 3.3 | **Max 2 concurrent calls** | ⚠️ From the account API | A third person tapping at the same time gets "busy, use Call me now". Ask Bolna to raise it before waves of invites |
| 3.4 | **ngrok warning page** | ⚠️ Free plan | Paid ngrok for the pilot week, or deploy |
| 3.5 | **Laptop must stay on** for days of live invites | ⚠️ | `caffeinate -dis`, or deploy (Vercel for the web app + Fly/Railway for the API) to remove the dependency |
| 3.6 | **Wallet size vs cost per call** | ⚠️ 500 units, ~16.5 per call | Confirm the unit; top up or get credits (§2.6) |

---

## 4. Improvement backlog (beyond the first call)

### Interview quality
| Priority | Improvement | Check |
|---|---|---|
| P0 | §2.1–2.3 (shorter turns, one question, no framing, product-name boost) | Test call + `simulate.py` metrics |
| P1 | Run `simulate.py` on all 6 personas after each prompt change (terse, rambler, price cover story, angry, vague, Hinglish) and keep a small score table | Talk ratio, leading questions, double questions |
| P1 | Indian English voice for Indian pilots (the account has several, e.g. "Raju – Natural Conversationalist", "Anika", "Aakash Aryan") | A/B listen |
| P2 | Shorter version (2 min) for people coming straight from a cancel page (plan 04 demo) | Completion rate by entry point |

### Measurement (the go/no-go numbers)
| Priority | Improvement | Note |
|---|---|---|
| ✅ done | Browser "started" counts only once the call connects | Fixed today |
| P1 | Record **when each invite email was actually sent** (mail merge happens outside our system) | Otherwise "invited" counts rows, not sent emails |
| P1 | Track **days since cancellation** at invite time, to see whether reaching out sooner helps | Add a `cancelled_at` CSV column |
| P2 | Show response time and talk ratio per call on `/results` (from `latency_data` + `user_talk_ratio`) | Helps the evening review in Sarthak's plan Step 13 |

### Reliability and operations
| Priority | Improvement | Note |
|---|---|---|
| P0 | Remove the laptop + free-ngrok dependency (§3.4–3.5) | |
| P1 | Standard Python `logging` with the call ID on every line (today errors only go to `errors.jsonl`) | Faster debugging of live calls |
| P2 | Extraction in a job queue instead of the web process | Only matters at higher volume |

### Privacy and trust
| Priority | Improvement | Note |
|---|---|---|
| P1 | A real **"delete my data"** path (an admin action or automatic retention), since the page promises it | Today it's "reply to the email" |
| P1 | Recording links are public while signed (anyone with the forwarded S3 link can listen) | Keep them on the password-protected `/results` page only; don't paste them in reports |
| P1 | Groq data terms before real pilot transcripts (§2.4) | |

### Results page
| Priority | Improvement | Note |
|---|---|---|
| P1 | CSV export (plan 03 Step 7) for founder reports | |
| P2 | Per-call cost and latency on the detail page | Data already in the webhook |

### Technical debt (low priority)
- Tests each set up their own data folder; share one fixture.
- `npm audit`: moderate `postcss` advisory in Next 15.5 (fixed by a Next upgrade; production only).
- No automated browser test for the invite page; add one end-to-end test before the demo.

---

## Appendix: transcript of the first interview
*(Test persona: Pranav playing a churned Shoplytics user. Spelling as transcribed.)*

> **AI:** Hi Pranav, thanks for joining. I'm an AI assistant helping Priya at Shoplytics. You recently cancelled, and Priya would really value your honest take on what didn't work. It takes about three minutes, and this conversation is recorded so the team can learn from it. Is now a good time?
> **User:** yes
> **AI:** Great! Take me back to when you first signed up. What were you hoping Shoplytics would do for your online store?
> **User:** so basically · i thought shoplitics would help me · analyze and find winning products but currently i found that shoplitex is too expensive to do that
> **AI:** Thanks for sharing that. When did you first start thinking about cancelling? Was there a specific moment or experience that made you feel Shoplytics was too expensive for what it offered?
> **User:** so basically there are alternatives that i cannot name that basically offer this for two dollars cheaper so i decided to cancel shoprelix
> **AI:** So the price difference compared to those other alternatives was the main trigger for you to consider cancelling. When you say those alternatives offer similar features for less, what was missing or not working well enough in Shoplytics for you day to day?
> **User:** was it shop letting basically says that their core usps ai analysis i found their ai analysis was not good enough their competitors did it better and i also learned more about · where i went wrong with the competitor's product
> **AI:** So the AI analysis in Shoplytics didn't meet your expectations compared to competitors, and you felt their insights were more helpful. Can you tell me more about what specifically didn't work well with Shoplytics' AI analysis?
> **User:** no
> **AI:** If a friend asked you whether to use Shoplytics, what would you tell them?
> **User:** no
> **AI:** Thanks for being honest. What do you use now instead of Shoplytics, and what about that works better for you?
> **User:** i cannot talk about that right now can we end this call now
> **AI:** Of course, Pranav. Thank you, this is genuinely useful. As a thank-you, a $5 Amazon voucher is on its way. Priya reads every one of these. Is there anything else you'd want Priya to know?
> **User:** no
> **AI:** Thanks again, Pranav. Have a great day! Goodbye.
