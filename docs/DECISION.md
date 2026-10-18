# Decision: what we build for the Bolna Buildathon

> 2026-10-18 · Status: **awaiting approval** · Research inputs: [docs/research/](research/)
> Deadline: submit by **Oct 31** · Shortlist Nov 3 · Interviews Nov 5–7 · Finale (top 3, YC interview prize) **Nov 20**

## TL;DR

**We build CareCall: one phone number that looks after ageing parents.**

- **Every day:** a warm call in the parent's own language (Hindi, Punjabi, English and others). It covers medicines, mood, symptoms and a few minutes of real conversation. The children get a dashboard, and an alert when something is off.
- **When a scammer calls:** the parent merges the CareCall number into the call (*Add call → Kavach → Merge*). **Kavach** announces itself, listens, recognises the digital-arrest / fake-courier / KYC script, warns the parent in their language, and alerts the family on WhatsApp.

The daily check-in is the **product and the business**. Kavach is the **stage moment and the moat**.

**Runner-up / backup:** Awaaz Research (AI voice surveys in Indian languages).

---

## 1. How I chose

The refined doc's four filters are the right ones. I added a fifth that matters to a voice engineer: **what still works when the risky part fails?**

| # | Filter | Why it matters |
|---|---|---|
| 1 | Real users and real calls before Oct 31, from Chandigarh | The submission form asks how long you've been building. Traction beats features. |
| 2 | Not what Bolna's customers already do | Judges see sales, support, collections and recruiting bots every week. |
| 3 | A moment someone *feels* within 20 s of video | Gets us past the written/video round. |
| 4 | Riskiest technical piece proven or killed in 48 h | We have 13 days, not 13 weeks. |
| 5 | **Graceful degradation**: a viable product even if the risky bet fails | Avoids a Day-3 pivot. |

### Scoring the serious contenders

✅ strong · 🟡 partial · ❌ weak

| Idea | 1 Real users | 2 Not Bolna-customer work | 3 20-s moment | 4 48-h de-risk | 5 Degrades well | YC story | Verdict |
|---|---|---|---|---|---|---|---|
| **CareCall + Kavach** | ✅ our own parents | ✅ | ✅ "Amma, this is a scam" | ✅ one merged-call test | ✅ check-in works without Kavach | ✅ YC RFS #7 names voice for older adults | **Pick** |
| Awaaz Research | ✅ run a real 100-person study | ✅ mostly | 🟡 dashboard of themes | ✅ | ✅ | ✅ (Listen Labs / Outset, phone-first for Bharat) | **Runner-up** |
| MolBhav | 🟡 real vendors need consent, no repeat users | ✅ | ✅ live haggle | ✅ | ✅ | 🟡 thin take-rate, TRAI rules | Backup #2 |
| Kavach alone | ✅ | ✅ | ✅ | ✅ | ❌ merge fails → nothing left | 🟡 | Absorbed into pick |
| Dubhashiya | ✅ | ✅ | ✅ | ❌ same merge test, plus translation latency | ❌ | 🟡 feature for big players | Reject |
| BeatBot / Vasooli / FirstCall | 🟡 | ❌ Bolna customers already do this | ✅ | ✅ | ✅ | ✅ | Reject (overlap) |
| Hamming for Bharat | 🟡 | ❌ competes with the host's "test & monitor" | 🟡 | ✅ | ✅ | ✅ | Reject (host conflict) |
| Saboot | ❌ enterprise pilot impossible in 13 days | ✅ | 🟡 | ✅ | ✅ | ✅ | Reject (no users in time) |
| PagerCall | ❌ own apps only | ✅ | ✅ | ✅ | ✅ | 🟡 | Reject (no users) |
| NightShift Saathi | 🟡 | ✅ | ✅ | ✅ | 🟡 | 🟡 liability | Reject |
| Kaun? | ✅ | ✅ | ✅ | 🟡 | ✅ | ❌ | Reject |

### Why CareCall + Kavach wins

1. **It's the only idea where every judging round has an answer.**
   - Written round: real families and real call counts.
   - Bolna interview: deep platform use, including custom LLM, scheduled outbound, multilingual, extraction, transfer, KB and webhooks.
   - Finale: a live scam being stopped on stage.
   - YC: it sits on YC's own request list, and there's a clear payer (the children).
2. **The risk is isolated.** The only scary unknown is how a Bolna agent behaves on a merged (conference) call. If it fails, Kavach falls back to "call Kavach afterwards" plus the daily check-in question *"Any strange calls today?"*. The core product is unaffected. No other high-wow idea degrades this gracefully.
3. **Real users are trivially reachable.** Team members' parents, grandparents and neighbours, today. Those users also generate the daily call volume that makes the metrics credible (20 parents × 1 call/day × 10 days ≈ 200 real calls).
4. **Voice isn't a gimmick here.** The users are elderly, often low-text, and phone-native. The threat (scams) arrives by phone call. A text or app product can't do either job.
5. **It doesn't collide with Bolna's customer base.** It's consumer and vertical, the gap the trackers call underserved.
6. **The two halves reinforce each other.** A parent who talks to CareCall every morning trusts the number and has it saved, so they'll actually merge it in a panic. A stranger's app wouldn't get that trust. The daily habit is the distribution channel for the safety feature.

### Why not the runner-up (Awaaz Research)?
It's the strongest pure-business story and the lowest risk. But the demo is a dashboard of themes, not a moment, and answer rates from unknown numbers can sink a 13-day study. Keep it as the backup if Day-2 tests show CareCall's voice quality with elderly speakers is unusable. That's unlikely, because Sarvam is tuned for exactly this.

---

## 2. Pros and cons of CareCall + Kavach

### Pros
- **Emotional, crore-scale problem.** ~₹4,058 cr lost to digital-arrest scams since 2022, mostly by the elderly. 41% of elders living alone report loneliness. 4–8 meds a day, and mistakes go unnoticed.
- **A clear payer with real willingness to pay:** adult children, especially in other cities or abroad (NRI pricing in USD). Later B2B2C via hospitals (post-discharge), insurers, banks and telcos.
- **No app for the parent.** Any phone works, including feature phones. Merging calls is a built-in phone feature.
- **Showcases Bolna deeply:** scheduled outbound with per-call `user_data`, `agent_language`, Sarvam STT/TTS with keyword biasing, extraction, call transfer, KB, webhooks, and a **custom LLM endpoint** (rarely shown at hackathons).
- **Compounding data moat:** daily longitudinal health/mood signals plus a scam-pattern corpus from real Indian calls.
- **Expansion path is obvious:** Haath (phone-in chores via browser agent), Kavach+ (ML scam and cloned-voice detection), care coordination and teleconsult booking.

### Cons (and what we do about each)
| Con | Severity | Mitigation |
|---|---|---|
| **Merged-call behaviour unknown:** two speakers on one channel, VAD constantly firing, agent may talk over people or hang up on "silence" | High for Kavach, none for CareCall | Day-0 spike. Our custom LLM endpoint decides when to speak. Fallback ladder in BUILD_PLAN §6.4. |
| **Elderly may not manage "Add call → Merge" under pressure.** Scammers also say "don't hang up, don't tell anyone". | Medium | Practice drill during onboarding, and Kavach as a *favourite* contact. Daily check-in asks about strange calls. "Call Kavach afterwards" mode. Kavach's spoken announcement alone often ends the scam. |
| **Video-call stage of digital arrest** (WhatsApp/Skype) can't be merged | Medium | Be honest in the pitch. Kavach catches the **first-stage phone call** (fake courier/TRAI/customs), where most cases start. The daily check-in catches the rest after the fact ("koi police/CBI wala call aaya?" — did any police or CBI caller ring you?). |
| **Unit economics:** per-minute voice cost × daily calls can exceed a ₹499 price | Medium | Price from measured cost (Day 0). Default 1 call/day of ~3 min. Plans at ₹999 India / $15 NRI. Pitch shows the cost curve falling. |
| **Consumer churn / "nice to have"** | Medium | Alerts that catch real events (missed meds, dizziness) create the "aha". Weekly voice digest to the child. Measure retention through the pilot. |
| **Medical liability** | Medium | Strictly reminders, logging and escalation. Never diagnose or advise doses. Red-flag symptoms → transfer to family / tell them to call 112. Disclaimers. |
| **Privacy and recording consent** (DPDP Act 2023) | Medium | Child and parent both consent. The parent gives verbal consent on the first call (recorded). Kavach announces recording on merge. OTP/Aadhaar-like digits redacted. Short retention. |
| **Elder-care space has players** (Emoha, Samarth, etc.) | Low | They are human-ops and app-based. None does daily vernacular AI phone calls plus in-call scam defence. |
| **Indian telephony friction:** number KYC, SMS DLT registration | Low–Med | Use Bolna/Plivo/Exotel numbers sorted Day 0. Alerts via WhatsApp/Telegram and **voice calls** instead of SMS. |

---

## 3. What I need from you to start (approval checklist)

1. ✅/❌ **Approve CareCall + Kavach** as the build (Awaaz Research as backup).
2. **Team:** how many people (1–4), and who's strongest at backend / frontend / voice / user ops?
3. **Languages for the pilot:** I'm assuming **Hindi + Punjabi + English** (Chandigarh). Add Tamil/Bengali etc. only if a real pilot parent needs it.
4. **Budget:** Bolna credits (ask on the Builders Slack), a phone number, and roughly ₹5–10k for calls + LLM during the pilot. OK?
5. **Alerts channel:** WhatsApp (Twilio sandbox / Meta Cloud API test number) plus Telegram fallback, plus voice-call alerts for urgent events. OK?
6. **Name:** "CareCall" for the product, "Kavach" for the scam shield. Or something more Indian, e.g. *Saathi* (companion)?

The full build document and day-by-day plan are in **[BUILD_PLAN.md](BUILD_PLAN.md)**.
