# Koji and Perspective AI teardown: what to copy, what to beat

> 2026-10-18 · Built from their public docs, pricing pages and embed SDK reference, **not hands-on use** (🟡 vendor claims).
> Still to do: the 30-minute hands-on test in the action plan (now [Sarthak's plan](../../build-plans/00-sarthaks-plan.md)) (go through each as a churned user, keep DevTools → Network open, and screenshot every screen).
> Related: [ChurnCall spec](../CHURNCALL.md) · [evidence §6](churncall-evidence.md)

---

## 1. How each one actually works

### Koji (koji.so)
| Part | Mechanics |
|---|---|
| **Setup** | Chat with an "AI consultant" → it writes an interview brief. 8 methodologies built in (Mom Test, JTBD, etc.). "Company context" is stored once and reused. |
| **Guide controls** | Each question has a **follow-up depth: None or 1–3**, plus optional custom probe guidance. Separate **"Topics to explore"**, **opening/closing approach**, and a **Guardrails** box ("things to avoid", one per line, max 10 × 300 characters over MCP). Built-in method rules apply even when the box is empty. |
| **Testing** | Free **Preview** mode: run the interview yourself, try to break it. Doesn't use credits. |
| **Trigger / distribution** | Share a link, an iframe embed, or a headless API ("Interviews" plan) fired on in-product events (e.g. cancellation intent). Their own churn advice: interview **within 2 weeks** of cancelling, max once per user per quarter. Outbound calling is **Enterprise-only**. |
| **Voice UX** | Browser only. Click "Start Voice Chat" → mic permission → **AI speaks first**. Mic always on (no push-to-talk), orb animation, mute button, live transcript on screen, "Done" button. **Mic denied → falls back to text, and the user can switch voice ↔ text mid-interview with history kept.** Voice is **ElevenLabs Conversational AI**. About 10 minutes, no hard limit; ends when topics are covered. |
| **Synthesis** | Per interview: insights, sentiment, pain points, feature requests, **quality score 1–5**. Cross-interview report with themes. **Every quote and theme attribution is re-checked against the transcript; anything unverifiable is discarded.** Live probes must cite a specific user utterance. Claims carry **frequency counts** ("3 of 15 participants"). **Themes are clustered before the team's hypotheses are shown** (to avoid confirmation bias). Separate agents for design / interview / analysis / report. Zod-typed outputs. |
| **Outputs** | Public report links (Notion/Confluence), CSV/JSON export, Slack, n8n, webhooks, and an MCP server so you can ask questions of transcripts from Claude Code. |
| **Pricing** | Free 10 credits · **€29/mo (29 credits)** · **€79/mo (79 credits, voice + API)** · Enterprise from €500/mo. **Text interview = 1 credit, voice = 3**, extra credit €1. **Quality gate: interviews scoring below 3/5 (or abandoned/off-topic) are free.** |

### Perspective AI (getperspective.ai)
| Part | Mechanics |
|---|---|
| **Positioning** | Broader than research: "replace forms with conversations." Agents: Concierge, **Interviewer**, Advocate, Evaluator, Intelligent Intake. Churn is one use case. |
| **Churn flow** | The interview **replaces the survey step inside the cancel flow**, triggered on the "cancel plan" click, not by a later email. Inline, popup, or chat embed. |
| **Conversation** | **One open opener** ("Before you go, what led you to cancel today?"), then follow-up intents: what they were trying to do, what they're switching to, what would have changed their mind, would they return. **About 2–3 minutes.** Example probes: vague answer → clarify; "too expensive" → value vs price; "switching" → which tool, what's better. |
| **Save routing** | When the conversation surfaces a fixable reason, it shows a **save offer in the flow** (downgrade, pause, migration call). How it decides isn't documented. |
| **Embed SDK** | Data attributes: `widget` (inline), `popup`, `slider`, `float` (chat bubble), `fullpage`. `Perspective.openPopup({ researchId, params: { email, user_id, plan, mrr, … } })`. **Any unknown param passes straight through to webhooks and exports.** Callbacks: `onReady`, `onSubmit`, `onClose`, `onNavigate`, `onError`. postMessage events and GTM dataLayer events (`perspective_conversation_completed`). |
| **Synthesis** | Theme clustering, verbatim quotes, severity flagging → **weekly digest** to product + CS. Results view shows: conversations completed, **average depth (e.g. 14 exchanges)**, top theme, key quote, sentiment, **risk signals** (e.g. "evaluating competitor"). |
| **Channels** | Text + voice, "any language." Marketing lists web, email, SMS, Slack, WhatsApp, phone, but phone isn't documented anywhere we found. |
| **Pricing** | Free 100 credits · **Pro $99/mo = 1,000 credits** · conversation = 10 credits → **~$1 per conversation**. Enterprise and done-for-you research are custom. |

---

## 2. ⚠️ Things this changes in our docs

1. **Pitch line #1 is wrong.** [Evidence doc](churncall-evidence.md) says *"Nobody interviews the customer at the moment they leave."* **Perspective does exactly that**, inside the cancel flow. Drop the line or rewrite it, e.g. *"…nobody calls them, in their language, and routes the savable ones to the founder the same day."*
2. **Price gap.** Our plan is $199 for 25 interviews (**~$8 each**). Koji voice is **€3**, Perspective is **~$1**. We need a reason worth 3–8×, or a lower price. Revenue-weighted themes, phone/Hinglish and founder hand-off are our only candidates. Ask pilots exactly this in the Oct 21 test.
3. **Timing.** Our demo sends an email after cancel. Perspective's in-flow interview catches users before they leave the page. Our "within minutes" story is weaker than theirs.

---

## 3. What to copy (ranked by value for the Oct 31 build)

| # | Copy this | From | Where it goes in ChurnCall | Effort |
|---|---|---|---|---|
| 1 | **In-flow trigger as the default**: a "Before you go, 2 minutes?" panel on the cancel page that opens a Bolna web call right there. Email invite stays as the fallback for people who skip. | Perspective | §3.2/§3.3 triggers; demo step 2 becomes instant (no waiting for an email) | M (we need a JS snippet anyway) |
| 2 | **Embed snippet with param pass-through**: `ChurnCall.open({ orgId, params: { user_id, email, plan, mrr, … } })`. Every param lands on the session row and in our webhooks. `mrr` is what powers revenue weighting **without needing a Stripe integration on day one**. | Perspective | `apps/web` snippet → `contacts`/`sessions`; Bolna `user_data` | S |
| 3 | **Per-goal follow-up depth (0–3) + a guardrails list (≤10 rules).** A simple, explainable control surface for the founder. Compiles straight into the Bolna prompt. | Koji | §5.3 guide compiler; settings UI | S |
| 4 | **Never a dead end**: mic denied or noisy → offer **"call me instead"** (Bolna outbound) or text. Koji only falls back to text; our phone fallback beats it. | Koji (improved) | invite page `/i/[token]` | S |
| 5 | **Opener + short default length**: one open question, then 4 intents. Target 2–3 minutes in the cancel flow and 4–6 minutes for email invites. | Perspective | §3.4 structure; Bolna hard limit by channel | S |
| 6 | **Quote frequency with denominators** ("7 of 23 churned users, $1.9k MRR"). Never show a theme without its count. | Koji | §3.6 dashboard theme cards | S |
| 7 | **Quality score 1–5 per interview + "you only pay for useful interviews"** (below 3 = free). Turns our eval rubric into a pricing promise. | Koji | §3.5 output (`quality_score`), §7 pricing | S (score) |
| 8 | **Hypothesis-blind clustering**: cluster and label themes *before* comparing them with the team's stated hypotheses, then show "confirmed / contradicted / new". | Koji | §5.4 step 3 | S |
| 9 | **Results header metrics**: completed, avg exchanges, top theme, key quote, risk signals (competitor named, savable). | Perspective | dashboard top row | S |
| 10 | **Free preview mode**: founder runs the interview on themselves in the browser before going live. Doubles as our onboarding "aha". | Koji | settings → "Try it" (one Bolna web call) | S |

**Already in our spec, so they only confirm we're on the right track:** quotes checked word for word against the transcript (§3.5), the coverage tracker, leading-question rewriting, and separate extraction/synthesis passes.

**Skip for now:** the MCP server over transcripts (both have one; nice later, irrelevant for judges), the multi-agent "design consultant" setup chat, and panel recruitment.

---

## 4. Where neither of them is strong (our angle, sharpened)

| Gap | Koji | Perspective | ChurnCall |
|---|---|---|---|
| **Phone as a first-class channel** | Outbound is Enterprise-only | Listed in marketing, not documented | Bolna outbound/inbound by default, "call me at 5 pm" |
| **India / Hinglish** | No language info | "Any language" claim | Bolna + Sarvam STT, Indian numbers |
| **Themes weighted by revenue** | No | Takes `mrr` as a param, but no MRR-weighted themes shown | Themes × MRR at risk is the headline view |
| **Founder hand-off on a live call** | No | Shows an in-flow offer, not a person | Bolna call transfer to the founder for high-MRR savable users |
| **Stripe-native trigger** | API/events you wire yourself | Embed only | Stripe webhook → invite/call automatically, for users who never saw the cancel page (failed payments, cancellations through support) |
| **Evidence on product tickets** | Slack, Confluence, n8n | Weekly digest | Linear issue with quotes, user count, MRR and audio clips |

**Positioning in one line:** *Koji and Perspective are survey replacements on a web page. ChurnCall is a phone-capable churn researcher that knows each customer's revenue and gets the savable ones on a call with the founder.*

---

## 5. Hands-on checklist (to finish this teardown properly)
Do as a churned user on each product (free tiers; Perspective says "no signup required to try"). Record:
- [ ] Time from clicking the link to the first AI word. Does the AI speak first?
- [ ] Latency per turn (stopwatch, 5 turns). Interruption handling: talk over it once.
- [ ] Number of follow-ups on "it was too expensive". Does it split value from price?
- [ ] What happens on a one-word answer, and on "I don't know"?
- [ ] Total length, and how it ends.
- [ ] DevTools → Network: which voice provider (ElevenLabs/LiveKit/Daily/WebRTC endpoints) and what's sent at the start (params, user id).
- [ ] The post-interview report: what's on it, how fast it appears, are quotes exact?
- [ ] Mic denied: what happens?

Use only what any user sees in their own browser. No decompiling, no scraping behind logins, no copying their UI or copy word for word.

## Sources
- Koji: [SaaS research](https://www.koji.so/docs/ai-research-for-saas), [docs index](https://www.koji.so/docs), [voice interview experience](https://www.koji.so/docs/voice-interview-experience), [guardrails](https://www.koji.so/docs/setting-interview-guardrails), [hallucination and bias mitigation](https://www.koji.so/docs/ai-interview-hallucinations-bias-mitigation), [plans](https://www.koji.so/docs/plan-comparison-guide)
- Perspective: [home](https://getperspective.ai), [Interviewer agent](https://getperspective.ai/agents/interviewer), [pricing](https://getperspective.ai/pricing), [embed SDK](https://getperspective.ai/docs/build/embed-api), [replacing the exit survey](https://getperspective.ai/blog/how-to-find-out-why-customers-cancel-2026-replacing-the-exit-survey)
