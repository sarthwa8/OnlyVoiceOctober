# Action plan: today and this week

> Updated Sat 2026-10-18 · Product: [ChurnCall](CHURNCALL.md) · Evidence and competitors: [research/churncall-evidence.md](research/churncall-evidence.md)

## The call: test, don't brainstorm and don't build the whole thing yet
- **Stop brainstorming.** We have a direction (ChurnCall), backups (win-loss interviews, India phone-first) and evidence.
- **Don't build the full product yet.** Koji and Perspective AI already do AI voice churn interviews. The risk isn't *can we build it*. It's:
  1. Will churned users actually talk?
  2. Are our insights better than an exit survey or Koji?
  3. Will founders pay more than Koji's €79/month?
- **So:** build the smallest test (invite → call → transcript → insights) while reaching out to startups at the same time.

## Roles
- **Person A: AI and voice.** Bolna agent, interviewer prompt, extraction, synthesis, evals.
- **Person B: Product and GTM.** Pilot startups, invite emails, landing page, dashboard, pitch.

## Today: Sat Oct 18
### Morning (both, 1–2 hours)
- [ ] Each of us tries **Koji** (koji.so) and **Perspective AI** (getperspective.ai) as a churned user. Note what's good and what's missing. (30 min)
- [ ] **Person B leads:** message **8–10 startups** from our freelance and GTM network. Ask: *"Free pilot. We'll interview 50 of your churned or trial-dropped users this week and send you the insights. Just need a CSV of emails."* Target: **3 yeses**.
- [ ] Each of us asks **5 friends:** *"If a founder emailed you after you cancelled, would you tap 'talk for 3 minutes' for a $5 voucher?"*

### Afternoon and evening
**Person A**
- [ ] Bolna account + submit the hackathon apply form + join the Bolna Builders Slack and ask about credits
- [ ] First **Web Call SDK** (browser) call + first outbound call working
- [ ] Interviewer prompt v1

**Person B**
- [ ] Invite email in **2 versions**: personal from the founder vs generic
- [ ] Repo scaffold + invite landing page → call
- [ ] Follow up with the startups

### Done when
- [ ] ≥ 3 startups said yes
- [ ] One end-to-end test interview run on ourselves

## This week
| Day | Goal |
|---|---|
| **Sun Oct 19** | Extraction v1 (JSON + checking quotes against the transcript). **First real invites sent.** |
| **Mon Oct 20** | Fix what the first calls show. Invite all pilot lists. Funnel tracking: sent → opened → started → completed. **≥ 10 completed interviews.** |
| **Tue Oct 21** | **GO / NO-GO.** (1) Completion rate by channel and incentive. (2) Side-by-side of our insights vs their exit survey vs Koji. (3) What founders say they'd pay. Go = (1) passes **and** (2) or (3) passes. |
| **Wed Oct 22 – Thu Oct 23** | **If go:** theme dashboard + revenue weighting + Stripe trigger. **If no-go:** switch the same engine to win-loss interviews or India phone-first. |
| **Fri Oct 24 – Sun Oct 26** | Slack + Linear integration, 2nd wave of invites, **≥ 40 interviews**. Interviewer v2 only if the evals show gaps. |
| **Mon Oct 27 – Tue Oct 28** | Eval report, ask for a paid pilot / LOI, launch post draft |
| **Wed Oct 29 – Thu Oct 30** | 2-min video + written submission. **Submit Oct 30** (deadline Oct 31). |

## One rule every day
**Every evening, both of us listen to 5 real calls** (30 min), log issues in `docs/pilot-log.md`, and pick tomorrow's top 3 fixes.

## Getting this repo
```bash
git clone https://github.com/sarthwa8/OnlyVoiceOctober.git
cd OnlyVoiceOctober
git checkout claude/bold-allen-oicfqq
# later, to update:
git pull origin claude/bold-allen-oicfqq
```
