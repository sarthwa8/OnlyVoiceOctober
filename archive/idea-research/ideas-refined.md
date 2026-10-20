# Bolna Buildathon: Refined Ideas

> Updated 2026-10-18 · Submit by **Oct 31** · Shortlist emails Nov 3 · Interviews Nov 5–7 · Finalists announced Nov 8 · Top 3 pitch at Symphony, Bengaluru, **Nov 20** (winner gets a YC interview)
> Fully virtual until the finale. Team size 1–4. No tracks: anything goes as long as voice is part of it.

---

## 1. What the event page tells us about judging

- **Three hurdles:** a written/video submission, then an interview with the Bolna team, then a live pitch to the crowd with a YC interview as the prize.
- The application form asks *"Since when have you been working on this idea?"*, so they want builders, not idea people.
- **Real users and real calls by Oct 31 are worth more than extra features.** The stage demo can keep improving for 3 weeks after submission.

## 2. Corrections to the earlier docs

- **The YC narrative is wrong.** Bolna was accepted into **YC Fall 2025**. Drop the "YC rejected them 5×" framing.
- **Avoid overlapping with Bolna's customers.** Bolna's customers already automate calls for sales, support, collections and recruitment (Varun Beverages is one of them). BeatBot, Vasooli, FirstCall, TalkCRM and RolePlay Guru are what Bolna's judges see every week.
- **Hamming for Bharat competes with the host.** Bolna markets itself as letting enterprises "build, test, deploy and monitor" agents, so testing is on their own roadmap.
- **Kavach has a gap.** Digital-arrest scams usually escalate to WhatsApp or Skype *video* calls, and "Add call → Merge" only works on regular phone calls. Kavach catches the first-stage call (fake courier, TRAI, customs), not the video stage.
- The 1–5 scores in the earlier docs are self-graded and bunched together (18–24), so they don't help choose.

## 3. The filter: four yes/no questions

1. Can we get **real users or real calls before Oct 31**, from Chandigarh?
2. Is it something Bolna's customers **aren't** already doing?
3. Is there a moment someone can **feel within 20 seconds** of video?
4. Can we prove or kill the **riskiest technical piece within 48 hours**?

---

## 4. Shortlist

### A. CareCall + Kavach: one phone line for ageing parents
- **What:** Daily check-in calls in the parent's language (medicines, mood, symptoms, companionship), plus a scam shield the parent can merge into a suspicious call. The adult children get a dashboard and alerts.
- **Why one product:** The daily check-in builds the trust and habit that the scam shield depends on. Scam protection is the stage moment, and the children paying is the business model. It matches YC's request for AI for the aging population.
- **Real users:** Team families and friends' parents, 15–20 elderly users in week 1.
- **Bolna features:** Scheduled call campaigns, multilingual support with a per-user `agent_language`, data extraction from calls, call transfer to family or to the 1930 cybercrime helpline, a knowledge base of scam scripts, a custom model endpoint that decides when the agent stays silent, and web search.
- **Demo:** "Amma" gets her morning call and mentions dizziness → the son gets an alert. Then a fake "CBI officer" calls, Amma merges Kavach in, Kavach warns her in Hindi, and a WhatsApp alert reaches the family.
- **Pricing:** ₹499–999/month in India, $10–20/month for NRI children. Later, B2B through hospitals (post-discharge care), insurers and banks.
- **Risks:** Day-1 test: can a Bolna agent stay quiet on a merged call? Plus the video-call gap, consumer willingness to pay, and churn. Stick to reminders and escalation, and never give medical advice.
- **Optional depth:** see Kavach+ (§6.3) and Haath (§6.2).

### B. MolBhav: an agent that calls local vendors and negotiates
- **What:** "Packers and movers, 2BHK, Saturday." MolBhav calls about 10 vendors in parallel in their language, collects quotes, uses the best quote so far to haggle, and returns a ranked comparison with a one-tap booking.
- **Real users:** Real tasks around Mohali and Chandigarh (a PG move, a caterer, a tempo), with vendors' consent.
- **Bolna features:** Batch calls with per-call variables (`job_spec`, `best_quote`), a mid-call function call to fetch `get_best_quote()`, data extraction (price, GST, date), call transfer, and web search for market rates.
- **Demo:** Three "vendor" phones ring. The AI says "another vendor quoted ₹8,500", the vendor drops the price live, and the comparison table fills in.
- **Revenue:** 5–10% booking commission from vendors. B2B procurement later.
- **Risks:** Telemarketing rules (disclose that it's an AI, frame calls as on behalf of a customer), negotiation quality, and a thinner business model.

**Backup plan:** if the merged-call test fails on Day 1, MolBhav becomes the primary.

---

## 5. Ideas from other industries

### 5.1 Shaadi Saathi: RSVP and logistics calls for Indian weddings
- **Problem:** 300–1,000 guests, many of them elderly relatives who ignore WhatsApp forms. Families and planners phone everyone by hand for headcount, arrivals, rooms and pickups.
- **How it works:** Upload the guest list → calls in each guest's language (attending? how many? which train or flight? need a room or pickup? food preferences?) → a reminder call 2 days before with venue and timing → planner dashboard with headcount, an arrivals timeline for cab planning, and room allocation.
- **Buyer:** Wedding planners (per event), banquet halls, families. Corporate events later.
- **Bolna features:** Batch calls, a structured call flow, data extraction, per-guest `agent_language`, scheduled follow-ups.
- **Demo:** "Nani ji" answers in Punjabi, says 4 people are coming on the Shatabdi, and the dashboard updates.
- **Checks:** Real users easy (it's wedding season) · not Bolna-customer work ✓ · strong demo · low risk.
- **Weakness:** Seasonal, and it could be seen as a feature. Pitch it as an events platform.

### 5.2 Awaaz Research: AI-run voice surveys and user interviews
- **Problem:** Brands, NGOs and researchers need to hear from Bharat. Field surveys are slow and costly, and online forms miss non-English and low-literacy respondents. The US has funded AI-interview startups (Listen Labs, Outset), but they work through text and video, not phone calls in Indian languages.
- **How it works:** The researcher states their goals → the system generates a conversational interview guide → calls the respondents and asks follow-up questions → transcribes and codes the answers → a themes dashboard with audio clips as evidence.
- **Buyer:** Market research firms, consumer brands, NGOs (baseline and impact surveys), think tanks, and HR (worker pulse surveys).
- **Bolna features:** Batch calls, data extraction, call summaries, webhooks, multilingual support.
- **Demo:** Launch a study → 30 calls finish → theme clusters and representative quotes appear live.
- **Checks:** Real users very easy (run a real 100-person study before Oct 31) · mostly not Bolna-customer work · credible demo · low risk.
- **Weakness:** Low answer rates for unknown numbers. Fix: the client sends a pre-intro to respondents.

### 5.3 Dubhashiya: a live interpreter on any phone call
- **Problem:** Hindi-speaking rider and Kannada-speaking customer, migrant patient and Tamil-speaking doctor, landlord and tenant. Translation apps don't work in the middle of a phone call.
- **How it works:** Either person adds the Dubhashiya number to the call → it translates each turn → both sides get a transcript and summary.
- **Buyer:** Logistics and quick-commerce companies (failed deliveries), hospitals, consumers.
- **Bolna features:** Custom model endpoint, Indian-language speech recognition and voices, language detection.
- **Demo:** A Kannada speaker and a Hindi speaker hold a full conversation through Dubhashiya.
- **Checks:** Real users easy · not Bolna-customer work ✓ · very strong demo · **high risk, but it's the same Day-1 merged-call test as Kavach**.
- **Weakness:** Translation delay, and the big players could ship it as a feature.

### 5.4 RaktSetu: rapid blood-donor mobilisation
- **Problem:** Urgent requests for rare blood groups spread through WhatsApp groups and one-by-one calls that take hours. Donor lists exist (college clubs, NGOs, the government's e-RaktKosh portal), but nothing contacts donors quickly.
- **How it works:** Submit blood group, hospital and urgency → call matched donors in parallel → check eligibility on the call (last donation date, current health, can they reach the hospital in time) → confirm 2–3 donors → send directions and notify the requester.
- **Buyer:** Hospitals and blood banks, plus CSR/NGO contracts. Weakest business model of this group.
- **Bolna features:** Parallel calls, eligibility checks with structured answers, keypad confirmation, call transfer. **Same engine as MolBhav.**
- **Demo:** "O-negative, PGIMER, 3 hours." Ten phones ring and two donors confirm.
- **Checks:** Real users easy (PEC blood donation / NSS club) · not Bolna-customer work ✓ · emotional demo · low risk.

### 5.5 MachineDown: a breakdown line for MSME factories
- **Problem:** In the Ludhiana, Mohali and Baddi clusters, breakdowns are handled by shouting and phone calls. Downtime goes unrecorded, and repair history lives in technicians' heads.
- **How it works:** The operator calls and says "CNC 3 band, spindle se awaaz" ("CNC 3 stopped, noise from the spindle") → a ticket is created → the right technician gets a call → the operator confirms the fix by keypad → the owner gets a daily voice summary of downtime by machine → the repair history later suggests likely causes.
- **Buyer:** Factory owners with 20–200 workers.
- **Checks:** Needs a factory contact · not Bolna-customer work ✓ · weak demo · low risk. Close to FieldLog.

### 5.6 Kaun? A murder mystery you play by phone
- **What:** Players get a case file and 4 suspect phone numbers. Each suspect is an agent with secrets, an alibi and memory of what you've already asked. Contradictions leak across calls. Call the "inspector" to name the killer.
- **Buyer:** Corporate team-building, escape rooms, brand and film marketing campaigns, pay-per-episode consumers.
- **Bolna features:** Multiple agents, per-player memory between calls, distinct voices per character.
- **Demo:** The judges play it live on stage.
- **Checks:** Real users very easy · best crowd demo · medium risk (keeping the story consistent) · **weakest YC story**.

### 5.7 Tareekh: court hearing companion (parked)
- Calls litigants before each hearing in their language, explains the last order, lists documents to bring, and takes questions.
- Buyer: legal aid bodies, lawyers' offices, legal-tech platforms.
- Parked: real users are hard to get in 13 days, and accuracy and liability risk is high.

### Industry ideas at a glance
| Idea | Real users by Oct 31 | Demo | YC story | Overlap with shortlist |
|---|---|---|---|---|
| Awaaz Research | Easy | Medium | Strong | None |
| Shaadi Saathi | Easy | Strong | Medium | None |
| Dubhashiya | Easy | Very strong | Medium–strong | Same Day-1 test as Kavach |
| RaktSetu | Easy | Strong | Weak | Same engine as MolBhav |
| Kaun? | Easy | Very strong | Weak | None |
| MachineDown | Needs a contact | Weak | Medium | Close to FieldLog |
| Tareekh | Hard | Medium | Medium | Parked |

---

## 6. AI- and tech-oriented ideas

### 6.1 PagerCall: a voice agent for on-call incidents
- **What:** An alert fires → the agent has already investigated (logs, metrics, recent deploys) → it calls the on-call engineer: "Checkout errors at 12%, started 4 min after deploy #482, which touched the payment client." The engineer says "roll back" or "scale workers to 6" → confirmation by voice and keypad → the agent executes, keeps watching, and writes the postmortem timeline.
- **Tech core:** An agent that investigates before calling, voice tool calls into GitHub, Vercel or Kubernetes, safety confirmation on destructive actions, and a timeline built from the call.
- **Demo:** Break your own deployed app on stage → a phone rings → "roll back" → the site recovers live.
- **Buyer:** Engineering teams. PagerDuty, incident.io and Rootly have AI features, but you can't talk to your incident over a phone call.
- **Risk:** Hard to get real users by Oct 31. Use your own deployed projects.

### 6.2 Haath: phone call in, browser agent does the work
- **What:** "Pay my electricity bill" or "check my PF balance" by phone → an AI agent operates the real website in a browser, asks follow-up questions on the call, and calls back with the result.
- **Tech core:** Voice agent → task planner → browser-automation agent (Playwright or similar). Hands off to the human for one-time codes and payments. Calls back when tasks take too long to stay on the line.
- **Demo:** The caller speaks Hindi, and a government portal fills itself in on the projector.
- **Buyer:** Consumers first, then banks and telecom companies. Matches YC's request for consumer AI for a billion people. Fits with CareCall.
- **Risk:** Browser agents are flaky, CAPTCHAs block them, and many sites forbid automation. Pick 2–3 reliable portals and keep the human in the loop for payments.

### 6.3 Kavach+: models that detect scam calls and cloned voices
- **What:** Real ML behind Kavach: (a) a classifier that recognizes scam scripts in Hindi/English mixed speech from live transcripts, and (b) a cloned-voice detector that works on phone-quality audio, which public datasets mostly ignore.
- **Tech core:** Generate cloned speech with the sponsors' voice tools, downsample to phone quality, mix in noise, fine-tune a small audio model, and report honest metrics.
- **Demo:** A cloned "son" voice calls Mom, and Kavach flags it as a likely AI voice.
- **Risk:** Results may be mediocre in 13 days, and fake-voice detection is genuinely hard.

### 6.4 Bolta Machine: IoT devices that call you and take spoken commands
- **What:** An ESP32 with sensors on a pump, cold room or machine. When something looks wrong, it calls the owner: "Cold room 2 is at 9°C and rising, compressor current dropped. Switch to backup?" The owner can also call in: "Run the pump for 30 minutes."
- **Tech core:** Hardware, sensor data flow, anomaly detection, voice tool calls that send commands back to the device.
- **Demo:** A physical device on stage. Heat the sensor → a phone rings → "switch off" → the relay clicks.
- **Buyer:** Cold-chain operators, farmers (GSM pump controllers already sell, without AI), small factories.
- **Risk:** Hardware takes time, but the minimal kit is a weekend build.

### 6.5 AskYourData: phone a number, query your business data
- **What:** "How did Punjab sales do this week vs last week?" → a text-to-SQL agent queries the database → an answer that works by ear (one number, one insight) → a chart sent on WhatsApp.
- **Risk:** AI analytics tools are a crowded category, so it needs a specific user group (for example, distributors).

### 6.6 Dispatch: delegate coding tasks to an agent by phone
- **What:** "Fix the failing test on main and open a PR." A background coding agent works on it, then calls back: "PR #31 is open, tests pass. Merge?"
- **Risk:** The big AI labs and coding tools are shipping mobile access to their own agents, so this is a feature, not a company. Skip it.

### Tech ideas at a glance
| Idea | Tech depth | Demo | YC story | Real users by Oct 31 |
|---|---|---|---|---|
| PagerCall | High | Very strong | Strong | Your own apps only |
| Haath | High | Strong | Strong | Easy (parents) |
| Kavach+ (ML) | Very high | Strong | Strong (with CareCall) | Easy |
| Bolta Machine | High (hardware) | Very strong | Medium–strong | Needs a site |
| AskYourData | Medium | Medium | Weak | Medium |
| Dispatch | Medium | Medium | Weak | Easy |

---

## 7. Current read

- **Pure engineering product:** PagerCall.
- **Combined product:** **CareCall + Kavach+ + Haath**, one phone line for parents that checks in daily, catches scams with a real model, and does online chores. It covers ML depth, agentic depth, real users and a buyer (the children).
- **Backup:** MolBhav (shares its parallel-calling engine with RaktSetu).
- **Strongest new candidate for the YC interview:** Awaaz Research.
- **Day-1 test that decides several ideas at once:** can a Bolna agent behave well on a merged call? It decides Kavach and Dubhashiya.

---

## Sources
- [Bolna Buildathon page](https://www.bolna.ai/symphony/buildathon)
- [AIM: Bolna raises $6.3M (YC Fall 2025 cohort)](https://analyticsindiamag.com/ai-news-updates/bengaluru-voice-ai-startup-bolna-grabs-6-3-mn-to-enhance-vernacular-calls)
- [Inc42: Bolna raises ₹57 Cr (use cases: sales, support, collections, recruitment)](https://inc42.com/?p=545778)
- [Entrepreneur India: Bolna funding ("build, test, deploy and monitor")](https://india.entrepreneur.com/?p=92781)
- Earlier research and sources: the original `ideas.md` (25-idea bank) and `ideas (1).md` (top 5)
