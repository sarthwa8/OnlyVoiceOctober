# PagerCall: the AI on-call engineer you talk to at 3 a.m.

> ⚠️ **Not chosen (2026-10-18):** the locked build is **[CHURNCALL.md](../../docs/CHURNCALL.md)**. This doc is kept for reference.

> v0.1 · 2026-10-18 · Team of **2** · Status: **recommended pick, awaiting approval**
> Supersedes the CareCall recommendation in [DECISION.md](DECISION.md) (the brief changed: tech-industry, B2B, venture scale).
> **[verify]** = confirm in Bolna or vendor docs, or by testing, before relying on it.

---

## 0. TL;DR

When production breaks at 3 a.m., today's on-call flow looks like this:
- PagerDuty or Opsgenie phones the engineer with a robot voice: *"Press 4 to acknowledge."*
- The engineer stumbles to a laptop and spends the next 20–40 minutes finding out what happened: which deploy, which error, which service.
- Then they page a second person and repeat the context.

**PagerCall replaces the robot call with an engineer-grade AI that has already investigated before your phone rings.**

> *"Hey Sarthak, checkout is failing: 12% error rate on `/api/checkout`, started 4 minutes after deploy `a1f3c` by Riya, which changed the payment client's timeout from 30s to 3s. Stripe calls are timing out. I recommend rolling back to the previous deploy. Should I?"*
> → "What else changed in that deploy?" → *answers* → "Roll it back." → *"Enter your PIN on the keypad to confirm."* → rollback → *"Errors are back to 0.2%. I've posted the timeline in #inc-checkout and drafted the postmortem. Go back to sleep."*

It's a voice-native incident responder:
1. **Investigates** the alert in under a minute: deploys, diffs, errors, metrics, logs, past incidents.
2. **Calls** the on-call engineer with a 20-second brief they can question in plain speech.
3. **Acts** on spoken approval, with keypad-PIN confirmation for anything risky: roll back, scale, flip a feature flag, restart, open a revert PR.
4. **Escalates**: calls the secondary already briefed, or patches them in.
5. **Writes it up**: Slack timeline, status-page draft, postmortem.

The long-term pitch line: ***the best on-call call is the one you don't get.*** Known, low-risk incidents get fixed while you sleep, and you hear about them in a 30-second morning summary call.

---

## 1. Why this one (and why not the others)

### What you asked for, and how PagerCall fits
| Your criterion | PagerCall |
|---|---|
| Useful to an industry, specifically tech | Every software company with production has on-call |
| Voice makes it genuinely better, not a gimmick | **The phone call is already the on-call interface.** It's just dumb today. Hands-free, half-awake, walking to the laptop: voice is the right medium for those first 5 minutes. |
| Technical, a real engineering product | An agentic investigator with tool use across GitHub/Vercel/Sentry/metrics/logs, a safe-action framework, durable escalation workflows and a real-time voice UX |
| Scalable: big market, big revenue, fundable | The AI SRE category is one of the hottest in dev infra (see below). Seat + usage pricing, global market from day one. |

### Market signal (sources at the end)
- **Resolve AI** (AI SRE) raised a **$125M Series A at a $1B valuation** led by Lightspeed (TechCrunch, Dec 2025 / Feb 2026).
- **Traversal** reportedly raised a **$48M Series A** (Kleiner Perkins, Sequoia) [verify].
- **PagerDuty** launched an AI agent suite in Oct 2025 (SRE Agent, Scribe, Shift Agent, Insights), but it's **text/Slack-based. I found no voice on-call agent.** The incumbents are adding AI to the dashboard and Slack, not to the phone call that actually wakes people up. That's our wedge.
- The "AI SRE" players sell investigation. **Nobody owns the human moment**: waking a person, briefing them, getting a decision, coordinating responders. Voice is how we own it.

### Other tech-industry ideas I considered
| Idea | Verdict | Why |
|---|---|---|
| **PagerCall** (AI on-call by phone) | ✅ **Pick** | Voice is native, hot category, users reachable (dev teams self-serve), we control the demo end to end |
| **Gatekeeper**: AI IT-helpdesk line that resolves L1 tickets *and* blocks vishing (fake "employee" calls asking for MFA resets, as in the Scattered Spider attacks) | 🥈 **Runner-up** | Huge security budgets and a real, current threat (vishing is a top initial-access vector per vendor summaries of Mandiant data). But we can't get real users by Oct 31: no company lets a hackathon tool reset passwords. Enterprise sales cycle. Deepfake detection is hard to prove in 13 days. |
| Hamming-for-Bharat (voice-agent QA) | ❌ | Competes with the host's own "build, test, deploy, monitor" pitch |
| AI technical phone screens | ❌ | Crowded (Mercor, micro1 and others) and recruiting is a Bolna-customer use case |
| Voice support agent for SaaS | ❌ | Bolna's customers do support every day |
| "Dispatch": run coding agents by phone | ❌ | The big labs are shipping this as a feature |
| Voice in-app copilot SDK for SaaS | 🟡 | Big but crowded (Intercom, Decagon, Sierra voice). Hard to differentiate in 13 days |
| AskYourData (talk to your warehouse) | ❌ | Crowded analytics category, weak voice reason |
| NightShift Saathi | ❌ (your call) | Social-impact framing and life-safety liability, not the B2B tech product you want |
| CareCall | ❌ (your call) | Fair point: you want a product for an industry, and an AI standing in for family is a hard sell emotionally |

---

## 2. Honest pros and cons

### Pros
- **Voice is the existing channel, not a bolt-on.** On-call phone calls already exist. We upgrade them from a one-way robot to a two-way expert.
- **Demo we fully control**, with no dependency on strangers: break our own deployed app on stage → a phone rings → "roll it back" → the site recovers live. It's the kind of moment a crowd and the judges *feel*.
- **Deep technical credibility** for the Bolna interview and YC: agent design, tool safety, latency engineering, durable workflows.
- **Self-serve growth:** a developer can connect GitHub + Sentry + Vercel in 5 minutes. No enterprise procurement to start.
- **Strong Bolna showcase:**
  - API-triggered outbound calls with rich per-call context
  - mid-call custom function calls
  - **keypad (DTMF) PIN confirmation** for destructive actions
  - call transfer to the secondary on-call
  - an inbound "status line" ("call in: what's happening with checkout?")
  - post-call webhooks
- **Not what Bolna's customers do** (they do sales, support, collections, recruiting). It also expands where voice AI is used: Bolna's own engineering team has on-call, and is a potential first design partner.
- **Clear expansion path:** auto-remediation for known incidents → AI incident commander on bridge calls → postmortems and status pages → full AI SRE platform → NOC/IT ops.

### Cons, with mitigations
| Con | Severity | Mitigation |
|---|---|---|
| **Crowded, well-funded category** (Resolve, Traversal, PagerDuty's own agents) | High | Don't compete on investigation depth. Win the *responder experience* (voice, decisions, coordination) and **integrate with** PagerDuty/Opsgenie/incident.io as an upgrade to their phone call. Be honest in the pitch: "they built the analyst, we built the responder." |
| **"It's a feature. PagerDuty adds voice next year."** | Medium | Speed plus depth of the voice UX (half-awake engineers, interruptions, numbers, code identifiers spoken clearly) is genuinely hard. Our safe-action layer + incident memory compounds. Incumbents move slowly on phone UX (the "press 4" call is about 15 years old). |
| **Trust: will anyone let an AI touch prod?** | High | Actions are an **allowlist** per service with risk tiers. Destructive ones need a spoken read-back **and** keypad PIN. Every action logged with a one-tap undo, plus auto-verification afterwards. Default mode for new teams is "recommend only". |
| **Real incidents are rare** → few real calls by Oct 31 | Medium | Weekly **game days** (chaos drills) on each pilot team's staging, plus real low-severity alerts (uptime monitors, error spikes). Report both honestly. |
| **Latency of tool calls mid-conversation** | Medium | Investigation runs *before* dialling. Likely follow-up answers are pre-computed and cached. Spoken fillers ("checking the logs…") for live lookups. Hard 3 s budget per mid-call tool. |
| **Less "India" than Bolna's usual story** | Low | Indian startups (Bengaluru alone) are a big early market, and English with Hinglish tolerance is fine. Pitch the global market: dev tools sell worldwide from day 1. |
| **Security of credentials we hold** (GitHub/Vercel/cloud tokens) | Medium | GitHub App with minimal scopes, short-lived tokens, encrypted at rest, per-org isolation, no free-form shell. |

---

## 3. Product spec

### 3.1 Users
- **On-call engineer** (primary user): gets the call, makes decisions.
- **Secondary / subject-matter expert:** gets escalated with context.
- **Eng manager / founder** (buyer at startups): wants lower time to resolve, fewer people woken up, and postmortems that actually get written.

### 3.2 Core flows
**A. Connect (5 minutes, web):** install the GitHub App, add a Vercel/Render/Railway token, a Sentry token, and optionally Grafana/Prometheus/Datadog. Point alert webhooks at PagerCall (Sentry, Grafana Alertmanager, UptimeRobot/BetterStack, Datadog, or generic JSON). Add an on-call rotation (phone numbers + PINs). Choose allowed actions per service.

**B. Incident → investigate → call:**
1. An alert arrives. Dedupe/group into an incident.
2. The **investigator agent** runs for ≤ 60 s:
   - recent deploys and their diffs
   - top new errors and stack traces
   - metric deltas around the start time
   - log search
   - runbook lookup
   - similar past incidents
3. It produces an **incident brief**: impact, suspected cause plus evidence, confidence, and recommended actions with risk tier.
4. A **severity gate** decides: low → Slack only, plus a morning summary. High → call now.
5. **Bolna outbound call** to the primary, with the brief injected as `user_data`.

**C. The call:**
- 20-second brief (impact → cause → recommendation), then "What do you want to do?"
- Free Q&A through mid-call functions: "show the diff", "which customers are affected", "is the DB OK", "what did we do last time this happened".
- Actions: "roll back" / "scale to 6" / "turn off the new-checkout flag" / "page Riya" / "snooze 10 minutes" / "I'm on it, just watch".
- Risky action → read-back + **DTMF PIN** → execute → keep watching metrics for 5 minutes → call back or post the result.
- No answer in 3 minutes → call the secondary with the brief ("Sarthak didn't pick up…").

**D. Status line (inbound):** anyone on the rotation calls the PagerCall number, enters their PIN, and asks "what's going on with checkout?" or "who's on call?".

**E. After the incident:** an auto-generated timeline (alerts, findings, call transcript, actions, recovery) → Slack channel → a postmortem draft as a markdown PR in the repo (or Notion).

**F. Morning summary call** (optional): *"Two incidents overnight. One auto-resolved, one rolled back by Sarthak at 3:12. Postmortem draft is ready."*

### 3.3 Safe-action framework (the trust core)
| Tier | Examples | Gate |
|---|---|---|
| 0: read | query logs/metrics/errors, read diff | none |
| 1: reversible, low blast radius | snooze alert, post to Slack, page someone, open revert PR | spoken "yes" |
| 2: production change, reversible | roll back / promote previous deploy, toggle feature flag, scale replicas, restart service | read-back + **DTMF PIN** + auto-verification + one-tap undo |
| 3: irreversible / data | DB operations, deleting resources | **never via voice** (link sent to laptop) |

Every action is recorded as `{who, what, when, why, evidence, result}` in an append-only audit log.

---

## 4. Architecture

```
 Alert sources                     PagerCall (TypeScript monorepo)                         Bolna
 ─────────────                     ───────────────────────────────                        ─────
 Sentry ─┐                    ┌──────────────────────────────────────────┐
 Grafana ├─ webhooks ───────► │ ingest → dedupe/group → incident         │
 Uptime  │                    │      │                                   │
 Datadog ┘                    │      ▼                                   │
                              │ INVESTIGATOR agent (LLM + tools, ≤60s)   │──tools──► GitHub / Vercel /
                              │  → brief JSON + cached Q&A               │           Sentry / Prometheus /
                              │      │                                   │           Loki / runbooks / pgvector
                              │      ▼                                   │
                              │ ESCALATION workflow (Inngest, durable)   │──POST /call (user_data)──► outbound
                              │  call primary → wait 3m → secondary …    │                          voice agent
                              │      ▲                                   │◄── mid-call functions ───  (Sarvam/Deepgram STT,
                              │ /fn/* : ask, get_diff, rollback, flag,   │    (HTTP, ≤3s budget)      Cartesia/ElevenLabs TTS)
                              │         scale, page, ack, snooze         │◄── exec webhooks ──────── transcripts
                              │ ACTION executor (allowlist, PIN, verify) │
                              │ comms: Slack, status page, postmortem PR │
                              └───────────────┬──────────────────────────┘
                                              │
                     Postgres (Neon/Supabase) + pgvector · Next.js dashboard on Vercel
```

### Stack
| Layer | Choice | Why |
|---|---|---|
| Language | **TypeScript** everywhere (Next.js app + Node worker) | Two people, one language. First-class SDKs (Octokit, Vercel, Sentry, Slack). |
| Durable workflows | **Inngest** (or Trigger.dev) | Escalation = "call, wait 3 min, check ack, call next". Sleeps and retries survive restarts. |
| DB | **Postgres** (Neon or Supabase) + **pgvector** | Incidents, audit log, similar-incident memory |
| Investigator LLM | Claude Sonnet 5.5 (tool use); Haiku 5.5 for fast summaries and call-time Q&A | Strong tool use + speed. A single provider keeps it simple. |
| Voice | **Bolna** outbound + inbound agents; English with Indian-accent tolerance. STT: Deepgram (tech vocabulary) vs Sarvam A/B; TTS: Cartesia/ElevenLabs Turbo (low latency) | Pick on Day 1 by testing identifiers like "a1f3c", "p99", "OOM" |
| Web | Next.js 15 + Tailwind + shadcn/ui | Connect flow, rotations, incidents, timelines, recordings, settings |
| Demo target | **"Shoply"**: a small Next.js shop on Vercel + Sentry + a Postgres DB + a feature flag (GrowthBook/Unleash or env-based) | Our own production to break on stage |
| Chaos kit | Scripts that inject 15–20 failure modes into Shoply | Game days + evaluation |

### Bolna specifics
- **Agent `pagercall-responder` (outbound):**
  - prompt = calm, terse incident-responder persona
  - `user_data` = brief + cached Q&A + allowed actions + responder name
  - functions = `ask_investigator(question)`, `get_diff`, `execute_action(action, params)`, `page(person)`, `ack`, `snooze`
  - DTMF capture for the PIN [verify DTMF in the middle of a function flow]
  - call transfer to the secondary [verify]
  - keyword biasing: service names, repo names, engineer names, "rollback", "p99", "OOM", "five-hundreds"
- **Agent `pagercall-status` (inbound):** DTMF PIN → caller identified → status Q&A.
- **Webhooks:** call transcripts → timeline and postmortem.
- **Speaking identifiers:** commit SHAs read as "a-one-f-three", numbers rounded ("about 12 percent"), service names given phonetic hints. This is a real voice-UX job and part of our differentiation.

### Data model (core)
```
orgs, users(phone, pin_hash, role), rotations(schedule json), services(name, repo, deploy_provider, allowed_actions json)
integrations(org_id, kind, encrypted_creds, scopes)
alerts(id, org_id, source, fingerprint, payload, received_at)
incidents(id, org_id, service_id, severity, status, started_at, acked_by, resolved_at, brief json, root_cause, confidence)
investigation_steps(incident_id, tool, input, output_summary, ms)
calls(id, incident_id, user_id, direction, bolna_execution_id, outcome, transcript, recording_url)
actions(id, incident_id, tier, kind, params, requested_by, confirmed_via, status, result, undo_ref)   -- append-only
postmortems(incident_id, markdown, pr_url)
incident_embeddings(incident_id, vector)
```

---

## 5. Evaluation: "PagerCall Bench"
- **15–20 seeded failure scenarios in Shoply:**
  - bad deploy (timeout change)
  - missing env var
  - DB connection-pool exhaustion
  - slow query after a migration
  - third-party (Stripe/API) outage
  - memory leak / out-of-memory loop
  - feature-flag bug
  - rate limiting
  - expired certificate or DNS problem (simulated)
  - cron job storm
  - cache stampede
  - …
- For each scenario we measure:
  - **root-cause top-1 accuracy**
  - **recommended-action correctness**
  - **time to brief**
  - **unsafe-action rate** (target 0)
- **Voice evals:** 30 scripted responder utterances (interruptions, "uh roll it… no wait, flip the flag", identifiers) → correct intent + correct gate.
- It runs in CI on every investigator prompt or tool change. **Published numbers become part of the pitch.**

---

## 6. Targets

### By Oct 31 (submission)
| Metric | Target |
|---|---|
| Pilot teams connected (real repos/alerts; startups, friends' companies, college product teams) | **≥ 5** |
| Real alerts processed | ≥ 50 |
| Real phone pages + game-day calls | ≥ 30 |
| Bench: root-cause top-1 | ≥ 70% |
| Bench: unsafe actions | **0** |
| Alert → phone ringing with brief | p50 ≤ 75 s |
| Voice turn latency | p50 ≤ 1.5 s (≤ 3 s with a tool call) |
| Time to diagnosis in drills: PagerCall vs a human with dashboards | Measured head-to-head on 5 drills |
| Design partners willing to pay / LOI | ≥ 2 |

### By Nov 20 (finale)
≥ 10 teams, auto-remediation for 2–3 known incident types, a PagerDuty/Opsgenie integration ("PagerCall answers your PagerDuty pages"), live stage demo rehearsed with a backup recording.

---

## 7. Business model
- **Pricing:** $25–40 per on-call responder per month, plus AI investigation usage beyond a free tier. India startups at around ₹1,500 per responder.
- **Wedge:** startups and scale-ups that hate their on-call (5–200 engineers), self-serve + founder-led.
- **Then:** mid-market through PagerDuty/Opsgenie/incident.io integrations, and enterprise "AI incident commander".
- **Moat over time:**
  - per-org incident memory and runbooks that learn
  - a trust record (actions taken, zero unsafe)
  - integrations
  - a voice responder UX tuned on thousands of 3 a.m. calls
- **Why VCs care:** a category that produced a $1B company in about 2 years, plus a channel (the phone call) the leaders don't own.

---

## 8. Getting real users (team of 2, 13 days)
1. **Our own apps first:** Shoply plus any project either of us runs in production.
2. **5–10 small teams:** Chandigarh/Mohali startups, college incubator startups, seniors' startups in Bengaluru, indie hackers, Bolna Builders Slack and other hackathon teams with live deploys. **Offer:** free forever for the pilot, recommend-only mode by default, 10-minute setup on a call with us.
3. **Weekly game day** with each team on their staging: we break something, PagerCall pages them, and we time it.
4. **Ask Bolna's own engineering team** to be a design partner during the interview round.
5. Launch posts (X/LinkedIn/HN Show) with the demo video around Oct 28 for inbound sign-ups.

---

## 9. Two-person plan

### Roles (both touch everything; each owns a track)
- **Person A: Agent + integrations + safety.** Investigator agent and tools (GitHub, Vercel, Sentry, Prometheus/Loki), action executor + allowlist + audit, PagerCall Bench.
- **Person B: Voice + product + users.** Bolna agents and call UX, escalation workflows (Inngest), Next.js dashboard and connect flow, Shoply + chaos kit, pilot teams, video and pitch.
- **Daily at 21:00 (30 min):** listen to the day's calls, review Bench numbers, pick tomorrow's top 3.

### Day by day
| Dates | Person A | Person B | Exit check |
|---|---|---|---|
| **Sat Oct 18 – Sun Oct 19** | Repo scaffold (Next.js + worker + Postgres + Inngest). GitHub App + Vercel + Sentry clients. Investigator v0 on one hard-coded scenario. | Bolna account + number. **Spikes:** outbound call with `user_data`; mid-call function latency; DTMF PIN capture; transfer; STT on SHAs/"p99"/service names (Deepgram vs Sarvam); TTS voice. Build **Shoply** on Vercel + Sentry. | **Gate Oct 20:** a hard-coded brief is spoken on a real call, and a mid-call function round-trip is ≤ 3 s |
| **Mon Oct 20 – Tue Oct 21** | Alert ingest (Sentry, Grafana, generic) → incident grouping. Investigator v1 with tools (deploys, diff, errors, metrics, logs). Brief schema. | `pagercall-responder` agent v1. Escalation workflow (primary → 3 min → secondary). Chaos kit: first 5 failure modes. | **End-to-end on Shoply:** break → alert → investigate → phone rings → spoken brief |
| **Wed Oct 22 – Thu Oct 23** | Action executor: Vercel rollback/promote, flag toggle, scale/restart (Render/Railway), revert PR. Allowlist, PIN, audit log, post-action verification. | Mid-call functions wired (Q&A, actions, page, snooze). DTMF PIN gate. Dashboard v1 (connect flow, incidents, timeline, recordings). | **"Roll it back" by voice fixes Shoply live** |
| **Fri Oct 24 – Sun Oct 26** | PagerCall Bench (15 scenarios) in CI, investigator iteration, similar-incident memory (pgvector), Slack timeline + postmortem PR. | **Onboard 3–5 pilot teams.** Inbound status line. First game days with pilots. Voice evals (interruptions, identifiers). | ≥ 3 real teams connected; Bench ≥ 60% |
| **Mon Oct 27 – Tue Oct 28** | Hardening: token scoping, encryption, rate limits, idempotency, timeouts. Bench → ≥ 70%. | ≥ 5 pilot teams, metrics page, **LOI/pricing asks**, launch post + demo clip. | Metrics exported; ≥ 2 design-partner commitments |
| **Wed Oct 29 – Thu Oct 30** | Demo reliability (pre-warmed caches, backup recording) | 2-min video + written submission | **Submitted Oct 30** (Oct 31 buffer) |
| **Nov 1 – Nov 20** | Auto-remediation for known patterns, PagerDuty/Opsgenie bridge, morning summary call | More teams, interview prep (architecture, safety, latency, Bench), stage rehearsal | Finale-ready |

### Scope cuts for a team of 2
- No Kubernetes in v1: Vercel/Render/Railway only, which most startups use. k8s comes after Oct 31.
- No status-page integration in v1; a Slack draft is enough.
- One alert source done really well (Sentry) + generic webhook. Others after.

---

## 10. Demo script (2-minute video = stage base)
1. **0:00–0:12:** a black screen, a phone buzzing at 3:07 a.m., the old robot voice: *"PagerDuty alert. Press 4 to acknowledge."* Caption: "This is how every engineer gets woken up."
2. **0:12–0:25:** we merge a "harmless" PR to Shoply live. Checkout starts failing and Sentry lights up.
3. **0:25–1:10:** **the phone rings with PagerCall's brief** (shown with live captions). The engineer asks "what changed?" and gets the answer. "Roll it back." → PIN on the keypad → the Vercel dashboard shows the rollback → error graph drops → *"Recovered. Timeline's in Slack."*
4. **1:10–1:30:** the Slack timeline and a postmortem PR, already written.
5. **1:30–1:50:** proof: pilot teams, alerts handled, Bench accuracy, time-to-diagnosis vs a human, 0 unsafe actions.
6. **1:50–2:00:** "PagerCall. The on-call engineer that's already awake. Built on Bolna."

---

## 11. Decisions needed from you
1. **Approve PagerCall** (Gatekeeper as runner-up).
2. Who is Person A (agent/integrations) and who is Person B (voice/product/users)?
3. Do you or your teammate have a production app, or know 3–5 startups/teams with live deploys who'd pilot? Names to message today.
4. Name: **PagerCall**, or something punchier (*Wakeup*, *Sev0*, *OnCall.ai*)?

---

## Sources
- [TechCrunch: Resolve AI hits $1B valuation with Series A (Dec 2025)](https://techcrunch.com/2025/12/19/ex-splunk-execs-startup-resolve-ai-hits-1-billion-valuation-with-series-a) · [TechCrunch: Resolve AI confirms $125M raise (Feb 2026)](https://techcrunch.com/2026/02/04/ai-sre-resolve-ai-confirms-125m-raise-unicorn-valuation/)
- [Traversal funding profile (vcbacked)](https://www.vcbacked.co/company/traversal) · [Best AI SRE tools 2026 overview](https://prommer.net/en/tech/guides/best-ai-sre-tools-2026/)
- [PagerDuty launches end-to-end AI agent suite (BusinessWire, Oct 2025)](https://www.businesswire.com/news/home/20251008279706/en/PagerDuty-Launches-Industry%E2%80%99s-First-End-to-End-AI-Agent-Suite-Slashing-Incident-Response-Times-and-Empowering-Teams-to-Innovate) · [IT Brief: PagerDuty AI agents](https://itbrief.news/story/pagerduty-unveils-ai-agents-150-updates-for-operations-teams)
- Gatekeeper context: [CSA research note on AI vishing (2026)](https://labs.cloudsecurityalliance.org/research/csa-research-note-athr-ai-vishing-credential-harvesting-2026/) · [CIS: vishing as an evolving threat](https://www.cisecurity.org/insights/blog/vishing-evolving-threat-us-sltt-organizations) · [Arsen: AI vishing targeting help desks](https://arsen.co/en/blog/ai-vishing-help-desk-attacks)
