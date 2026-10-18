# Bolna Buildathon: Idea Research & Top 5 Pitches

> Researched 2026-10-18 · Submission deadline **Oct 31** (13 days) · See [hackathon-details.md](hackathon-details.md)

---

## 1. What the research says

### 1.1 What wins voice AI hackathons
Patterns from recent winners (ElevenLabs Worldwide, ElevenLabs Online, Sarvam BuildIn' Hours, Agora, YC Conversational AI):

| Pattern | Winning examples |
|---|---|
| **Agent picks up the phone and does a chore for you** (calls businesses, negotiates, chases) | *Dealwise* (SF #1, calls local businesses for quotes), *Procuro* (NYC #2, calls suppliers to track delayed parts), *Claimsio* (Warsaw, compliant debt collection) |
| **Safety / guardian agents** | *Roadmate* (drowsy-driver copilot that texts a friend), *Voice Guardian* (Seoul #1, home protection), *DeepSky* (Warsaw #1, airspace safety) |
| **Voice-first for underserved users / Indic** | Sarvam hackathon top 3: tender discovery for small businesses, Indic storytelling for kids, *Setu* for non-speaking people. Egypt: Arabic-first voice tutor |
| **Voice layer on existing software** | *Unstuck* (NYC #1, docs-style support agent for any website), ElevenLabs partner tracks (Notion, n8n, Lovable, Exa integrations) |
| **Real-world, physical-world help** | *Pep* (PT coach), *Hugo Tour Guide*, YC Spring '26 RFS: "multimodal real-time guidance for physical work" |

**Takeaway:** the winners aren't novelty chatbots. They're agents that act (make calls, write structured data, alert people), carry clear stakes, and finish a live demo with a moment the audience feels.

### 1.2 What Bolna cares about (signals for judging)
- Bolna's business is **Indian, multilingual, telephony-first** voice: 200K+ calls/day, 1,050+ customers across e-commerce, BFSI, logistics, recruitment and education. Customers include Spinny, Snabbit and Varun Beverages (FMCG). About 60–70% of volume is English/Hindi, and regional languages are growing.
- They've built India-specific features: Hinglish code-mixing, numbers read in English, **DTMF keypad input for long entries**, noise handling, and Truecaller verification.
- YC rejected them 5× because "Indian enterprises won't pay for voice AI." They will probably favour builds that show **someone will pay**.
- Sponsors: Plivo, Exotel (telephony), Sarvam, Deepgram, Cartesia, Kalpa Labs (speech). Using their stack is a soft plus.

### 1.3 Bolna platform features available to build on (as of Oct 2026)
| Capability | Use it for |
|---|---|
| **Inbound + outbound phone agents**, batch calls, scheduled **Workflows/Campaigns** | Daily or weekly calling loops |
| **Graph agents** (node-based flows, extraction on edges, static nodes that end calls) | Deterministic, structured conversations |
| **Custom function calls** (any REST API mid-call), Cal.com booking, **call transfer** | Taking actions: write order, look up data, escalate to a human |
| **Web Search tool** (new, Oct 8: OpenAI/Exa/Firecrawl/Parallel) | Live prices, news, verification |
| **Knowledge base** (URL / PDF RAG) | Catalogs, scheme rules, scam playbooks |
| **Extractions / Dispositions + call summary + webhooks** | Turning calls into structured JSON for dashboards |
| **Web Call SDK** (browser voice) | Adding a voice layer to a web app |
| **Multilingual** with smart language switching, start-in-language via `agent_language` | Vernacular users |
| **Custom LLM** (OpenAI-compatible endpoint) and **Custom TTS** | Full control over agent logic |
| **DTMF**, P-Asserted-Identity / Diversion headers, **SIP trunks** (Plivo/Exotel/etc.) | Telephony tricks |
| **MCP server / Claude connector** | Fast agent setup from Claude |
| STT: Sarvam saaras v4 (keyword biasing), Deepgram, AssemblyAI U3 · TTS: Sarvam Bulbul v4 Flash (code-mixed voices), Cartesia, ElevenLabs v4 Turbo, Kalpa | Indic voice quality |

### 1.4 India problem spaces with real pain
- **"Digital arrest" scams:** about ₹4,058 cr lost from 2022 to May 2026 across ~2.98 lakh complaints. Victims are mostly elderly. The Supreme Court has called it a "very big challenge."
- **Kirana / general trade:** orders arrive scattered across phone, SMS and WhatsApp voice notes and some get missed. FMCG reorders depend on weekly salesman beat visits, so outlets that run out early wait for the next visit. App-based retailer ordering has struggled to scale.
- **Healthcare:** no-shows cost clinics ₹500–2,000 per slot. The space is crowded with vendors.
- **Elderly living alone:** 41% of elders living alone report loneliness (LASI). Many seniors take 4–8 meds a day, and mistakes go unnoticed.
- **Blue-collar hiring:** ~300M workers prefer speaking to typing. Vahan already does voice hiring at scale, so this space is crowded.
- **Government services:** Bhashini/VoicERA exist, but citizen-facing helplines remain weak in dialects.
- **Gap noted by trackers:** Indian voice AI is concentrated in customer-service bots and developer APIs. **Vertical, consumer-facing and field-ops products are underserved.**

---

## 2. Top 5 ideas

### Idea 1 — 🛡️ **Kavach: an AI that joins the call when your parent is being scammed**

**One-liner:** If a "CBI officer" calls Mom, she taps *Add Call → Kavach* and merges it. Kavach listens, recognises the digital-arrest script, tells her in Hindi or Tamil that it's a scam, and alerts the family on WhatsApp.

**Problem:** About ₹4,000+ crore has been lost to "digital arrest" and impersonation scams, mostly by elderly people. Scammers keep victims on the line for hours or days ("don't hang up, don't tell anyone"). Awareness campaigns don't help in the moment, because the victim is isolated *while it is happening*.

**How it works (seamless, no app needed):**
1. **Onboarding (2 min):** A family member registers the parent's number and their own WhatsApp on a simple web page. The parent saves "Kavach" as a contact.
2. **Mid-call SOS:** During any suspicious call, the parent uses the phone's built-in **"Add call" → Kavach → Merge**. This works on every phone, including feature phones, with no app.
3. **Kavach listens** to the merged audio: scammer plus parent. A custom-LLM layer stays quiet and scores the conversation against a scam playbook (KB of known scripts: CBI/ED/TRAI/customs parcel/"your Aadhaar is linked to money laundering").
4. **Kavach speaks up** in the parent's language once risk crosses a threshold: *"Amma, this is Kavach. Police never arrest anyone on a video call. This is a scam. Please hang up now."* It can also address the scammer directly ("This call is being recorded and reported to 1930").
5. **Family alert:** a WhatsApp/SMS with the call summary, risk score and the scammer's claims, plus an optional **warm transfer to the child's phone** or the national cyber helpline **1930**.
6. **Fallback mode:** if the parent already hung up, they call Kavach and describe what happened. Kavach uses **web search** to verify claims (e.g. "is there an FIR system called…") and walks them through next steps (block the payment, call the bank, call 1930).

**Why voice is essential:** The threat is a phone call and the victim is on a phone. Voice is the only interface that can intervene in real time. Text or app solutions arrive after the money is gone.

**Bolna implementation:**
- Inbound Bolna number (Plivo/Exotel) → agent in Hindi/English plus regional languages; Sarvam saaras v4 STT with **keyword biasing** (CBI, ED, TRAI, FedEx, Aadhaar, "digital arrest", "money laundering").
- **Custom LLM endpoint** (our FastAPI proxy) decides *when* to speak. It sends minimal filler or a pre-tool hold while listening, and an alert once the risk score is high. Prompt-only "stay silent" fallback if needed.
- Knowledge base of scam scripts (from I4C/RBI advisories and news cases).
- Custom function `alert_family(risk, summary)` → WhatsApp (Twilio/Gupshup sandbox) or SMS.
- Call transfer tool → family member or 1930.
- Extractions: scam type, impersonated agency, amount demanded, scammer number → **family dashboard** (Next.js).

**Demo for judges (90 sec):** Teammate A plays a "CBI officer" and calls Teammate B (playing a nervous parent). B merges Kavach. The audience hears Kavach detect the script and speak in Hindi, and a WhatsApp alert pops up live on the projected phone. This is a dramatic, emotional moment with a crore-scale problem behind it.

**Business model:** ₹99–199/month family subscription (sold to the children). B2B2C via banks, insurers and telcos (Jio/Airtel are under pressure to fight spam). Pension funds and senior-living communities.

**Risks / day-1 checks:**
- ⚠️ Verify Bolna handles **merged/conference audio** well (two speakers on one channel, VAD constantly triggered). Validate on Day 1. If the agent can't stay quiet reliably, use the custom-LLM gate or switch to "call Kavach after" mode.
- Recording consent and legality: frame it as user-initiated (the parent adds Kavach).

**Scores:** Value ⭐⭐⭐⭐⭐ · Wow demo ⭐⭐⭐⭐⭐ · Feasibility in 13 days ⭐⭐⭐ · Bolna fit ⭐⭐⭐⭐ · YC angle ⭐⭐⭐⭐

---

### Idea 2 — 🛒 **BeatBot: an AI sales rep that calls every kirana for its reorder**

**One-liner:** FMCG distributors replace or augment their salesman's weekly beat visit with a **personalised voice call in the shopkeeper's language**. It knows what they ordered last time, suggests the reorder, pitches this week's scheme, and pushes the order into the distributor's system and a WhatsApp invoice.

**Problem:** India has 12M+ kiranas, served by distributors whose salesmen (DSRs) walk fixed beats. Reorders are captured in diaries or apps, or via WhatsApp voice notes the distributor has to parse by hand. An outlet that runs out mid-week waits for the next visit, and that's a lost sale. App-based retailer ordering hasn't scaled: shopkeepers won't log into apps, but they **always pick up the phone**. A rep visit is the most expensive way to capture a routine reorder.

**How it works:**
1. Distributor uploads its retailer list and SKU catalog (CSV / Google Sheet) and order history.
2. **Scheduled outbound campaign** (Bolna Workflows): every retailer gets a call at their preferred time (e.g. 11am, after morning rush).
3. Agent: *"Namaste Sharma ji, Ravi from Gupta Distributors. Last week you took 5 cases of Maaza and 2 of Thums Up. Same again? There's also a buy-10-get-1 on Sting this week."* It handles Hinglish, brand names (keyword-biased STT), quantities and units (cases/peti/dozen), and substitutions.
4. **Live order building:** custom function calls check stock and price in the distributor's backend. The agent reads back the order and total and confirms with DTMF ("press 1 to confirm").
5. **Instantly:** an order appears on the distributor dashboard, and the retailer gets a WhatsApp order summary and UPI payment link.
6. **Inbound too:** a retailer can call the same number any time to place an ad-hoc order. That replaces messy voice notes.
7. **Insights:** extractions capture complaints, competitor mentions, out-of-stocks and credit requests. The sales manager sees a heatmap.

**Why voice is essential:** Kirana owners are behind a counter with their hands full, often low-text-literacy, and phone-native. Voice is already how general trade works ("bhaiya order likh lo"). BeatBot just puts an AI on the other end of the line.

**Bolna implementation:**
- **Graph agent**: greet → recall last order → upsell scheme → collect line items (loop) → confirm → end. Extraction on edges for `sku`, `qty`, `unit`.
- **Workflows + campaigns** for scheduled daily/weekly beats, with webhooks on completion. **Batch CSV** with `agent_language` per retailer so each call opens in Marathi, Tamil, etc.
- Custom functions: `get_last_order`, `check_stock`, `create_order` → Supabase/Postgres. Knowledge base = catalog plus active schemes.
- Sarvam saaras v4 keyword biasing for SKU names; Bulbul v4 Flash Hinglish voice.
- Dashboard (Next.js): orders, call outcomes, retailer heatmap, revenue recovered.

**Demo:** Upload a CSV of 5 retailers (teammates' phones) → click "Run beat" → 3 phones ring at once → one person orders in Hindi, another in Kannada → orders stream onto the dashboard and WhatsApp invoices arrive live.

**Business model:** SaaS per distributor (₹3–10K/month) or per-order fee. Sell to FMCG brands (HUL, ITC, Dabur, Varun Beverages, which is already a Bolna customer) to cover their whole distributor network. Clear ROI: one DSR costs ₹15–25K/month and covers ~40 outlets a day.

**Risks:** Catalog matching for messy speech (fix with a fuzzy-match function plus read-back confirmation). Distributor data integration (use a Google Sheet as the "DMS" for the MVP).

**Scores:** Value ⭐⭐⭐⭐⭐ · Wow demo ⭐⭐⭐⭐ · Feasibility ⭐⭐⭐⭐⭐ · Bolna fit ⭐⭐⭐⭐⭐ · YC angle ⭐⭐⭐⭐⭐ (clear "who pays")

---

### Idea 3 — 🤝 **MolBhav: an agent that calls 10 local vendors, gets quotes and negotiates for you**

**One-liner:** Tell it "I need packers and movers from Koramangala to Whitefield, 2BHK, Saturday" (or a caterer for 50 people, an AC repair, a tempo). MolBhav **phones vendors in parallel in their language**, collects quotes, **haggles**, and hands you a ranked comparison with a one-tap "book this one".

**Problem:** India's local-services economy runs on phone calls. Vendors on JustDial and Google Maps rarely have online pricing. Getting three quotes means 10 calls, repeating your requirements, and haggling in Hindi or Kannada. It takes hours and urban users hate it. Prices vary 2–3× for the same job.

**How it works:**
1. User describes the need in a voice note or text (web app, WhatsApp, or by calling MolBhav).
2. MolBhav pulls vendor numbers (Google Places API / curated list) and **creates a batch of outbound calls**, each opening in the vendor's likely language.
3. On each call the agent describes the job precisely, answers vendor questions (floor, lift, items), asks for the price, and **negotiates** with policy: anchor with the lowest quote so far, ask for discounts, confirm inclusions (packing material, GST, labour).
4. Extractions → structured quote: price, inclusions, availability, vendor tone and confidence.
5. User gets a **live-updating comparison card** (and WhatsApp summary). Tapping "Book" makes MolBhav call the vendor back to confirm, or warm-transfer the user.

**Why voice is essential:** The supply side (small vendors) only speaks phone. That's the moat: no API exists, and voice *is* the API.

**Bolna implementation:**
- Outbound **batch calls** with dynamic per-call variables (`job_spec`, `best_quote_so_far`), so later calls negotiate against earlier quotes.
- Custom function `get_best_quote()` mid-call. Web Search tool for market-rate sanity checks.
- Extractions/dispositions: `price`, `includes_gst`, `available_date`, `agreed` → webhook → app.
- Call transfer for "connect me to the vendor". Multilingual agent with `agent_language`.

**Demo:** On stage, type "movers, 2BHK, Saturday". Three teammates' phones ring as "vendors", each with different prices and personalities (one in Hindi, one in Kannada). The audience watches the AI anchor ("Another vendor quoted ₹8,500, can you do better?") and the vendor drop the price live. The comparison table fills in real time. This is the proven Dealwise/Procuro winning format, localised to India.

**Business model:** Free for consumers, with a lead/booking commission from vendors (like Urban Company / JustDial). Premium "concierge" tier. B2B: procurement for SMBs (raw materials, transport, printing).

**Risks:** Calling real vendors without consent at scale (TRAI telemarketing rules). For the demo, use team phones. For production, frame as transactional calls on behalf of a customer with clear AI disclosure. Negotiation quality depends on prompting.

**Scores:** Value ⭐⭐⭐⭐ · Wow demo ⭐⭐⭐⭐⭐ · Feasibility ⭐⭐⭐⭐ · Bolna fit ⭐⭐⭐⭐ · YC angle ⭐⭐⭐⭐

---

### Idea 4 — 📋 **FieldLog: daily reporting for field teams by phone call, no apps or forms**

**One-liner:** At 6pm every site supervisor, ASHA worker or delivery lead gets a **2-minute call** in their language: "How many workers came today? Any material shortage? Any safety incident?" Their spoken answers become a **structured daily report**, a dashboard for the owner, and instant escalations.

**Problem:** India's field workforce (construction, ASHA/anganwadi health workers, logistics, agri-procurement, security agencies) still reports via paper registers, WhatsApp chaos or apps they don't use. Owners get no reliable daily visibility. ASHA workers spend hours on manual registers. Supervisors are on-site with dirty hands and low text literacy, so forms fail and voice works.

**How it works:**
1. Owner picks a template (Construction / ASHA / Delivery fleet / Security) or builds a custom checklist of questions → we generate a **graph agent**.
2. **Scheduled daily outbound call** to each worker (or they call in). The agent asks the checklist conversationally, follows up on vague answers ("Kitne bags cement bacha hai?"), and uses DTMF for numbers if needed.
3. **Extractions** turn answers into typed fields (labour count, materials, % progress, incidents, photos requested via a WhatsApp link).
4. **Rules fire instantly:** incident reported → call/WhatsApp the owner. Low cement → auto-message the supplier. ASHA: high-risk pregnancy flagged → PHC alert.
5. Owner dashboard: daily summaries across all sites, trends, a missing-report list, and a weekly AI digest by voice note.

**Why voice is essential:** It turns the worker's phone (any phone, no data plan needed) into a data-entry terminal. A phone call is the most inclusive interface in India.

**Bolna implementation:**
- **Graph agents** generated from a checklist JSON via Bolna API/MCP (`create_graph_agent`), with extraction params with `allowed_values` on edges for clean data.
- **Workflows + campaigns** for daily schedules. Workflow execution **webhooks** → our backend.
- Custom functions for escalations. Call summary → owner WhatsApp digest.
- Multilingual (`agent_language` per worker). Sarvam STT for Indic.

**Demo:** Owner creates a "Construction site" template in 30 seconds → three supervisor phones ring → one reports a safety incident in Hindi → the owner's phone gets an escalation call and WhatsApp within seconds → the dashboard updates live.

**Business model:** Per-worker SaaS (₹100–300/worker/month) for construction firms, logistics companies, security agencies, NGOs and CSR programmes. Government pilots (NHM for ASHA).

**Risks:** Less "wow" than Ideas 1 and 3, and it needs a crisp vertical story. Pick **one vertical** (construction or ASHA) for the pitch.

**Scores:** Value ⭐⭐⭐⭐⭐ · Wow demo ⭐⭐⭐ · Feasibility ⭐⭐⭐⭐⭐ · Bolna fit ⭐⭐⭐⭐⭐ · YC angle ⭐⭐⭐⭐ (YC RFS: real-time guidance for physical work)

---

### Idea 5 — 🧩 **Bolo Forms: one script tag that makes any web form fillable by voice in 10 Indian languages**

**One-liner:** A drop-in widget for any website (gov portals, insurance claims, loan applications, KYC, hospital registration). The user taps 🎙️ and talks in Tamil or Bhojpuri, and the AI **fills the form live on screen**, asks for missing fields, explains confusing ones, and validates before submit.

**Problem:** Hundreds of millions of Indians are now online but struggle with long English forms. That drives drop-offs in loan and insurance funnels and dependence on agents or cyber cafés (who charge fees and sometimes commit fraud) for scheme applications. Every form-heavy business loses conversions to this.

**How it works:**
1. Developer adds `<script src="boloforms.js" data-key="…">`. The widget auto-scans the page's form fields (labels, types, required, options).
2. User clicks the mic → a **Bolna Web Call SDK** session starts with the form schema injected as context.
3. Conversational filling: *"Aapka naam? … Aadhaar number bata dijiye"*. Numbers are read back in English, a Bolna strength. The agent explains jargon ("nominee", "IFSC") in simple terms.
4. Each answer triggers a tool call → the widget writes the value into the DOM field live (the user *sees* it fill), with validation (PIN code, IFSC lookup, date formats).
5. Review step: the agent reads back a summary. The user corrects by voice and submits.

**Why voice is essential:** It removes literacy and English as barriers without rebuilding the product. This maps directly to the hackathon's example "a voice layer on an app you already built".

**Bolna implementation:**
- **Web Call SDK** in the browser. Agent context = serialised form schema plus page context.
- Custom function `fill_field(field_id, value)` → our backend → pushed to the widget via WebSocket/SSE (or SDK events if client-side tools are supported).
- Multilingual with auto-switching. Knowledge base for domain glossaries (insurance, banking, schemes).
- Analytics dashboard: completion rate with vs. without voice, drop-off fields.

**Demo:** Open a clone of a long PM-Kisan or insurance-claim form. A teammate speaks Tamil and the fields fill in live on the projector. The judges see a 3-minute ordeal become 40 seconds. Then show the same script tag working on a second, totally different form, which shows it's infrastructure, not a one-off.

**Business model:** Usage-based dev tool (per voice-session). Sell to fintech/insurtech funnels (conversion lift = direct revenue), CSC/government portals and hospitals.

**Risks:** The Web Call SDK's client-side tool support is undocumented. You may need a server relay for DOM updates (doable). It's less "phone-native", which Bolna loves, though it shows off their new SDK.

**Scores:** Value ⭐⭐⭐⭐ · Wow demo ⭐⭐⭐⭐ · Feasibility ⭐⭐⭐ · Bolna fit ⭐⭐⭐⭐ · YC angle ⭐⭐⭐⭐ (dev infra, horizontal)

---

## 3. Side-by-side

| | Kavach (scam shield) | BeatBot (kirana reorder) | MolBhav (quote negotiator) | FieldLog (field reporting) | Bolo Forms (voice forms) |
|---|---|---|---|---|---|
| Who pays | Families, banks, telcos | FMCG distributors/brands | Vendors (commission) | Construction/logistics/NGOs | Fintech, insurers, gov portals |
| Stage "wow" moment | AI interrupts a live scam call | Phones ring, orders stream in | AI haggles price down live | Incident → instant escalation | Form fills itself as you talk |
| Build risk | Merged-audio handling | Low | Low-medium | Low | SDK DOM sync |
| Bolna features used | Inbound, custom LLM, KB, transfer, web search | Graph, workflows, batch, functions, KB, DTMF | Batch, dynamic vars, extraction, transfer | Graph via API, workflows, webhooks | Web Call SDK, functions |
| Overall | 🔥 Highest emotional impact | 🔥 Strongest business case | 🔥 Most proven format | Solid, practical | Solid, infra play |

## 4. My recommendation

1. **BeatBot** if you want the safest path to the YC interview: a clear buyer, direct relevance to Bolna's own customers (Varun Beverages), and a showcase of most of Bolna's platform (graph agents, workflows, batch, multilingual, functions, DTMF). It answers the exact objection YC had about Bolna: Indian businesses will pay.
2. **Kavach** if you want to win the room. It's the most memorable live demo, about a crore-scale national problem. Spend Day 1 validating merged-audio behaviour on Bolna. If that works, it's a top-3 contender.
3. **MolBhav** as a crowd-pleaser with a proven winning format.

**Hybrid option:** Kavach's "family safety for parents" can expand into a **daily parent check-in companion** (meds reminder, mood, loneliness, plus scam shield) using the same infra. That gives a bigger subscription story for the pitch.

**Honourable mentions** (researched, rejected as primary): clinic appointment bot (very crowded), blue-collar voice hiring (Vahan dominates), kids' voice tutor (crowded, hard to show value in a demo), farmer advisory hotline (good, but Kisan Call Centre and Digital Green exist; possible angle: web-search mandi prices plus scheme eligibility).

## 5. Day-1 checklist (whichever idea we pick)
- [ ] Register on the apply form; join the [Bolna Builders Slack](https://join.slack.com/t/bolnabuilders/shared_invite/zt-4dg50suac-narQNDvQ9zKgC7aR2VdS3w) and ask about hackathon credits
- [ ] Bolna account → test an inbound and outbound call to an Indian number (check number KYC/compliance needs; Plivo/Exotel sponsor numbers may be quicker)
- [ ] Prototype the riskiest piece first (Kavach: merged audio · Bolo Forms: SDK DOM sync · BeatBot/MolBhav: SKU/quote extraction accuracy)
- [ ] Pick STT/TTS: Sarvam saaras v4 + Bulbul v4 Flash (Hinglish) vs Deepgram + Cartesia
- [ ] Plan the 2-min pitch video early, since the demo moment drives the submission

---

## Sources
- Bolna docs: [llms.txt index](https://www.bolna.ai/docs/llms.txt), [Oct 2026 changelog](https://www.bolna.ai/docs/changelog/october-2026.md), [Sep 2026 changelog](https://www.bolna.ai/docs/changelog/september-2026.md), [MCP tool list](https://www.bolna.ai/docs/mcp-tool-list.md), [Tools tab](https://www.bolna.ai/docs/agent-setup/tools-tab), [Custom function calls](https://www.bolna.ai/docs/tool-calling/custom-function-calls), [Custom LLM](https://www.bolna.ai/docs/custom-llm-inference.md), [SDKs](https://www.bolna.ai/docs/developer-resources/sdks/overview.md)
- [TechCrunch: Bolna raises $6.3M](https://techcrunch.com/2026/01/20/bolna-nabs-6-3-million-from-general-catalyst-for-its-india-focused-voice-orchestration-platform/) · [Entrepreneur India on Bolna](https://india.entrepreneur.com/news-and-trends/voice-ai-startup-bolna-raises-usd-63-mn-funding-led-by/502062)
- [ElevenLabs Worldwide Hackathon winners](https://elevenlabs.io/blog/announcing-the-winners-of-the-elevenlabs-worldwide-hackathon) · [ElevenLabs online hackathon tracks](https://elevenlabs.io/blog/online-conversational-agent-hackathon) · [Sarvam hackathon at Zo House](https://digitalterminal.in/tech-companies/zo-house-bengaluru-hosts-sarvam-ai-hackathon) · [Agora Voice AI Hackathon Manila](https://tutorialsdojo.com/voice-ai-hackathon-manila-2026/) · [lablab.ai winners](https://lablab.ai/apps/recent-winners)
- [Digital arrest losses ₹4,000 cr](https://www.newsbytesapp.com/news/science/india-s-digital-arrest-scam-causes-4-000cr-losses-in-3-years/story) · [Pune seniors lose ₹100 cr](https://www.punekarnews.in/?p=245348) · [SC on digital arrests](https://superkalam.com/current-affairs/04-11-2025/digital-arrests-are-a-very-big-challenge-victims-mostly-elderly-lost-3-000-cr-in-india-alone-sc-pg14-e9a40d2b-a355-49c7-ae2f-a819ae7fb574)
- [Kirana digitisation & scattered orders](https://zopnote.com/12-how-to-digitize-a-kirana-grocery-store-in-india) · [WhatsApp B2B reorder for distributors](https://richautomate.in/blog/whatsapp-b2b-reorder-automation-distributors-india-2026) · [Capillary on FMCG digital distribution](https://www.capillarytech.com/blog/indian-fmcg-brands-digital-distribution/) · [Kirana Club on selling without sales teams](https://kirana.club/resources/sell-fmcg-kirana-without-sales-team)
- [NITI Frontier Tech: Vahan voice hiring](https://frontiertech.niti.gov.in/story/how-ai-is-solving-indias-blue-collar-hiring-crisis-one-call-at-a-time/) · [AIM: vernacular voice hiring](https://analyticsindiamag.com/ai-startups/hello-ai-speaking-hiring-goes-vernacular-with-voice-ai)
- [LASI loneliness study](https://submit.iafor.org/submission/submission103106/) · [Samarth: elders living alone](https://care.samarth.community/blog/safety/elderly-living-alone-india-safety/)
- [PIB: AI transforming rural India](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc2026223798701.pdf) · [MediaNama: Bhashini VoicERA](https://www.medianama.com/2026/02/223-bhashini-voice-ai-stack-voicera-ai-impact-summit-policy-recommendations/)
- [Healthcare no-show vendor claims](https://www.squadstack.ai/blog/cut-no-shows-ai-voice-agents-for-hospital-appointments) · [Tracxn: India voice AI startups](https://tracxn.com/d/explore/voice-ai-startups-in-india/__s7thq7EI12tPI5Mmcnok_iuzpK5VWI3-4ZhUxzXfMmA) · [Entrepreneur: voice AI as India's backbone](https://www.entrepreneur.com/en-in/news-and-trends/is-voice-ai-becoming-indias-next-digital-backbone/495110)
