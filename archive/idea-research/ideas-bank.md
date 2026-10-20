# Bolna Buildathon: Idea Bank (25 ideas)

> Compiled 2026-10-18 · Submission deadline **Oct 31** · Hackathon details: [hackathon-details.md](hackathon-details.md)
> Each card covers: problem · how it works · user · buyer · seller/GTM · business model · stack · Bolna features · demo · why now · moat/expansion · risks · scores.
> Scores (1–5): **V** value · **D** demo wow · **F** feasibility in 13 days · **B** Bolna fit · **Y** YC-ness

---

## 0. Quick reference

### Default tech stack (applies to every idea unless noted)
| Layer | Choice |
|---|---|
| Voice agent | **Bolna** (single-prompt or **graph agents**), API + MCP for setup |
| STT | **Sarvam saaras v4** (Indic + keyword biasing) or Deepgram / AssemblyAI U3 |
| TTS | **Sarvam Bulbul v4 Flash** (Hinglish code-mixed voices) or Cartesia / ElevenLabs v4 Turbo |
| LLM | GPT-4.1-mini / Claude via Bolna, or our own **custom LLM endpoint** (OpenAI-compatible) when we need control |
| Telephony | Bolna numbers or **Plivo / Exotel** (sponsors) via SIP trunk |
| Backend | **FastAPI** (Python) or Next.js API routes, receives Bolna **custom function calls + webhooks** |
| DB | **Supabase** (Postgres + realtime for live dashboards) |
| Frontend | **Next.js + Tailwind + shadcn/ui**, deployed on Vercel |
| Messaging | WhatsApp via Twilio / Gupshup sandbox, SMS via Plivo |
| Infra | Vercel (web), Railway/Render (API), ngrok for local webhooks |

### Bolna features cheat-sheet
Inbound/outbound calls · batch calls (CSV) · **Workflows + campaigns** (scheduled calling) · **graph agents** (node flows, extraction on edges) · **custom function calls** (REST mid-call) · Cal.com booking · **call transfer** · **web search tool** · knowledge base (URL/PDF) · **extractions/dispositions + call summary** · webhooks · **Web Call SDK** (browser) · DTMF keypad input · multilingual auto-switch + `agent_language` · custom LLM / custom TTS · SIP trunks.

### All ideas at a glance
Numbering matches the cards below and is roughly by priority. Totals: **24** BeatBot · **22** Hamming for Bharat, Saboot, Vasooli, FirstCall, ServiceTitan for India, FieldLog · **21** Kavach, CareCall, MolBhav, NightShift Saathi, Procuro India, Phone Primer.

| # | Idea | One-liner | V | D | F | B | Y | Total |
|---|---|---|---|---|---|---|---|---|
| 1 | **BeatBot** | AI sales rep calls kiranas for reorders | 5 | 4 | 5 | 5 | 5 | **24** |
| 2 | **Hamming for Bharat** | Simulated Indian callers stress-test voice agents | 4 | 4 | 4 | 5 | 5 | **22** |
| 3 | **Saboot** | AI verification calls prove informed consent in BFSI sales | 5 | 4 | 4 | 4 | 5 | **22** |
| 4 | **Kavach** | AI joins the call when a parent is being scammed | 5 | 5 | 3 | 4 | 4 | **21** |
| 5 | **CareCall** | Daily check-in calls for ageing parents + family app | 5 | 4 | 4 | 4 | 4 | **21** |
| 6 | **MolBhav** | Agent calls 10 local vendors, gets quotes, haggles | 4 | 5 | 4 | 4 | 4 | **21** |
| 7 | **Vasooli** | Polite, persistent payment-collection calls for MSMEs | 5 | 3 | 5 | 5 | 4 | **22** |
| 8 | **FirstCall** | Calls every property lead in 60s, paid per site visit | 4 | 4 | 5 | 5 | 4 | **22** |
| 9 | **HoldForMe** | AI calls customer care for you and fights for refunds | 4 | 5 | 3 | 4 | 4 | **20** |
| 10 | **NightShift Saathi** | AI stays on the call with women commuting at night | 5 | 5 | 4 | 4 | 3 | **21** |
| 11 | **ServiceTitan for India** | AI office for home-services SMBs | 4 | 4 | 4 | 5 | 5 | **22** |
| 12 | **Procuro India** | AI buyer calls 50 suppliers for quotes | 4 | 4 | 4 | 4 | 5 | **21** |
| 13 | **FieldLog** | Daily phone reporting for field workers | 5 | 3 | 5 | 5 | 4 | **22** |
| 14 | **Phone Primer** | Call-in reading/maths tutor for kids | 5 | 4 | 4 | 4 | 4 | **21** |
| 15 | **TalkCRM** | Field reps update CRM by talking | 4 | 3 | 5 | 4 | 4 | **20** |
| 16 | **School Saathi** | Absence/dropout calls to non-literate parents | 5 | 3 | 5 | 4 | 3 | **20** |
| 17 | **ClaimSaathi** | Health-insurance claim companion | 4 | 3 | 4 | 4 | 4 | **19** |
| 18 | **Bolo Forms** | One script tag makes any web form voice-fillable | 4 | 4 | 3 | 4 | 4 | **19** |
| 19 | **Asli** | Anti-deepfake callback verification for payments | 4 | 4 | 4 | 3 | 4 | **19** |
| 20 | **RolePlay Guru** | AI plays tough customers to train sales agents | 4 | 3 | 5 | 4 | 3 | **19** |
| 21 | **GaadiSaathi** | Voice load board + trip check-ins for truckers | 4 | 3 | 4 | 4 | 4 | **19** |
| 22 | **KisanBid** | Farmer lists produce by phone, AI collects trader bids | 4 | 4 | 4 | 4 | 3 | **19** |
| 23 | **DawaiDhoondo** | Generic-medicine finder + chemist stock calls | 4 | 3 | 4 | 4 | 3 | **18** |
| 24 | **Bolo Bazaar** | A phone number that buys anything (ONDC + UPI 123PAY) | 4 | 4 | 2 | 4 | 4 | **18** |
| 25 | **108 Co-Pilot** | Overflow triage + first-aid guidance for ambulance lines | 5 | 4 | 3 | 4 | 2 | **18** |

**Top picks:** 🏆 Safest/YC: **BeatBot** · Infra/judge-pleaser: **Hamming for Bharat** · Regulation tailwind: **Saboot** · Win the room: **Kavach** / **NightShift Saathi** · Matches YC's request list: **CareCall**, **Phone Primer**.

---

## 1. Research context (short)
- **What wins voice hackathons:** agents that *act* (call businesses, negotiate, chase: Dealwise, Procuro, Claimsio), safety/guardian agents (Roadmate, Voice Guardian), Indic/underserved (Sarvam hack winners), voice layers on existing software (Unstuck).
- **Bolna's DNA:** India, multilingual, telephony-first. 200K+ calls/day, 1,050+ customers (Spinny, Snabbit, Varun Beverages). YC rejected them 5× on "Indian SMBs won't pay", so **show willingness to pay**.
- **YC Fall 2026 RFS that voice fits:** #1 The Primer (AI tutor), #6 consumer AI for 1B people, **#7 AI for the aging population (voice explicitly)**, #8 OS for physical world, #11 proving you're human, #12 AI-native compliance.
- **Gaps:** Indian voice AI is concentrated in CX bots and dev APIs. Vertical, field-ops and consumer products are underserved.

---

## 2. Idea cards

### 1. 🛒 BeatBot: AI sales rep for kirana reorders
- **One-liner:** FMCG distributors replace or augment the weekly salesman visit with a personalised vernacular call that recalls last order, pitches schemes, and books the reorder.
- **Problem:** 12M+ kiranas. Reorders are captured on fixed beat days via diaries, apps or WhatsApp voice notes. Outlets that run out mid-week lose sales. Shopkeepers won't use apps but always pick up the phone. A rep visit is the costliest way to take a routine order.
- **How it works:** Upload retailer list + SKU catalog + history → scheduled campaign calls each retailer → "Same as last week? Buy-10-get-1 on Sting" → live stock/price checks → read-back + DTMF confirm → order lands on dashboard + WhatsApp invoice/UPI link. Retailers can also call in anytime.
- **User:** kirana owners (respond) + distributor ops (dashboard).
- **Buyer:** FMCG distributors; later FMCG brands for their whole network (HUL, ITC, Dabur, Varun Beverages, which is a Bolna customer).
- **Seller/GTM:** founder-led sales to distributors in one city → brand partnerships for top-down rollout → distributor associations.
- **Business model:** SaaS ₹3–10K/distributor/month + per-order fee. ROI: one rep costs ₹15–25K/month for ~40 outlets/day.
- **Stack extras:** Google Sheet as mock DMS, fuzzy SKU matcher (rapidfuzz), WhatsApp invoice.
- **Bolna features:** graph agent (greet → recall → upsell → line-item loop → confirm), workflows/campaigns, batch CSV with `agent_language`, custom functions (`get_last_order`, `check_stock`, `create_order`), KB (catalog/schemes), keyword biasing for SKUs, DTMF.
- **Demo:** Upload CSV → "Run beat" → 3 phones ring → orders in Hindi and Kannada stream onto dashboard → WhatsApp invoices arrive live.
- **Why now:** cheap Indic STT/TTS, Bolna workflows, quick-commerce pressure on general trade.
- **Moat/expansion:** order history + retailer behaviour data → demand forecasting → retailer credit → full AI sales force for general trade.
- **Risks:** messy SKU speech (fix with fuzzy match + read-back). DMS integrations (Sheet for MVP).
- **Scores:** V5 D4 F5 B5 Y5

### 2. 🧪 Hamming for Bharat: QA for Indian voice agents
- **One-liner:** 1,000 simulated Indian callers (Hinglish, accents, market noise, interruptions, mid-call language switches) stress-test your voice agent before launch and score every failure.
- **Problem:** Voice agents break on Indian reality: code-mixing, numbers, noise, interruptions. US tools (Coval $28M Series A, Hamming YC S24) don't model India.
- **How it works:** Paste agent phone number/ID + goals → generate persona matrix (language × accent × noise × behaviour) → swarm of caller agents dial in → transcripts scored (task success, hallucination, wrong numbers, latency, language errors) → regression suite + production monitoring.
- **User:** voice-AI engineers / PMs.
- **Buyer:** companies deploying voice agents (Bolna's 1,050+ customers, BPOs migrating to AI, banks).
- **Seller/GTM:** partnership/marketplace listing with Bolna and other voice platforms, dev-led PLG, content ("India voice agent failure benchmark").
- **Business model:** usage-based per simulated minute + monitoring subscription. Enterprise compliance tier.
- **Stack extras:** persona generator (LLM), noise mixing (custom TTS server that overlays market/traffic noise), LLM-as-judge scoring, results dashboard.
- **Bolna features:** outbound batch calls from *caller* agents, custom TTS (noisy/accented voices), multilingual personas, extractions for scoring, MCP/API to target Bolna agents.
- **Demo:** Point at any Bolna agent → 20 fake callers dial at once → dashboard fills with failures ("misheard ₹1,500 as ₹15,000 in Hindi") → one-click re-test after prompt fix shows score jump.
- **Why now:** voice agent deployments in India are exploding. Proven US category, no India player.
- **Moat/expansion:** largest library of real Indian failure cases → monitoring → "certified safe to deploy" compliance standard.
- **Risks:** judges may see it as a dev tool rather than end-user value (counter with BPO/bank pain). Cost of many simultaneous calls.
- **Scores:** V4 D4 F4 B5 Y5

### 3. ✅ Saboot: proof-of-consent calls for BFSI sales
- **One-liner:** After every insurance policy, loan or card sale, an AI calls the customer in their language, explains key terms, checks understanding, records consent, and flags mis-selling before the free-look window ends.
- **Problem:** Mis-selling is rampant. RBI's draft conduct directions shift from "did we disclose?" to "can we *prove* informed choice?" The free-look period is now up to 30 days. Insurers already run human pre-issuance verification / welcome calls (verify the exact IRDAI rule).
- **How it works:** Sale event via API/CSV → AI calls within hours → explains lock-in, premiums, exclusions → asks comprehension questions → captures explicit consent (voice + DTMF) → risk score → compliance dashboard + audit pack; mis-sold cases routed to retention/cancellation.
- **User:** policyholders/borrowers (calls), compliance teams (dashboard).
- **Buyer:** life/health insurers, NBFCs, banks, card issuers (CCO/compliance head).
- **Seller/GTM:** enterprise sales to compliance heads, regulator-driven urgency, partnerships with insurance distribution platforms (PolicyBazaar-type).
- **Business model:** per verified sale (₹20–60) + enterprise platform fee.
- **Stack extras:** policy-term extraction from PDFs (LLM), audit-trail storage (signed recordings + transcripts), risk-scoring rules.
- **Bolna features:** outbound batch/workflows, KB per product, graph agent for scripted disclosure + Q&A, DTMF consent, extractions (`understood_lock_in`, `consent_given`), call recordings, webhooks.
- **Demo:** "Sell" a teammate a policy → Saboot calls → "Did the agent tell you about the 5-year lock-in?" → "No…" → mis-selling alert with clip on dashboard.
- **Why now:** RBI/IRDAI conduct push. Voice AI now cheap enough for 100% coverage.
- **Moat/expansion:** regulator-grade audit trails, insurer integrations → 100% sales-call QA → compliance OS for financial sales (matches YC's compliance RFS).
- **Risks:** long enterprise sales cycles. Regulatory specifics must be verified.
- **Scores:** V5 D4 F4 B4 Y5

### 4. 🛡️ Kavach: anti-scam guardian for parents
- **One-liner:** When a "CBI officer" calls Mom, she taps *Add call → Kavach → Merge*. Kavach listens, recognises the digital-arrest script, warns her in her language, and alerts the family.
- **Problem:** ~₹4,058 cr lost to digital-arrest scams (2022–May 2026, ~2.98 lakh complaints), mostly elderly. Victims are isolated on the call for hours.
- **How it works:** Family registers parent + WhatsApp → parent merges Kavach into a suspicious call (works on any phone, no app) → custom-LLM gate stays quiet and scores against scam playbook → speaks up when risky → WhatsApp alert + optional transfer to family or 1930 → fallback "call Kavach after" mode with web-search verification.
- **User:** elderly parent. **Buyer:** adult children (consumer subscription); later banks, telcos, insurers (B2B2C).
- **Seller/GTM:** viral consumer content (scam stories), bank/telco partnerships, senior communities, RWAs.
- **Business model:** ₹99–199/month family plan. B2B2C per-user fees from banks/telcos.
- **Stack extras:** FastAPI custom-LLM proxy (OpenAI-compatible, streaming) that controls silence, scam-script KB from I4C/RBI advisories, family dashboard.
- **Bolna features:** inbound number, custom LLM, KB, keyword biasing (CBI, ED, TRAI, Aadhaar, parcel), call transfer, web search, extractions (scam type, amount, agency).
- **Demo:** Teammate "CBI officer" calls "parent" → merge Kavach → Kavach interrupts in Hindi → WhatsApp alert pops on projected phone.
- **Why now:** digital-arrest crisis, Supreme Court attention, cheap real-time voice AI.
- **Moat/expansion:** scam-pattern database from every call → CareCall-style parent companion → telco-level scam shield.
- **Risks:** ⚠️ merged-call audio (two speakers, constant VAD), so **validate Day 1**. Recording-consent framing.
- **Scores:** V5 D5 F3 B4 Y4

### 5. 👵 CareCall: voice companion for ageing parents
- **One-liner:** Daily calls to parents in their language (meds, mood, symptoms, companionship, scam warnings) with a dashboard and alerts for their children.
- **Problem:** India's 60+ population heads to ~193M by 2031. 41% of elders living alone report loneliness. Many take 4–8 meds a day. ~10% of Indians are untrained family caregivers. Children often live in other cities or abroad.
- **How it works:** Child sets meds, routines and contacts → scheduled morning/evening calls → conversational check-in + med confirmation → extractions (took meds, pain, mood, falls) → alerts (missed meds ×2, dizziness) → book doctor/lab via functions → weekly voice summary to family.
- **User:** parents. **Buyer:** adult children (NRI pricing), later hospitals (post-discharge), insurers, senior-living operators.
- **Seller/GTM:** NRI communities, direct-to-consumer ads, hospital discharge partnerships, corporate employee-benefit plans.
- **Business model:** ₹499–999/month (India) / $10–20/month (NRI). B2B per-patient fees.
- **Stack extras:** family mobile-friendly web app, symptom rules engine, optional wearable integration later.
- **Bolna features:** workflows (daily schedule), multilingual + `agent_language`, extractions, call transfer to family/doctor, Cal.com/custom booking functions, memory via `user_data` context.
- **Demo:** "Amma" gets her morning call, mentions dizziness in Tamil → son's phone shows alert + suggested appointment.
- **Why now:** YC RFS #7 names voice interfaces for older adults.
- **Moat/expansion:** daily relationship + longitudinal health data → care coordination marketplace → insurer partnerships. Kavach becomes a feature.
- **Risks:** medical advice liability (stick to reminders + escalation). Churn.
- **Scores:** V5 D4 F4 B4 Y4

### 6. 🤝 MolBhav: AI negotiator for local services
- **One-liner:** "Packers & movers, 2BHK, Saturday": MolBhav phones 10 vendors in parallel in their language, gets quotes, haggles, and returns a ranked comparison.
- **Problem:** India's local services run on phone calls. No online pricing, quotes vary 2–3×, and getting three quotes takes hours.
- **How it works:** User describes the need → vendor numbers from Google Places / list → outbound batch with job spec → agent negotiates using best-quote-so-far → extractions build comparison card → "Book" triggers confirm call or warm transfer.
- **User:** urban consumers. **Buyer:** vendors (commission) or consumers (concierge). B2B SMB procurement later.
- **Seller/GTM:** consumer app + WhatsApp, SEO for "movers near me", vendor onboarding.
- **Business model:** lead/booking commission 5–10%. Premium concierge.
- **Stack extras:** Google Places API, live comparison board (Supabase realtime).
- **Bolna features:** batch calls with dynamic vars (`job_spec`, `best_quote`), mid-call `get_best_quote()` function, extractions (price, GST, date), call transfer, web search for market rates.
- **Demo:** Type request → 3 "vendor" phones ring → AI anchors "another vendor quoted ₹8,500…" → price drops live → table fills.
- **Why now:** proven winning format (Dealwise/Procuro), localised.
- **Moat/expansion:** local price index → vendor marketplace → B2B procurement (see Procuro India).
- **Risks:** TRAI/unsolicited-call rules (AI disclosure, transactional framing). Negotiation quality.
- **Scores:** V4 D5 F4 B4 Y4

### 7. 💰 Vasooli: receivables collection for MSMEs
- **One-liner:** Connect invoices; AI calls buyers' accounts teams with escalating, polite reminders, negotiates a pay date, sends a UPI link, and follows up on broken promises.
- **Problem:** ~₹8.1 lakh cr of MSME payments delayed. Average 73 days to pay vs the 45-day legal limit. ₹21k cr pending on MSME Samadhaan. Owners hate chasing.
- **How it works:** Import from Tally/Sheet → cadence (reminder → firm → cite MSMED 45-day rule + interest) → capture promise-to-pay → UPI link via WhatsApp → recall on due date → escalation draft for MSME Samadhaan → cash-flow forecast dashboard.
- **User:** MSME owner/accountant. **Buyer:** MSMEs, CA firms (for their clients), invoice-discounting platforms.
- **Seller/GTM:** CA networks, Tally ecosystem, MSME associations, fintech partnerships (TReDS players).
- **Business model:** ₹1–5K/month + % of recovered overdue (1–2%).
- **Stack extras:** Tally/Sheet import, Razorpay/UPI payment links, forecasting chart.
- **Bolna features:** workflows/campaigns, extractions (`promise_date`, `amount`, `dispute_reason`), webhooks, multilingual per buyer, call transfer to owner on dispute.
- **Demo:** Upload 5 overdue invoices → calls go out → "buyer" promises Friday → dashboard shows expected inflow; on "Friday" (simulated) the follow-up call fires automatically.
- **Why now:** MSME Development (Amendment) Bill 2026 tightens payment discipline. Similar to Claimsio (hackathon winner).
- **Moat/expansion:** buyer payment-behaviour data → credit scoring → invoice financing.
- **Risks:** collection-harassment norms (keep it polite, B2B only).
- **Scores:** V5 D3 F5 B5 Y4

### 8. 🏠 FirstCall: speed-to-lead agency for real estate
- **One-liner:** Every portal/ad lead gets called within 60s in their language, qualified, and booked for a site visit. The developer pays per visit that happens.
- **Problem:** Buyers enquire on many properties at once, so first caller wins. Vendor case: 24h+ response → 8% lead-to-visit. Fast AI calling → 25%.
- **How it works:** Webhook from 99acres/MagicBricks/Meta lead forms → instant call → qualify (budget, BHK, location, timeline, loan) → book visit (Cal.com) → reminders day-before/same-day → no-show recovery → CRM sync.
- **User:** home buyers. **Buyer:** real-estate developers, large brokerages; later edu admissions, auto dealers (Spinny is a Bolna customer).
- **Seller/GTM:** outcome-based pilots with developers ("pay only per visit"), channel partners, real-estate marketing agencies.
- **Business model:** ₹500–1,500 per completed site visit, or SaaS + per-minute.
- **Stack extras:** lead-ingest webhooks, CRM sync (LeadSquared/Sell.do mock), funnel analytics.
- **Bolna features:** API-triggered outbound call, Cal.com booking, workflows for reminders, extractions (budget, intent score), call transfer to sales on hot leads.
- **Demo:** Submit fake lead form on stage → phone rings <60s → visit booked → calendar invite + WhatsApp confirmation appear.
- **Why now:** "AI-operated agency" (YC Spring '26). Portal lead costs rising.
- **Moat/expansion:** conversion data by city × language × script → horizontal AI SDR for Indian lead-gen verticals.
- **Risks:** crowded with call-automation vendors, so differentiate on outcome pricing + vernacular quality.
- **Scores:** V4 D4 F5 B5 Y4

### 9. 📞 HoldForMe: your agent vs customer care
- **One-liner:** "Get my ₹2,400 IndiGo refund." The AI calls the helpline, navigates the IVR, waits on hold, argues your case, and reports back, escalating to a National Consumer Helpline complaint if needed.
- **Problem:** NCH processed 1.66 lakh refund grievances (₹105 cr, 2025–26), 1 lakh in e-commerce. IVRs and hold times are brutal. Businesses deploy AI; consumers have none.
- **How it works:** User gives company + issue + docs → agent calls support → IVR navigation → waits → negotiates with policy knowledge (web search) → extracts ticket ID/promise → follow-up calls → drafts NCH/consumer forum complaint → warm-transfers user when identity verification is needed.
- **User/Buyer:** consumers (freemium). Later fintech/credit-card apps embedding it as a perk.
- **Seller/GTM:** viral consumer launch ("I made an AI fight Airtel"), Reddit/X, browser extension.
- **Business model:** freemium + % of refund recovered (10–20%) or ₹99/case.
- **Stack extras:** company helpline directory, IVR map cache, complaint-draft generator.
- **Bolna features:** outbound calls, web search, extractions (ticket ID, promised date), workflows for follow-ups, call transfer (patch user in).
- **Demo:** Agent navigates a mock IVR (teammate-built), waits on hold, calmly secures a refund promise from the "support agent".
- **Why now:** Sierra does B2B IVR navigation; the consumer side is open.
- **Moat/expansion:** IVR maps + resolution playbooks per company → consumer "AI concierge for every phone chore".
- **Risks:** ⚠️ confirm Bolna can **send** DTMF (only receiving is documented). Identity verification needs the user.
- **Scores:** V4 D5 F3 B4 Y4

### 10. 🌙 NightShift Saathi: AI ride companion for women
- **One-liner:** Starting a night cab, the AI calls and talks like a friend tracking you (audible deterrent). If you say a code word, go silent, or the route deviates, it alerts contacts/employer security/112.
- **Problem:** Most SOS incidents 11pm–2am (Bengaluru Suraksha). Fake-call apps are scripted and obvious. Employers must ensure safe night transport for women staff.
- **How it works:** Trip start (app/link) → AI calls → natural conversation with live trip context → check-ins every few minutes → code word/silence/route anomaly → silent escalation (WhatsApp location to contacts, transfer to security desk, 112 script).
- **User:** women commuters/night-shift employees. **Buyer:** BPO/IT employers (transport compliance), ride/fleet operators, consumers.
- **Seller/GTM:** HR/admin heads at BPOs/IT parks, employee-transport vendors, women's safety campaigns.
- **Business model:** B2B ₹50–150/employee/month. Consumer freemium.
- **Stack extras:** trip-tracking web page (geolocation), route-deviation check (Maps API), security-desk dashboard.
- **Bolna features:** outbound call on trip start, Web Call SDK option, extractions (danger flag), custom functions (location update), call transfer to security/contacts.
- **Demo:** "Ride" starts → AI chats naturally → teammate says code word → security dashboard flashes + contacts get WhatsApp with location within seconds.
- **Why now:** realistic real-time voice makes "someone is on the line" believable.
- **Moat/expansion:** employer compliance integrations → broader personal-safety platform.
- **Risks:** false alarms, life-safety liability (position as an assistive layer).
- **Scores:** V5 D5 F4 B4 Y3

### 11. 🔧 ServiceTitan for India: AI office for home-services SMBs
- **One-liner:** AI front desk + dispatcher for AC/RO/pest/plumbing/electrical businesses: answers every call, books jobs, briefs technicians in Hindi, collects payment, requests a review.
- **Problem:** Small service businesses run on phone/WhatsApp with no software, and missed calls are lost jobs.
- **How it works:** Inbound AI receptionist → job created (address, issue, slot) → technician called with job details → "job done" call/DTMF → invoice + UPI link → Google review request → AMC renewal reminders.
- **User:** customers + technicians. **Buyer:** home-services business owners (5–50 techs).
- **Seller/GTM:** IndiaMART/JustDial listings outreach, trade associations, equipment brands' service networks.
- **Business model:** ₹2–5K/month + payments take-rate.
- **Stack extras:** job board/dispatch UI, payment links, review links.
- **Bolna features:** inbound + outbound, graph agents, custom functions (create job, assign tech), Cal.com slots, multilingual, call transfer.
- **Demo:** Customer calls "AC thanda nahi kar raha" → job created → tech's phone rings with Hindi brief → "done" → invoice + UPI arrive.
- **Why now:** YC funded CentralComs (US). Matches YC RFS #8 (OS for physical work).
- **Moat/expansion:** system of record → payments → AMC contracts → financing (ServiceTitan path).
- **Risks:** low ACV, fragmented market.
- **Scores:** V4 D4 F4 B5 Y5

### 12. 🏭 Procuro India: AI procurement caller
- **One-liner:** "500 kg SS304 sheets, 2mm, Pune by Friday": AI calls suppliers, gets quotes, negotiates, and returns a comparison.
- **Problem:** MSME and contractor purchasing is phone-only and suppliers don't publish prices.
- **How it works:** RFQ form → supplier list (IndiaMART scrape/own DB) → parallel outbound calls → negotiate → extractions → comparison + PO draft.
- **User:** purchase managers. **Buyer:** manufacturers, EPC/construction contractors.
- **Seller/GTM:** industrial clusters (Pune, Ludhiana, Rajkot), CA/consultant networks.
- **Business model:** per RFQ (₹200–500) or % of savings.
- **Stack extras:** supplier DB, RFQ parser, PO generator.
- **Bolna features:** batch calls + dynamic vars, extractions (price, MOQ, lead time), web search, call transfer.
- **Demo:** Submit RFQ → 3 "suppliers" called → live haggle → comparison table + PO.
- **Why now:** Procuro (US) was a hackathon winner. B2B version of MolBhav.
- **Moat/expansion:** proprietary industrial price index → ordering → supplier financing → B2B marketplace.
- **Risks:** supplier data quality. Spec complexity.
- **Scores:** V4 D4 F4 B4 Y5

### 13. 📋 FieldLog: phone-call reporting for field teams
- **One-liner:** Every evening site supervisors / ASHA workers / delivery leads get a 2-minute call. Spoken answers become structured reports, dashboards and instant escalations.
- **Problem:** Field reporting is paper registers or WhatsApp chaos. Owners lack daily visibility. ASHA workers spend hours on registers.
- **How it works:** Pick template or custom checklist → auto-generated graph agent → scheduled daily calls → typed extractions → rules (incident → owner call; low cement → supplier message; high-risk pregnancy → PHC) → dashboard + weekly AI digest.
- **User:** field workers. **Buyer:** construction firms, logistics, security agencies, NGOs/NHM.
- **Seller/GTM:** pick one vertical (construction or ASHA); builder associations, CSR/NGO partners, state health missions.
- **Business model:** ₹100–300/worker/month. Government contracts.
- **Stack extras:** checklist → graph-agent generator via Bolna API, rules engine.
- **Bolna features:** `create_graph_agent` via API/MCP, `allowed_values` extraction, workflows + execution webhooks, DTMF numbers, multilingual.
- **Demo:** Build "construction" template in 30s → supervisors' phones ring → incident reported in Hindi → owner escalation + dashboard update in seconds.
- **Why now:** YC RFS #8, Bolna graph-agent extraction updates (Oct 2026).
- **Moat/expansion:** operational data per site → benchmarks → AI site manager.
- **Risks:** less "wow". Must pick one vertical story.
- **Scores:** V5 D3 F5 B5 Y4

### 14. 📚 Phone Primer: call-in tutor for kids
- **One-liner:** A 15-minute daily phone call that teaches reading and arithmetic in the child's mother tongue, adapts to level, and reports to parents/teachers. No smartphone needed.
- **Problem:** ASER surveys repeatedly show large learning gaps in foundational reading/maths. Many homes have only a basic phone.
- **How it works:** Child calls (or scheduled call) → level check → phonics/reading/maths drills with adaptive difficulty → praise + spaced repetition → SMS progress to parent → teacher dashboard.
- **User:** children 5–10. **Buyer:** state education departments, NGOs (Pratham), CSR funds, low-cost private schools; later parents.
- **Seller/GTM:** NGO pilots → government MoUs → CSR-funded scale.
- **Business model:** per child per year (₹200–600) paid by government/CSR. Consumer premium.
- **Stack extras:** curriculum graph (levels, items), progress store, teacher dashboard.
- **Bolna features:** inbound + scheduled outbound, graph agent per lesson, extractions (correct/incorrect, level), multilingual, slow/clear TTS voices.
- **Demo:** "Child" reads a Hindi sentence, stumbles, AI breaks into phonemes, retries succeed, parent gets progress SMS.
- **Why now:** YC RFS #1 "The Primer". Indic speech now good on phone lines.
- **Moat/expansion:** per-child learning data → English, exam prep → Bharat edtech at feature-phone scale.
- **Risks:** child speech recognition accuracy. Safeguarding.
- **Scores:** V5 D4 F4 B4 Y4

### 15. 🎙️ TalkCRM: voice CRM updates for field sales
- **One-liner:** After each visit the rep gets a 60-second call ("Kya hua meeting mein?") and the CRM updates itself. Managers get an evening voice briefing.
- **Problem:** Millions of field reps (insurance, pharma, FMCG, lending) hate typing, so CRM data is garbage.
- **How it works:** Visit check-out triggers a call → rep debriefs in Hinglish → extractions (next step, value, objections, competitor) → CRM write → manager digest call.
- **User:** reps. **Buyer:** sales heads at companies with field forces.
- **Seller/GTM:** CRM marketplaces (LeadSquared, Zoho, Salesforce AppExchange), pharma/BFSI sales ops.
- **Business model:** ₹300–800/rep/month.
- **Stack extras:** CRM connectors (mock LeadSquared), manager digest generator.
- **Bolna features:** API-triggered outbound, extractions, call summary, workflows (daily digest).
- **Demo:** Rep talks 40s in Hinglish → fully populated CRM record appears.
- **Moat/expansion:** field-sales intelligence → coaching (RolePlay Guru) → AI sales manager.
- **Risks:** CRM integration depth. Crowded "voice notes to CRM" space.
- **Scores:** V4 D3 F5 B4 Y4

### 16. 🏫 School Saathi: voice outreach to parents
- **One-liner:** Absence alert *calls* in the parent's dialect capture the reason, flag dropout risk, and deliver weekly learning tips and PTM reminders.
- **Problem:** Text apps (HP e-Samwad) reached 53% of parents in pilot, and non-literate parents are left out. UP primary dropout rose 3.7% → 9.7% (2018–21). Delhi now mandates phoning parents of out-of-school kids.
- **How it works:** Attendance feed → same-day call → reason captured (illness/migration/work) → risk score → teacher/headmaster alerts → weekly tips → PTM reminders.
- **User:** parents. **Buyer:** state education departments, NGOs, CSR.
- **Seller/GTM:** district pilots, NGO partnerships, education ministries.
- **Business model:** per-student/year government contract.
- **Stack extras:** attendance CSV/API ingest, risk model, district dashboard.
- **Bolna features:** workflows/campaigns, dispositions (reason categories), multilingual, call summary.
- **Demo:** Mark child absent → parent's phone rings in Bhojpuri → "migration" reason → dropout-risk flag on teacher dashboard.
- **Moat/expansion:** student-risk data → Phone Primer upsell → govt citizen-outreach platform.
- **Risks:** govt sales cycles. Data privacy for minors.
- **Scores:** V5 D3 F5 B4 Y3

### 17. 🏥 ClaimSaathi: health-insurance claim companion
- **One-liner:** Upload your policy and get coverage answers by phone in your language. The AI chases TPA/insurer against IRDAI's 1h/3h timelines and drafts grievances when rejected.
- **Problem:** ~8% of claims rejected. 1.37 lakh insurance grievances (FY25). Families don't understand sub-limits/co-pay. Cashless disputes (e.g. Telangana hospitals suspending one insurer).
- **How it works:** Policy PDF → KB → patient family calls with questions → claim tracker → outbound chase calls to TPA → timeline breach alerts → Bima Bharosa grievance draft.
- **User:** patients' families. **Buyer:** consumers, hospitals (TPA desk automation), corporate HR (employee benefit).
- **Seller/GTM:** hospital billing desks, insurance brokers, HR benefits platforms.
- **Business model:** per-claim fee or % of recovered amount. B2B per-bed SaaS for hospitals.
- **Stack extras:** policy parser, claim timeline tracker, grievance generator.
- **Bolna features:** KB (PDF), inbound Q&A, outbound chasing workflows, extractions, web search for IRDAI rules.
- **Demo:** "Is my knee surgery covered?" → precise answer citing sub-limit → simulated TPA call → grievance PDF generated.
- **Moat/expansion:** claim-outcome data → claims advocacy marketplace → hospital RCM.
- **Risks:** TPAs may not engage with AI callers. Accuracy of policy interpretation.
- **Scores:** V4 D3 F4 B4 Y4

### 18. 🧩 Bolo Forms: voice-fill any web form
- **One-liner:** One script tag: users tap 🎙️, speak in Tamil/Bhojpuri, and the form fills live with explanations and validation.
- **Problem:** Long English forms kill funnels (loans, insurance, KYC, schemes) and push users to cyber cafés/agents.
- **How it works:** Widget scans form schema → Web Call SDK session with schema as context → conversational filling → `fill_field` tool → DOM updates live → read-back → submit. Analytics on drop-off fields.
- **User:** low-literacy / non-English users. **Buyer:** fintechs, insurers, gov portals, hospitals.
- **Seller/GTM:** developer PLG (npm + script tag), fintech growth teams, GovTech integrators.
- **Business model:** per voice session or per completed form.
- **Stack extras:** JS widget, WebSocket/SSE relay for field updates, validation (IFSC/PIN APIs).
- **Bolna features:** Web Call SDK, custom functions, multilingual, KB glossaries.
- **Demo:** Long PM-Kisan-style form fills in 40s from Tamil speech, then the same tag works on a second form.
- **Moat/expansion:** form-completion data → conversion optimisation → voice layer for any web app.
- **Risks:** ⚠️ SDK client-side tool support undocumented (use server relay). Less phone-native.
- **Scores:** V4 D4 F3 B4 Y4

### 19. 🔐 Asli: anti-deepfake payment verification
- **One-liner:** When finance gets an urgent "CEO" payment request, Asli calls the real person back on a registered number with challenge questions and holds the payment until verified.
- **Problem:** Voice clones of executives (e.g. attempted Sunil Mittal clone). A BBC reporter beat UK bank voice-ID with an AI clone. Account-recovery attacks on bank helplines.
- **How it works:** Request flagged (email/Slack/payment system) → Asli calls registered number → challenge questions from private knowledge + liveness prompts → verified/blocked → audit log; bank variant verifies callers before resets.
- **User:** finance teams / bank agents. **Buyer:** CFOs, banks, treasury/payroll ops.
- **Seller/GTM:** CISO/CFO sales, payment-platform integrations, cyber-insurance partners.
- **Business model:** per seat or per verification + enterprise fee.
- **Stack extras:** approval workflow integration (Slack/email webhook), challenge-question vault, audit log.
- **Bolna features:** outbound verification calls, graph agent (challenge flow), extractions (pass/fail), DTMF PIN.
- **Demo:** Cloned "CEO" voice asks "CFO" for urgent transfer → Asli calls real CEO → "I never asked" → payment blocked.
- **Why now:** YC RFS #11 "Proving you're human".
- **Moat/expansion:** trust graph of verified numbers → "verified human" layer for any call.
- **Risks:** security buyers want proven vendors. Detection claims must be careful.
- **Scores:** V4 D4 F4 B3 Y4

### 20. 🎓 RolePlay Guru: AI sales-training roleplays
- **One-liner:** Daily calls where AI plays a tough customer in Hindi/regional languages, then scores the rep on objection handling and IRDAI/SEBI compliance.
- **Problem:** 4.6M+ insurance agents (vendor estimate) plus lakhs of bank/pharma reps. Classroom training. Mis-selling penalties.
- **How it works:** Pick persona/scenario → AI calls the rep → realistic objections → post-call scorecard → manager leaderboard.
- **User:** sales agents. **Buyer:** insurers, banks, NBFCs, pharma.
- **Seller/GTM:** L&D heads, insurer agency channels.
- **Business model:** ₹200–500/agent/month.
- **Stack extras:** scenario library, scoring rubric (LLM judge), leaderboard.
- **Bolna features:** persona prompts, outbound scheduled calls, extractions/scoring, call summary.
- **Demo:** Agent practises a "burned by LIC before" customer → scorecard flags a non-compliant promise.
- **Moat/expansion:** scenario + performance data → TalkCRM / Saboot bundle.
- **Risks:** crowded roleplay category (Mindtickle, Sharpsell).
- **Scores:** V4 D3 F5 B4 Y3

### 21. 🚚 GaadiSaathi: voice load board for small truckers
- **One-liner:** Drivers call in "khaali hoon Nagpur, 20 ton" ("I'm empty in Nagpur, 20 tons") to get matched return loads. Fleet owners get daily voice trip check-ins without GPS hardware.
- **Problem:** 70%+ of fleet owners run <5 trucks. Loads come via phone brokers taking cuts. Drivers avoid English apps.
- **How it works:** Inbound driver availability → match shipper loads → AI calls shipper to negotiate → confirms both → daily driver check-ins (location, delay, POD via WhatsApp link).
- **User:** drivers/small fleet owners. **Buyer:** fleet owners (SaaS), shippers (commission).
- **Seller/GTM:** transport nagar hubs, driver associations, fuel-pump partnerships.
- **Business model:** commission per load (2–5%) + fleet SaaS.
- **Stack extras:** load DB + matching, WhatsApp POD upload.
- **Bolna features:** inbound + outbound, extractions (route, tonnage, rate), workflows (daily check-ins), multilingual.
- **Demo:** Driver calls, gets load offer, shipper negotiation happens live, both confirmations arrive.
- **Moat/expansion:** freight liquidity → payments → fuel/insurance/finance.
- **Risks:** two-sided marketplace cold start. Competitors (TrucksUp, Vahak).
- **Scores:** V4 D3 F4 B4 Y4

### 22. 🌾 KisanBid: farmer selling by phone
- **One-liner:** The farmer gives a missed call, the AI calls back to capture produce/quantity, checks mandi prices, collects bids from traders, and returns the best offer.
- **Problem:** Advisory is covered (Kisan e-Mitra: 93 lakh queries); selling isn't. Farmers depend on middlemen and lack price discovery.
- **How it works:** Missed call → callback → capture crop, grade, qty, location → web search mandi prices → outbound calls to 5–10 traders → best bid → confirm call to farmer → logistics hand-off.
- **User:** farmers. **Buyer:** traders/FPOs (commission), agri-marketplaces.
- **Seller/GTM:** FPOs, agri-input dealers, KVKs.
- **Business model:** commission per trade (1–2%).
- **Stack extras:** trader DB, Agmarknet price fetch.
- **Bolna features:** inbound/callback, web search, batch outbound, extractions, Sarvam rural STT.
- **Demo:** Farmer lists 20 quintal onions, 3 traders bid live, farmer accepts best offer.
- **Moat/expansion:** price/trade data → agri-credit, inputs marketplace.
- **Risks:** trust and logistics. Trader adoption.
- **Scores:** V4 D4 F4 B4 Y3

### 23. 💊 DawaiDhoondo: generic medicine finder
- **One-liner:** Read your prescription aloud. AI names generic equivalents and savings, then calls nearby chemists/Jan Aushadhi to confirm stock.
- **Problem:** Generics are 50–90% cheaper. Awareness is low and Jan Aushadhi stock is unreliable.
- **How it works:** Inbound call → drug names (keyword-biased STT) → generic mapping (KB) → parallel stock-check calls → SMS with location + price.
- **User:** patients. **Buyer:** pharmacies (lead fee), insurers/employers (cost savings), CSR.
- **Seller/GTM:** hospital OPDs, senior groups, pharmacy chains.
- **Business model:** lead fee per fulfilled prescription. B2B savings programmes.
- **Stack extras:** drug → generic DB, pharmacy directory.
- **Bolna features:** KB, batch outbound, extractions (in stock, price), keyword biasing.
- **Demo:** Read prescription, hear savings, two chemists called, SMS arrives with nearest stock.
- **Risks:** medical accuracy (no substitution advice beyond same molecule). Data quality.
- **Scores:** V4 D3 F4 B4 Y3

### 24. 🛒 Bolo Bazaar: the phone number that buys anything
- **One-liner:** Call one number, order groceries/recharges/tickets in your language, and pay via UPI 123PAY with no internet.
- **Problem:** ~400M feature-phone users are excluded from e-commerce and app UPI.
- **How it works:** Inbound order call → catalogue match (ONDC/local shops) → confirm + total → UPI 123PAY IVR payment → seller dashboard → delivery updates by call/SMS.
- **User:** feature-phone users. **Buyer:** sellers/ONDC buyer apps (commission), brands (placement).
- **Seller/GTM:** kirana partners, rural distribution, ONDC network participants.
- **Business model:** commission per order (3–8%) + brand placement.
- **Stack extras:** catalogue service (mock ONDC), seller app.
- **Bolna features:** inbound, KB/catalogue functions, multilingual, DTMF.
- **Demo:** A feature phone on stage orders atta + Surf Excel, and the seller dashboard receives it.
- **Why now:** YC RFS #6, UPI 123PAY live across banks.
- **Moat/expansion:** voice-commerce super-app for the next 500M.
- **Risks:** ⚠️ ONDC integration is heavy (mock it). Payments via 123PAY can't be fully integrated in 13 days.
- **Scores:** V4 D4 F2 B4 Y4

### 25. 🚑 108 Co-Pilot: emergency-line overflow + guidance
- **One-liner:** When ambulance lines are busy, AI answers in the caller's language, captures location and severity for dispatch, then calls back with first-aid (e.g. CPR) guidance.
- **Problem:** CAG: in Karnataka, 60%+ of cardiac/respiratory/stroke cases had late arrival. BLS ambulances sent to 75% of critical cases. Outages tripled dispatch time.
- **How it works:** Overflow inbound → structured intake (landmarks, symptoms, consciousness) → severity score → push to dispatcher console → callback with guided first aid until arrival.
- **User:** callers in emergencies. **Buyer:** state health departments, private ambulance networks (Red Health), hospitals.
- **Seller/GTM:** government tenders, private EMS partnerships.
- **Business model:** per-call / per-seat government contract.
- **Stack extras:** dispatcher console, geocoding from landmarks.
- **Bolna features:** inbound, graph agent intake, extractions, call transfer to human dispatcher, multilingual.
- **Demo:** Caller panics in Kannada → structured case appears on dispatcher map in 30s → CPR-guidance callback.
- **Risks:** ⚠️ safety-critical, so position as *dispatcher assist*, never a replacement. Long sales cycles.
- **Scores:** V5 D4 F3 B4 Y2

---

## 3. Rejected / parked
| Idea | Why parked |
|---|---|
| Clinic appointment bot | Very crowded (SquadStack, caller.digital, etc.) |
| Blue-collar voice hiring | Vahan dominates |
| Restaurant phone orders | Zomato piloting, many vendors |
| Doctor voice scribe | Crowded, in-clinic rather than phone-native |
| Mental-health first-line | Too risky for AI |
| Spoken-English coach | Crowded apps (RolePlay Guru is the B2B take) |
| Voice UPI for visually impaired | Payments compliance minefield |
| Farmer advisory hotline | Kisan e-Mitra covers it (KisanBid is the gap) |

## 4. Day-1 checklist (any idea)
- [ ] Apply via the form. Join [Bolna Builders Slack](https://join.slack.com/t/bolnabuilders/shared_invite/zt-4dg50suac-narQNDvQ9zKgC7aR2VdS3w) and ask about credits
- [ ] Bolna account: test inbound + outbound to an Indian number (number KYC/compliance; Plivo/Exotel may be faster)
- [ ] Prototype the riskiest piece first (Kavach: merged audio · HoldForMe: sending DTMF · Bolo Forms: SDK DOM sync · Hamming for Bharat: parallel call limits)
- [ ] Choose STT/TTS (Sarvam saaras v4 + Bulbul v4 Flash vs Deepgram + Cartesia)
- [ ] Script the 2-min pitch video + demo moment early

## 5. Sources
**Bolna:** [docs index](https://www.bolna.ai/docs/llms.txt) · [Oct 2026 changelog](https://www.bolna.ai/docs/changelog/october-2026.md) · [Sep 2026 changelog](https://www.bolna.ai/docs/changelog/september-2026.md) · [MCP tools](https://www.bolna.ai/docs/mcp-tool-list.md) · [Tools tab](https://www.bolna.ai/docs/agent-setup/tools-tab) · [Custom functions](https://www.bolna.ai/docs/tool-calling/custom-function-calls) · [Custom LLM](https://www.bolna.ai/docs/custom-llm-inference.md) · [SDKs](https://www.bolna.ai/docs/developer-resources/sdks/overview.md) · [TechCrunch](https://techcrunch.com/2026/01/20/bolna-nabs-6-3-million-from-general-catalyst-for-its-india-focused-voice-orchestration-platform/)
**Hackathons/VC:** [ElevenLabs winners](https://elevenlabs.io/blog/announcing-the-winners-of-the-elevenlabs-worldwide-hackathon) · [ElevenLabs tracks](https://elevenlabs.io/blog/online-conversational-agent-hackathon) · [Sarvam hackathon](https://digitalterminal.in/tech-companies/zo-house-bengaluru-hosts-sarvam-ai-hackathon) · [YC RFS](https://www.ycombinator.com/rfs) · [a16z voice 2026](https://podscripts.co/podcasts/a16z-podcast/big-ideas-2026-voice-agents-and-high-stakes-trust) · [Coval Series A](https://thenextweb.com/news/coval-28m-series-a-voice-ai-testing) · [Hamming vs Coval](https://hamming.ai/blog/hamming-vs-coval) · [YC W26](https://www.extruct.ai/data-room/ycombinator-companies-w26/) · [YC S26](https://www.extruct.ai/data-room/ycombinator-companies-s26/)
**Problems:** [Digital arrest ₹4k cr](https://www.newsbytesapp.com/news/science/india-s-digital-arrest-scam-causes-4-000cr-losses-in-3-years/story) · [Kirana orders](https://zopnote.com/12-how-to-digitize-a-kirana-grocery-store-in-india) · [Distributor reorders](https://richautomate.in/blog/whatsapp-b2b-reorder-automation-distributors-india-2026) · [MSME ₹8.1 lakh cr](https://www.fintechbiznews.com/fintech-technology/rs81-trn-is-locked-up-in-overdue-receivables) · [Recordent 73 days](https://mediabrief.com/recordent-report-highlights-working-capital-stress-for-indian-smes-as-average-overdue-receivables-cross-%E2%82%B93-83-crore/) · [NCH refunds](https://newsonair.gov.in/national-consumer-helpline-facilitates-refunds-of-more-than-105-cr-rupees-at-pre-litigation-stage/) · [Sierra IVR agents](https://www.zenml.io/llmops-database/ai-agents-navigating-ivr-systems-for-automated-outbound-calling) · [RBI mis-selling (Forrester)](https://www.forrester.com/blogs/the-consent-deficit-rbis-draft-rbc-directions-turn-misselling-into-a-proof-problem) · [Free-look](https://taxguru.in/?p=1090743) · [PIVC claim](https://jurigram.com/blog/consumer-law/life-insurance-mis-selling-complaint-free-look-period) · [Real-estate leads](https://www.sell.do/blog/real-estate-portal-leads-99acres-magicbricks-housing-2026) · [Elder care market](https://www.outlookmoney.com/retirement/spend/senior-living/indias-elderly-care-market-is-set-to-boom-in-tier-2-and-tier-3-cities-say-experts) · [LASI loneliness](https://submit.iafor.org/submission/submission103106/) · [UPI 123PAY](https://npci.org.in/what-we-do/upi-123pay/product-overview) · [Deepfake bank fraud](https://hyperverge.co/blog/deepfake-bank-fraud/) · [Health claims](https://www.dtnext.in/amp/story/news/business/understanding-challenges-in-health-insurance-claims-in-india-2) · [Women safety apps](https://techradar.com/news/best-women-safety-apps-in-india-for-android-and-ios) · [e-Samwad](https://www.brookings.edu/essay/case-study-e-samwad/) · [CAG 108 audit](https://cag.gov.in/uploads/icisa_it_reports/f081103b45fccc4748d202e6c6ea7fbe-06245a65d635d22-75261345.pdf) · [Kisan e-Mitra](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc2026214789901.pdf) · [Jan Aushadhi stock](https://www.tribuneindia.com/news/archive/ludhiana/jan-aushadhi-store-faces-medicine-crunch-566509) · [Truck owners](https://truckguru.co.in/blog/major-indian-transport-challenges-and-how-shippers-can-win/) · [Vahan (NITI)](https://frontiertech.niti.gov.in/story/how-ai-is-solving-indias-blue-collar-hiring-crisis-one-call-at-a-time/) · [BFSI field sales](https://www.squadstack.ai/blog/the-future-of-field-sales-in-bfsi)
