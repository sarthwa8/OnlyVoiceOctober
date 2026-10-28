# Buildathon submission kit (due Sat Oct 31; aim for Thu Oct 30)

> Drafted 2026-10-28 by Sarthak (with Claude). Everything in **[brackets]** needs a real number from `/results` or a decision. Never round a number up or invent one: judges interview the shortlisted teams, and every claim here must survive a follow-up question.
> Form: https://www.bolna.ai/symphony/buildathon/submit · Details: [`hackathon-details.md`](../hackathon-details.md)

## 1. The form, field by field
| Field | Answer |
|---|---|
| Team size | 2 |
| Full name / Email | [the registered person's name and **the same email used on the apply form**] |
| Project name | **ChurnCall** |
| Project description (≤ 200 chars) | **Recommended (178):** `An AI voice interviewer for SaaS founders: it talks to users who cancelled, finds the real reason they left, and reports it with exact quotes and revenue at risk. Built on Bolna.` |
| | Alt, shorter (166): `AI voice interviews with churned SaaS users: the real reason they left, in their own words, ranked by revenue at risk. For founders and product teams. Built on Bolna.` |
| Submission link | GitHub repo **[make `sarthwa8/OnlyVoiceOctober` public, or link a demo page; check that `data/` and `.env` are not in it]**. Optionally a live demo link (see §5). |
| Pitch video / deck link | Google Drive link, sharing **"Anyone with the link"** (test it in a private window) |

## 2. The story (use the same words in the video, the deck and the interview)
1. **Problem:** every subscription company loses customers, and exit surveys say "too expensive", which is usually not the real reason. In the first audit we found, 38% picked "too expensive", but most of those users had never finished onboarding (SEOJuice founder, ~340 cancellations; small sample, say so).
2. **Insight:** people tell you the real story in a short conversation, not a checkbox. A randomised study found spoken answers carry more information than typed ones (Galasso, Nannicini & Nozza, IZA DP 17488, 2024).
3. **Product:** the founder uploads churned users → each gets a private link → one tap starts a ~3-minute AI voice interview in the browser (or "call me") → every call becomes a reason, a "savable" score and **quotes checked word for word against the transcript** → `/results` shows reasons by revenue at risk.
4. **Why us vs Koji / Perspective:** they're survey replacements on a web page. ChurnCall weights every reason by the customer's revenue, works by phone, and is built for founders to act the same day. (Don't claim we're the only AI churn interviewer. We're not.)
5. **Proof:** [the pilot numbers, §3].
6. **Built on Bolna:** Web Call SDK, outbound calls with `user_data` prompt variables, the v2 agent API (pushed from code with `agents/sync.py`), post-call webhooks, recordings.

## 3. Numbers to fill in (from `/results`, the evening before recording)
| Metric | Value | Where |
|---|---|---|
| Startups in the pilot | [ ] | pilot log |
| Invites sent | [ ] | `/results` funnel ("invited") |
| Opened / started / completed | [ ] / [ ] / [ ] | `/results` funnel |
| Completion rate (completed ÷ opened) | [ ]% | `/results` |
| Top 3 reasons, with count and MRR | [ ] | `/results` reasons |
| 2–3 best quotes (with permission) | [ ] | `/results/<token>` |
| Quote faithfulness | **100%** by construction (unverifiable quotes are dropped in code) | `extraction.verify_quotes` |
| Interview quality before → after prompt v2 | talk ratio **0.29 → [ ]**, AI words/turn **28.7 → [ ]**, double questions **2 → [ ]** | `eval/interviews/quality.py` on a real call |
| A founder's reaction | "[quote]" | pilot log, Step 15 |

**If the pilot is small (e.g. under 10 calls):** say exactly that. "We ran N real interviews with M startups this week" plus one strong quote and a founder reaction beats a big made-up number. If there were no outside users at all, call it "test interviews with friends playing churned users", never "customers".

## 4. Pitch video (2 minutes) script
| Time | On screen | Voice-over |
|---|---|---|
| 0:00–0:12 | An exit survey with "Too expensive" ticked | "This is everything most SaaS founders learn when a customer leaves. And it's usually not even true." |
| 0:12–0:20 | The founder's CSV → `make_invites.py` → private links | "ChurnCall gives every churned user a private link from the founder." |
| 0:20–0:55 | Phone screen: open the link → **Talk in browser** → the AI's opener → 2–3 real exchanges (captions on) | "One tap, and an AI interviewer asks what actually happened, one short question at a time." |
| 0:55–1:25 | `/results`: funnel, reasons by MRR, one call's insight card with highlighted quotes, the recording | "Every call becomes a reason, a savable score and exact quotes. We check each quote against the transcript, so nothing is made up." |
| 1:25–1:45 | The pilot numbers (§3) + a founder quote | "This week: [N] interviews for [M] startups. [Founder]: '[quote]'." |
| 1:45–2:00 | Architecture strip: invite page → Bolna web call / outbound → webhook → extraction → results | "Built on Bolna's Web Call SDK, outbound calls and webhooks. ChurnCall: every churned user, interviewed." |

**Recording tips:** record the call segment from a **real** call (a teammate playing a churned user is fine if you say so). Use `scripts/seed_results_demo.py` data **only** for practice, never as pilot results. Blur emails and phone numbers.

## 5. Live demo link (optional but strong)
Judges may click the link days later, so a laptop + ngrok demo can be offline when they try.
- **Simplest honest option:** submit the GitHub repo + the video, and keep the live demo for the interview round (Nov 5–7).
- **If there's time:** deploy the web app on Vercel and the API on Railway/Fly/Render (~2–3 h; the API needs `CHURNCALL_DATA_DIR` on a persistent volume). Point Bolna's webhook at the new URL with `agents/sync.py`.

## 6. Before you press submit
- [ ] Repo is public (or the link works for someone logged out), `README.md` explains what it is and how to run it
- [ ] `git log -p | grep -i "sk-\|api_key="` finds no secrets; `data/` was never committed
- [ ] Video link opens in a private window
- [ ] Description ≤ 200 characters (the recommended one is 178)
- [ ] Every number in the video matches `/results` on the day it was recorded
- [ ] Same email as the apply form
