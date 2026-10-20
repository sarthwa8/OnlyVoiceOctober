# OnlyVoiceOctober: ChurnCall for the Bolna Buildathon

## We're building **ChurnCall**, and only ChurnCall
The AI that calls your churned users and tells you why they left. When a SaaS user cancels, downgrades or goes quiet, ChurnCall invites them to a short voice conversation (one tap in the browser, or a phone call when they ask for one). An AI interviewer runs a research-grade conversation with real follow-up questions, then turns every call into churn themes weighted by revenue at risk. Each theme comes with verbatim quotes and audio clips, alerts about users who can be won back, and Linear tickets.

## Where things are
| What | Where |
|---|---|
| **Today and this week** | [docs/ACTION_PLAN.md](docs/ACTION_PLAN.md) |
| **Product spec** (problem, product, architecture, evals, business) | [docs/CHURNCALL.md](docs/CHURNCALL.md) |
| **Build plans** (one per feature, with steps and checks) | [build-plans/](build-plans/) · done: [01 invite page](build-plans/01-invite-page.md) |
| Evidence and competitors | [docs/research/churncall-evidence.md](docs/research/churncall-evidence.md) · [Koji/Perspective teardown](docs/research/koji-perspective-teardown.md) |
| Latest handoff between us | [docs/HANDOFF_2026-10-20.md](docs/HANDOFF_2026-10-20.md) · open questions for Bolna: [docs/BOLNA_QUESTIONS.md](docs/BOLNA_QUESTIONS.md) |
| Hackathon rules and dates | [hackathon-details.md](hackathon-details.md) |
| API (FastAPI): invites, calls, webhook, extraction | [apps/api/](apps/api/README.md) |
| Web (Next.js): the invite page `/i/[token]` | [apps/web/](apps/web/) |
| Bolna interviewer agent: prompt, settings, sync script | [agents/](agents/) |
| Interview evals (persona simulator) | [eval/](eval/) |
| Dropped ideas (reference only, don't build from them) | [archive/](archive/README.md) |

## Key dates
Kill test go/no-go **Oct 21** · submit **Oct 30** (deadline Oct 31) · finale **Nov 20**, Bengaluru.

## Team
Sarthak (AI + voice: agent, prompt, extraction, evals) · Pranav (product + GTM: invite flow, web app, pilots, pitch).
