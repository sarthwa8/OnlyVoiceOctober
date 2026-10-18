# FieldLog (working name: *Munshi*): the AI site record-keeper that works by phone call

> v0.1 · 2026-10-18 · Team of **2** · Status: **candidate, compared with CareCall in §12**
> Earlier concept: [research/ideas-bank.md #13](research/ideas-bank.md) · Shared build stack: [BUILD_PLAN.md](BUILD_PLAN.md)
> Items marked **[verify]** need checking against Bolna docs or real users. ₹ figures marked *(est.)* are assumptions to confirm in customer interviews.

---

## 0. TL;DR

Every construction site in India has a **munshi**, the record-keeper who writes labour attendance and material in a register. The site supervisor then phones or WhatsApps the owner every evening with a scattered update. Owners running 3–10 sites never get a clean picture until something goes wrong: cement runs out and 25 labourers sit idle, a slab slips a week, a labour contractor inflates headcount, or an accident goes unreported.

**FieldLog calls the site supervisor twice a day in Hindi/Punjabi:**
- a **60-second attendance call** in the morning
- a **2-minute progress call** in the evening

It turns what the supervisor says into:
- a **client-ready Daily Progress Report (DPR)**
- a **multi-site owner dashboard**
- a **labour attendance sheet per contractor**
- **instant escalations**: material shortages, safety incidents, delays

There's also an inbound line: *"Sariya khatam ho gaya"* ("we're out of steel bars") becomes a material request, the owner approves it on WhatsApp, and (stretch goal) the AI calls the supplier to place the order.

**Why voice:** supervisors and munshis are on-site, hands busy, often semi-literate in English, and speak Hindi, Punjabi or Bhojpuri. Construction apps exist, but **adoption is the problem**: nobody on site types. A phone call needs no app, no training and works on a keypad phone.

---

## 1. Choosing the vertical

The original idea listed construction, ASHA workers, delivery and security. One vertical is a must for both the pitch and the pilot.

| Vertical | Real users from Chandigarh in 13 days | Clear payer and ROI | Overlap with Bolna customers | Demo | Verdict |
|---|---|---|---|---|---|
| **Construction (contractors / builders)** | ✅ Tricity building boom (Mohali, Kharar, Zirakpur, New Chandigarh). Everyone knows a builder or thekedar (labour contractor). We can **visit sites in person**. | ✅ idle labour, delays, leakage | ✅ none | 🟡→✅ with the voice→DPR and supplier-call moments | **Pick** |
| ASHA / health workers | ❌ needs NHM/state approval, health-data rules | 🟡 government, slow | ✅ none | ✅ emotional | Pitch as an expansion vertical only |
| Delivery / logistics leads | ✅ | ✅ | ❌ Bolna customers already automate this | 🟡 | Reject |
| Security agencies (guard check-ins) | 🟡 | ✅ | ✅ | 🟡 | Possible 2nd vertical |
| Solar / telecom field crews | 🟡 needs a contact | ✅ | ✅ | 🟡 | Expansion |

**Sub-segment to target first:** small and mid contractors and builders with **2–10 active sites**. They're big enough to feel the pain of not seeing every site, and small enough that the owner decides on the spot. Large developers already have ERP teams.

**Secondary wedge (worth testing in discovery):** families building their own house in Punjab, often with a child abroad, who want daily updates from their contractor. Same product, consumer buyer.

---

## 2. The workflow today (what we're replacing)

### Who's who on a site
| Role | What they do | FieldLog's relationship |
|---|---|---|
| **Owner / contractor / builder** | Runs several sites, pays everyone, answers to the client | **Buyer.** Gets dashboard, DPR, alerts |
| **Site engineer / supervisor** | Runs the site day to day | **Primary caller.** Answers the 2 daily calls |
| **Munshi** | Keeps the attendance and material register | Alternate caller. FieldLog becomes their voice register. |
| **Thekedar** (labour contractor) | Supplies masons (*mistri*) and helpers (*beldar*), paid per labour-day | Gets a weekly attendance sheet, which cuts payment disputes |
| **Client / architect / PMC** | Wants DPRs, progress and photos | Gets the auto-generated DPR |
| **Supplier** (cement, steel, sand, ready-mix concrete) | Delivers on phone orders | Stretch goal: FieldLog calls them for orders |

### A day on site, as it is now
1. **Morning:** labour arrives and the munshi writes names and counts in the register, per thekedar and trade.
2. **Day:** trucks arrive with a delivery slip. Material is used. Nobody records stock in real time.
3. **Evening:** the supervisor phones the owner or sends a WhatsApp voice note or text: *"Aaj 22 labour, shuttering aadhi, cement 40 bag bacha"* ("22 labour today, shuttering half done, 40 bags of cement left"). The owner gets this from 5 sites, in 5 formats, while driving.
4. **Weekly:** labour gets paid (often cash, Saturdays) from the register. Disputes come up over headcount.
5. **Monthly:** progress bills are raised from progress measurements. Clients chase DPRs that are often typed up late, from memory.

### The pains, and what they cost *(est., validate in interviews)*
| Pain | Cost |
|---|---|
| Material stock-out found too late → idle labour | 25 labourers × ~₹600–900/day ≈ **₹15–20k per idle day**, plus schedule slip |
| Headcount inflation / attendance disputes | A few % of the wage bill. Trust problems with thekedars. |
| Delays found late (no daily plan vs actual) | Penalty clauses, angry clients, cash-flow hits |
| Owner's time chasing updates | 1–2 hours/day of calls across sites |
| DPRs late or missing | Client friction, slower progress-bill approval |
| Safety incidents under-reported | Legal and insurance exposure, no record |

---

## 3. The FieldLog workflow

### 3.1 Calls
| Call | When | Length | Captures |
|---|---|---|---|
| **Morning attendance** (outbound) | ~9:30–10:00, per site | 45–90 s | Headcount per thekedar × trade; today's planned activities; early blockers ("anything short today?") |
| **Evening progress** (outbound) | ~18:00–19:00 | 2–3 min | Work done per activity vs plan; material received / used / remaining; issues (rain, machine down, missing drawing, client change); safety incidents; tomorrow's plan and needs |
| **Ad-hoc line** (inbound, 24×7) | Anytime | 30–60 s | Material request, incident report, visitor/inspection, breakdown |
| **Reminder / escalation** (outbound) | If a report is missed | 30 s | "Shaam ki report baaki hai" ("evening report is pending"). After 2 misses → tell the owner. |
| *Stretch:* **Supplier order call** (outbound) | After owner approves a request | 1–2 min | Order quantity, rate confirmation, delivery date → purchase order |

### 3.2 What each call produces
- **DPR PDF** (English, the client's format, with logo), sent to the owner at ~20:00, plus the client if enabled.
- **WhatsApp summary** to the owner: one card per site (🟢/🟡/🔴), headcount, progress, top issue.
- **Dashboard:** all sites at a glance, per-site timeline, a "plan vs actual" activity list, material ledger, issues board, recordings and transcripts as proof.
- **Weekly attendance sheet** per thekedar (CSV/PDF) → payment-ready.
- **Audit trail:** every number links to the recording and the moment it was said, which settles "who said what".

### 3.3 Escalation rules (v1)
| Trigger | Action |
|---|---|
| Safety incident ("gir gaya", "chot lagi" — someone fell, someone's hurt) | **Immediate voice call to owner** + WhatsApp, and transfer the supervisor to the owner if they want |
| Material below threshold or "khatam" (run out) | Material request → owner gets WhatsApp with Approve/Reject buttons |
| Headcount down >30% vs 7-day average | WARN to owner |
| Activity behind plan 2 days running | WARN + shown in DPR |
| No evening report by 20:00 | Reminder call → owner notified after 2 misses |
| Client visit / inspection mentioned | Note in DPR + owner FYI |

### 3.4 Sample evening call (Hindi, demo-ready)
> **FieldLog:** Namaste Gurpreet ji, FieldLog se — Sector 82 site ki shaam ki report. Aaj kul kitne log aaye the?
> *(Namaste Gurpreet ji, this is FieldLog — evening report for the Sector 82 site. How many people came today in total?)*
> **Supervisor:** Baais. Chhe mistri, solah beldar.
> *(Twenty-two. Six masons, sixteen helpers.)*
> **FieldLog:** Theek — 6 mistri, 16 beldar, kul 22. Teesri manzil ki slab shuttering kitni hui?
> *(OK — 6 masons, 16 helpers, 22 in all. How much of the third-floor slab shuttering got done?)*
> **Supervisor:** Aadhi ho gayi, kal poori. Par sariya kam pad raha hai.
> *(Half done, it'll be complete tomorrow. But we're running short of steel bars.)*
> **FieldLog:** Kitna sariya chahiye, aur kab tak?
> *(How much steel do you need, and by when?)*
> **Supervisor:** Do ton, parson tak.
> *(Two tons, by the day after tomorrow.)*
> **FieldLog:** Samjha — 2 ton sariya, parson tak. Sharma sir ko approval bhej raha hoon. Cement kitne bag bache?
> *(Got it — 2 tons of steel by the day after tomorrow. I'm sending it to Sharma sir for approval. How many bags of cement are left?)*
> **Supervisor:** Chaalis.
> *(Forty.)*
> **FieldLog:** Koi chot ya hadsa aaj?
> *(Any injury or accident today?)*
> **Supervisor:** Nahi.
> *(No.)*
> **FieldLog:** Kal ka plan?
> *(What's the plan for tomorrow?)*
> **Supervisor:** Shuttering khatam, phir sariya bandhai shuru.
> *(Finish the shuttering, then start tying the steel.)*
> **FieldLog:** Dohra deta hoon: 22 log, slab shuttering 50%, sariya 2 ton parson tak chahiye, cement 40 bag, koi hadsa nahi, kal shuttering aur bandhai. Sahi hai?
> *(Let me read it back: 22 people, slab shuttering 50%, 2 tons of steel needed by the day after tomorrow, 40 bags of cement, no accidents, tomorrow shuttering and steel-tying. Is that right?)*
> **Supervisor:** Haan.
> *(Yes.)*
>
> → 70 seconds later: the DPR PDF lands on the owner's WhatsApp, the steel request waits for approval, and the dashboard tile for Sector 82 turns 🟡.

---

## 4. Why this, why now, and what it's up against

- **Why voice:** the people on site won't type, and the register and phone call are already the system. FieldLog doesn't change their habit. It just puts an AI on the other end of the call they already make.
- **Why now:** Indian-language speech recognition (Sarvam) now copes with Hinglish and Punjabi plus numbers on phone audio. Bolna gives us scheduled calls, structured extraction and mid-call function calls out of the box. The Tricity construction boom means demand on our doorstep.
- **Competition:**
  - **Construction-management apps** (e.g. Powerplay, Onsite) [verify current features, and whether they've added voice]. They're our biggest "why not a feature?" question. Answer: they sell to the office, and the field won't type. Voice is a different wedge, and we could even *integrate into* them later ("a voice layer on software you already have").
  - **WhatsApp + Excel:** the real incumbent. We beat it on structure, rollups and alerts.
  - **Hiring a second munshi or coordinator:** ~₹12–18k/month *(est.)*. We're a fraction of that.
- **YC fit:** a vertical AI agent replacing a manual physical-world workflow (YC's "OS for the physical world" request). Clear B2B payer.
- **Moat over time:** daily structured site data across many sites gives:
  - productivity benchmarks (labour-days per sq ft per activity)
  - delay prediction
  - material reconciliation (what was used vs what should have been → theft/wastage flags)
  - later: contractor credit and insurance underwriting

---

## 5. Business model *(est., validate)*
- **Price:** ₹1,500–3,000 per active site per month, or ₹10–15k/month for a contractor with up to 10 sites.
- **ROI pitch:** *"Avoid one idle-labour day per site per quarter and FieldLog has paid for itself."*
- **Cost to serve:** ~4 min of calls per site per day ≈ ~120 min/month. Price this from Bolna's measured per-minute cost (Day-0 spike). Comfortable margin at the prices above.
- **Go-to-market:** founder-led in Tricity → builder associations / CREDAI chapters → construction-material dealers as channel partners (they talk to every contractor) → white-label for construction apps.
- **Expansion:** the same engine (checklist → call → structured report → rules) serves solar installation firms, interior fit-out, facility management, security agencies, and later ASHA/NGO programmes.

---

## 6. Demo (2-minute video / stage)
1. **0:00–0:15 Hook:** a photo of a handwritten site register and a messy WhatsApp group. "An owner with 6 sites. Every evening, 6 phone calls and 40 WhatsApp messages."
2. **0:15–0:55 The call:** a real supervisor on a real Mohali site (subtitled) gives the 70-second Hindi/Punjabi report from §3.4.
3. **0:55–1:15 The output:** cut to the owner's phone. An English DPR PDF arrives, the dashboard tile turns 🟡, and a steel request waits with an **Approve** button.
4. **1:15–1:35 The agent acts** (stretch): owner taps Approve → FieldLog **calls the steel supplier** in Hindi, confirms 2 tons for Thursday, and a purchase order appears. *If not built:* a safety-incident call → owner's phone rings in 5 seconds.
5. **1:35–1:50 Proof:** pilot numbers. Sites and supervisors live, reports completed, **accuracy vs the paper register**, minutes saved per day, and a quote from the owner.
6. **1:50–2:00 Ask:** "₹2,000 per site per month. No app. Any phone. Built on Bolna."

---

## 7. Build: what's different from the CareCall build plan

**About 70% of the engine is the same:** scheduled outbound calls with per-call context, post-call extraction, rules, alerts and dashboard. FastAPI + Supabase + Next.js as in [BUILD_PLAN.md §2](BUILD_PLAN.md). What changes:

### 7.1 Agents
| Agent | Type | Key config |
|---|---|---|
| `fieldlog-morning` | **Graph agent**: greet → headcount per thekedar (loop) → planned activities → blockers → read-back | Extraction on edges, using the site's `allowed_values` (thekedar names, trades, activity list) [verify graph extraction + allowed_values]. DTMF fallback for counts ("keypad pe number daba dijiye" — "please type the number on the keypad"). |
| `fieldlog-evening` | Graph agent: headcount check → each planned activity's progress → materials → issues → safety → tomorrow → read-back | Function calls mid-call: `get_site_context`, `create_material_request`, `flag_incident` (→ immediate owner call) |
| `fieldlog-inbound` | Single prompt + functions | Caller ID → supervisor → site lookup. Intents: material request / incident / other. |
| `fieldlog-supplier` *(stretch)* | Single prompt | Order details from `user_data`. Extract confirmed qty, rate, delivery date. Transfer to the owner if the rate differs. |

**Per-call `user_data`:** site name, supervisor name, thekedars and trades, today's planned activities (from yesterday's "kal ka plan" — tomorrow's plan), material items with last-known stock, open issues. This is what makes the call feel like it *knows the site*.

**Keyword biasing per site:** thekedar names; trade words (mistri/mason, beldar/helper, carpenter, steel fixer); materials (cement, sariya/steel bars, ret/sand, bajri/gravel, eent/bricks, RMC/ready-mix, tiles, POP); activities (shuttering/formwork, slab, chinai/brickwork, plaster, bandhai/steel-tying, curing, excavation, PCC); numbers and units (bag, ton, trolley, cubic foot, running foot).

### 7.2 Data model (delta)
```sql
orgs            (id, name, plan)
sites           (id, org_id, name, address, client_name, dpr_template, morning_time, evening_time, active)
people          (id, org_id, name, phone, role check (role in ('owner','supervisor','munshi','thekedar','client','supplier')), language, whatsapp)
site_people     (site_id, person_id, role)
activities      (id, site_id, name, unit, planned_qty, planned_start, planned_end, status)
reports         (id, site_id, date, kind ('morning','evening'), call_id, completed bool, readback_confirmed bool)
labour_entries  (report_id, thekedar_id, trade, count)
progress_entries(report_id, activity_id, qty_done, pct_done, note)
materials       (id, site_id, name, unit, reorder_threshold)
material_txns   (id, material_id, report_id, kind ('received','consumed','stock_count'), qty, challan_photo_url)
issues          (id, site_id, report_id, type ('safety','material','machine','drawing','weather','client','other'), severity, status, note)
material_requests(id, site_id, material_id, qty, needed_by, status ('pending','approved','rejected','ordered'), approved_by, supplier_call_id)
calls, alerts, audit_log   -- same as CareCall plan
```

### 7.3 New components
- **DPR generator:** HTML template → PDF (WeasyPrint), one template per client, sent through WhatsApp and email.
- **Site setup wizard:** owner (or we, during the pilot) enters site, people, thekedars, activities and materials in ~10 minutes. Can also be bootstrapped by a *voice setup call* with the supervisor (nice to have).
- **Reconciliation view:** labour-days per thekedar per week, material ledger with received vs consumed.
- **Photo nudge** (nice to have): after the evening call, a WhatsApp message "Aaj ki 2 photo bhejiye" ("please send 2 photos from today") → photos attached to the DPR.

### 7.4 Technical risks specific to FieldLog
| Risk | Mitigation |
|---|---|
| **Numbers misheard** (22 vs 32, "dedh sau" = 150, "saade teen" = 3.5) | Keyword biasing, mandatory read-back + confirmation, DTMF fallback for headcount, Hindi-number normaliser in the backend, eval set of spoken numbers |
| **Site noise** (mixer, generator, cutters) | Evening call after work stops; ask the supervisor to step aside; test Sarvam vs Deepgram on real site audio on Day 1 |
| **Free speech → right activity** | Activity list as `allowed_values`; LLM maps "teesri manzil ka lenter" ("third-floor slab") to "3F slab"; unknowns go to an "unmapped" list the owner can fix in one tap |
| **Supervisor fatigue** (two calls a day) | Keep morning under 60 s, skip unchanged items ("same as yesterday?"), measure completion rate daily |
| **Owner doesn't trust AI numbers** | Every number links to the recording timestamp. Run a parallel accuracy audit against the paper register during the pilot. |

---

## 8. Getting real users (the make-or-break for FieldLog)

**Target by Oct 31:** **1–2 contractors, 4–8 sites, 6–12 supervisors**, with ≥ 10 days of real reports. **Anchor contractor committed by Mon Oct 20.**

### Where to find them (Tricity)
1. Family and friends' network: "who do you know building something right now?" Every family in Punjab knows a contractor.
2. Civil-engineering friends and juniors on site internships; PEC / Chandigarh University civil faculty with consultancies.
3. Walk into active sites in Mohali Sectors 66–90, Kharar, Zirakpur and New Chandigarh. Ask for the site engineer and offer a **free 3-week pilot**.
4. Building-material dealers (cement/steel shops): they know every active contractor and can introduce us.
5. Secondary: families building a house who want daily updates.

### The pilot offer
"Free until Nov 30. Your munshi keeps the register as usual, so there's zero risk. You get a DPR every evening and alerts. If it's useful, it's ₹X/site after that." Ask for a **written LOI / price agreement** at day 7.

### Discovery script (Oct 18–19, two site visits + two owner calls)
- How do you hear about each site's day now? How long does it take you?
- Show me the register. Show me yesterday's WhatsApp updates. *(Photograph them.)*
- When did material last run out? What did it cost you?
- Do your clients ask for DPRs? *Can I see one?* (This becomes our template.)
- Which app have you tried? Why did the site team stop using it?
- Would your supervisor pick up a 2-minute call at 6 pm? What language?
- What would you pay to never chase a site update again?

---

## 9. What we measure (proof for the submission)
| Metric | Target |
|---|---|
| Report completion rate (calls answered + completed / scheduled) | ≥ 85% |
| **Field accuracy vs paper register** (headcount, material counts) | ≥ 95% on headcount |
| Median report call length | Morning ≤ 60 s, evening ≤ 150 s |
| Owner time saved | Self-reported + count of "update" calls before vs after |
| Issues caught early | e.g. material shortages flagged ≥ 1 day before stock-out |
| Paying intent | ≥ 1 signed LOI or paid pilot |
| Voice latency | p50 ≤ 1.5 s to first audio |

---

## 10. Two-person plan

### Roles (both people do everything, each owns one track)
- **Person A: Voice + backend.** Bolna agents (graph flows, prompts, keyword lists), scheduler, webhooks, extraction, number normaliser, rules, alerts, eval sets.
- **Person B: Product + users.** Customer discovery and site visits, onboarding and site setup, dashboard, DPR template and generator, daily transcript QA, accuracy audit, pitch and video.
- **Both, daily (30 min at 21:00):** listen to 5 real calls, log issues in `docs/pilot-log.md`, and pick tomorrow's top 3 fixes.

### Scope cuts for a team of two
Supplier-order call is a **stretch** (Phase 4 only if on track). Photo nudge, voice-based site setup and the reconciliation view are nice-to-haves. One DPR template. Hindi + Punjabi only.

### Day by day
| Dates | Person A (voice + backend) | Person B (product + users) | Exit check |
|---|---|---|---|
| **Sat Oct 18 – Sun Oct 19** | Bolna account + Indian number; spikes: Hindi/Punjabi numbers accuracy, noisy-audio STT (Sarvam vs Deepgram), graph agent extraction, `user_data`, webhook payloads, DTMF; cost per minute | **2 site visits + 2 owner calls** (discovery script), photograph registers/DPRs/WhatsApp updates, line up anchor contractor; repo + Supabase + Vercel scaffold | **Gate Mon Oct 20 10:00:** anchor contractor yes/no (see §12) |
| **Mon Oct 20 – Tue Oct 21** | `fieldlog-evening` graph agent v1, scheduler, webhook → `reports`/entries, number normaliser | Site setup form, seed the anchor's 2–3 sites, WhatsApp evening summary | **First real evening reports from 2–3 supervisors on Oct 21** |
| **Wed Oct 22 – Thu Oct 23** | `fieldlog-morning` agent, rules + alerts (incident → owner call), reminder calls | DPR PDF generator (anchor's format), dashboard v1 (all sites + per-site timeline) | Owner receives a real DPR from a real call |
| **Fri Oct 24 – Sun Oct 26** | `fieldlog-inbound` (material request / incident), WhatsApp Approve/Reject, prompt v2 from transcripts, number eval set | Expand to **6–12 supervisors** (2nd contractor), start the **register accuracy audit**, weekly thekedar attendance sheet | Accuracy ≥ 95% on headcount; ≥ 85% completion |
| **Mon Oct 27 – Tue Oct 28** | Hardening (retries, idempotency, IST time handling, Sentry); *stretch:* `fieldlog-supplier` call | Metrics page, owner interview (time saved, quote), **LOI / price ask** | Metrics exported; LOI or a clear "no" |
| **Wed Oct 29 – Thu Oct 30** | Demo-day reliability; backup recordings | 2-min video (real site footage) + written submission | **Submitted Oct 30** (Oct 31 is buffer) |
| **Nov 1 – Nov 20** | Supplier call (if not done), activity-plan import from Excel, delay prediction v0 | Keep the pilot running, add contractors, interview prep, stage rehearsal | Retention + more sites for the finale |

---

## 11. FieldLog pros and cons (summary)

**Pros**
- **Strongest business case of everything we've looked at:** B2B payer, ROI in rupees, decision-maker reachable in person in Chandigarh.
- **Lower technical risk than CareCall + Kavach.** No merged-call unknowns, no custom silence gate. The hard parts (numbers, jargon, noise) are testable on Day 1.
- **Smaller scope, which fits a team of 2:** one engine, three agents.
- No overlap with Bolna's customer base (sales, support, collections, recruiting).
- Uses Bolna well: graph agents with extraction, scheduled outbound with `user_data`, inbound, mid-call functions, DTMF, transfer, multilingual, webhooks.
- Natural "agent that acts" upgrade (supplier ordering), plus a clear data moat.

**Cons**
- **Real users depend on finding an anchor contractor within ~48 hours.** This is the single biggest risk.
- **Less emotional demo** than a live scam being stopped. It needs the voice→DPR and supplier-call moments to land.
- **"Why isn't this a feature of Powerplay/Onsite?"** We need a crisp answer (adoption wedge, voice-native, could partner).
- Supervisors may tire of two calls a day. Completion rate must be watched from Day 1.
- Construction is fragmented and price-sensitive. Sales cycles beyond the pilot may be slow.

---

## 12. FieldLog vs CareCall + Kavach (team of 2)

| | **FieldLog** | **CareCall + Kavach** |
|---|---|---|
| Real users by Oct 31 | 🟡 needs an anchor contractor by Oct 20 | ✅ our own parents, today |
| Who pays | ✅ contractor, ROI in ₹ | 🟡 adult children, consumer willingness to pay unproven |
| Demo emotion | 🟡 (✅ with supplier call) | ✅ live scam stopped |
| Technical risk | ✅ low–medium (numbers, noise) | 🟡 merged-call behaviour unknown |
| Scope for 2 people | ✅ one engine, 3 agents | 🟡 effectively two products (check-in + Kavach gate + eval set) |
| Bolna feature depth | ✅ graph agents, DTMF, functions, inbound + outbound | ✅ custom LLM, KB, transfer, outbound |
| YC story | ✅ vertical AI for physical-world work | ✅ AI for the aging population |
| "Why not a feature?" risk | 🟡 construction apps | ✅ low |

### Recommendation for a team of two
**Make it a gated decision on Mon Oct 20, 10:00, and spend this weekend so that both options stay open:**
1. **Person B** spends Sat–Sun on construction discovery (2 site visits + 2 owner calls) and tries to get an **anchor contractor** committed.
2. **Person A** runs the Bolna spikes. These are mostly shared (Indian number, outbound with `user_data`, webhooks, extraction, Hindi/Punjabi accuracy, cost). Add the merged-call test (~1 hour) to keep CareCall alive.

**Then:**
- **Anchor contractor committed → build FieldLog.** Stronger business, lower risk, right-sized for two.
- **No anchor → build CareCall**, cutting Kavach down to the "announce + warn" level if the merged-call test is shaky.

Either way, nothing built this weekend is wasted, because the core engine is the same.

---

## 13. Decisions needed from you
1. Approve the **gated plan** above (or pick one outright now).
2. Who is Person A (voice + backend) and who is Person B (product + users)?
3. Do either of you already know a contractor, builder, site engineer or building-material dealer? Names to call **today**.
4. Name: **FieldLog** (generic, works across verticals) or **Munshi** (memorable, construction-native)?
