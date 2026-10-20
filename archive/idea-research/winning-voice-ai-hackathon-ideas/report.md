# Win Bolna with calls people want

Voice-AI hackathons in 2024–2026 were won by projects that made something real happen in front of the judges, most often a live phone call. They were not won by agents that just chat. Out of about 73 winners we catalogued, only about 9 had an agent calling a real third party. But those few took the biggest prizes: the ElevenLabs global top prize, SF 1st place, NYC 2nd place (where judges were "blown away"), and the "most mind-blowing" award at a health hackathon. Judges at several events said they rewarded working code over mockups, real business value, and products where voice is truly needed. For the Bolna Buildathon the signals point the same way, but with an Indian, production-minded tilt. Bolna's own team picks the shortlist. Bolna earns about 80% of its revenue from e-commerce, banking and finance, and education, and its founders often say "Indian enterprises will pay". The final judge, Grey Baker, is a YC General Partner who co-founded Dependabot, a developer tool. Today's voice agents are reliable only for short, scripted calls. The best 2026 agents still fail about one task in three on realistic customer-service work, and Hindi speech recognition gets roughly 12–22% of words wrong on phone audio. So the winning shape is a **short call that the other person expects or wants, which ends in structured data that a business pays for**. We propose ten new ideas of that shape. Our top three are **KaamHua** (proof-of-service calls that decide whether a technician gets paid), **ShiftPakka** (night-before shift confirmation with automatic backup calls) and **NakliGrahak** (an Indic test harness that phones your voice agent with simulated Hinglish callers). The first two can get real users in the 13 days left. The third can sign up other buildathon teams as users before October 31.

| Term | Plain meaning |
|---|---|
| B2B | A product sold to businesses, not to individual consumers |
| Outbound / inbound call | Outbound: the agent places the call. Inbound: a person calls the agent |
| Pickup rate | The share of calls that a person answers |
| Structured output | Clean fields (yes/no, a date, a number, a choice from a list) saved to a sheet or database, not just a transcript |
| Extraction | Pulling those fields out of the conversation, usually with an LLM after or during the call |
| Webhook | An automatic message one system sends to another when something happens (for example, "call ended, here is the data") |
| DTMF | Keypad presses during a call ("press 1 to confirm") |
| ASR / STT, TTS | Speech-to-text (the agent hearing) and text-to-speech (the agent speaking) |
| WER | Word error rate: the share of words that speech-to-text gets wrong |
| P95 latency | The delay that 95% of turns stay under; the slow tail that callers notice |
| pass^k | Whether an agent succeeds on *every one* of k repeated runs of the same test, a measure of consistency |
| HITL | Human in the loop: a person takes over when the agent cannot finish |
| TRAI, DPDP | India's telecom regulator; India's data-protection law (Digital Personal Data Protection Act) |

## Winners make a real call happen in front of the judges

The clearest pattern from 2024–2026 is simple. **Voice plus a visible real-world action beats voice plus chat.** At the ElevenLabs x a16z Worldwide Hackathon (Feb 2025, 300+ projects), the global winner was GibberLink. In its demo, two agents on a hotel-booking call notice that both are AI and switch to a faster sound-based protocol. The judges were unanimous and cited the "intriguing demo" ([ElevenLabs](https://elevenlabs.io/blog/announcing-the-winners-of-the-elevenlabs-worldwide-hackathon)). The video went viral ([Wikipedia](https://en.wikipedia.org/wiki/Gibberlink)). At the same event, Procuro took NYC 2nd by phoning US suppliers live to find delayed parts, and judges were "blown away". Dealwise took SF 1st by phoning local businesses for quotes ([ElevenLabs](https://elevenlabs.io/blog/announcing-the-winners-of-the-elevenlabs-worldwide-hackathon)). At a 2025 healthcare hackathon, Clinicians Unchained won the "most mind-blowing" award. Its agent phones pharmacies and insurers to learn why a prescription was denied, and it was built on Retell ([Out of Pocket](https://www.outofpocket.health/p/oops-2025-healthcare-ai-hackathon-projects)). Google's Gemini Live Agent Challenge had 1,536 entries. It gave an honourable mention to Call My Parts, which calls suppliers for price and stock and ranks the answers ([Google Cloud](https://cloud.google.com/blog/topics/developers-practitioners/winners-and-highlights-of-the-gemini-live-agent-challenge)).

**Judges reward demos they can touch.** At AI Week Milan in 2026, the winner of the voice stream let judges type in their own phone numbers and take live calls. He says that is "what won them over" ([Resonance](https://resonancevoiceai.substack.com/p/going-it-alone-i-built-a-hackathon)). In the AssemblyAI/LiveKit SF hackathon, judges gave Best Overall to Voxy with one line: "The platform just works" ([AssemblyAI](https://www.assemblyai.com/blog/voice-agent-hackathon-sept-19)). Published rubrics repeat the same few axes: application of technology, presentation, business value and originality ([lablab.ai](https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon)). One Deepgram prize adds "how essential voice is to the experience" ([Devpost](https://ai-hackathon-2026.devpost.com/)). That last test matters most. If a text box would do the job just as well, the project is weak. A phone call to someone who does not use apps, or who has busy hands, passes easily.

**B2B winners were always narrow and vertical**, meaning built for one industry. Examples are supply-chain parts (Procuro), debt collection (Claimsio), airspace safety (DeepSky), prescription denials (Clinicians Unchained) and robotic surgery (ORION, the $25k Gemini grand prize) ([ElevenLabs](https://elevenlabs.io/blog/announcing-the-winners-of-the-elevenlabs-worldwide-hackathon); [Google Cloud](https://cloud.google.com/blog/topics/developers-practitioners/winners-and-highlights-of-the-gemini-live-agent-challenge)). Developer tools for voice teams also win. Vapi's own hackathon reportedly gave 1st place to a training and testing tool for voice-AI teams ([Vapi on X](https://x.com/Vapi_AI/status/1796598283688870209), from a search snippet). A YC voice hackathon kit tells teams to run simulated conversations and score transcripts before they demo ([Pipecat GitHub](https://github.com/pipecat-ai/yc-voice-agents-hackathon)). YC-linked events now offer YC interviews as prizes. Their briefs ask for agents that "actually touch the real world", with "no more sandbox demos" ([David Lieb on X](https://x.com/dflieb/status/2052146123079639398)).

**Some ideas are now overdone.** Galleries from 2026 events show many near-copies: language tutors, AI therapists and companions, pitch and interview coaches, travel planners, standup bots, podcast-ad insertion, and "AI calls local businesses for quotes or bookings" ([OpenAI Voice Hack Night gallery](https://cerebralvalley.ai/e/openai-voice-hack-night/hackathon/gallery); [Cartesia gallery](https://cerebralvalley.ai/e/cartesia-voice-agents-hackathon/hackathon/gallery)). Calling businesses for quotes won SF 1st in Feb 2025. By 2026 it showed up again in entries that did not place. The lesson is that the call-a-third-party demo still works, but only when it is aimed at a specific B2B buyer, not a consumer errand. One honest caveat: we found **no hackathon winner with a documented funding round that clearly came from the win**. Wins work mainly as credibility and distribution.

## Bolna's shortlist will favour production calls, paying buyers and Indian languages

The Bolna Buildathon has **no tracks and no published rubric**. Submissions close October 31. Bolna's team reviews them and interviews shortlisted teams on November 5–7. The top three pitch at the Symphony finale in Bengaluru on November 20. First prize is ₹50k plus a YC interview with Grey Baker ([Bolna Buildathon](https://www.bolna.ai/symphony/buildathon)). The submission form allows only **200 characters** of description, plus a demo link and a deck or video. The one-line pitch has to land on its own. Grey Baker became a YC General Partner in June 2026. He co-founded Dependabot (sold to GitHub), was an early product and engineering lead at GoCardless, and co-founded Pincites, a legal-tech company ([YC blog](https://www.ycombinator.com/blog/chris-golda-and-grey-baker-general-partners)). His background is developer tools, payments and B2B workflow software.

The first gate is Bolna's own team, so Bolna's worldview matters most. YC rejected Bolna five times with the objection that "Indian enterprises are not going to pay" ([TechCrunch](https://techcrunch.com/2026/01/20/bolna-nabs-6-3-million-from-general-catalyst-for-its-india-focused-voice-orchestration-platform/)). **A project that shows an Indian business will pay answers the exact doubt Bolna had to overcome.** About 80% of Bolna's revenue comes from e-commerce, BFSI (banking, financial services and insurance) and education. Its founders describe a shift from "call-centre replacement" to "outcome-driven automation" ([Inc42](https://inc42.com/startups/how-bolna-ai-is-helping-enterprises-to-win-the-voice-ai-race/)). Its case studies lead with a rupee or volume outcome, such as "₹2.5 Cr+ revenue recovered" for Hypothesis ([Bolna](https://www.bolna.ai/customer-story/hypothesis)) and technical screening calls for the staffing firm Awign ([Bolna](https://www.bolna.ai/customer-story/awign)). CEO Maitreya Wagh names **vernacular quality, noise handling and address recognition** as the gaps that keep deals from going live ([Inc42](https://inc42.com/startups/how-bolna-ai-is-helping-enterprises-to-win-the-voice-ai-race/)). A build that visibly handles Hindi or a regional language over a noisy line speaks to Bolna's own roadmap.

Bolna's September–October 2026 changelog shows what it wants builders to use. The main items are graph agents with **extraction limited to allowed values**, extracted data sent in webhooks, **workflow execution webhooks**, a web-search tool, **SIP trunks** with your own carrier (Plivo, Twilio, Telnyx) including DTMF and call transfer, Sarvam keyword biasing for up to 50 terms, Sarvam Bulbul v4 Flash voices, bring-your-own TTS, a Claude connector and an MCP server ([Oct 2026 changelog](https://www.bolna.ai/docs/changelog/october-2026.md)), and starting a call in a chosen language ([Sep 2026 changelog](https://www.bolna.ai/docs/changelog/september-2026.md)). Symphony's top sponsors include Truecaller for Business, Exotel, Plivo and Sarvam ([Symphony](https://www.bolna.ai/symphony)). Indian voice hackathons with enterprise sponsors judge on engineering rigour. IIT Kharagpur's CallKaro "Golden Hour" scores tool calling, data schema, guardrails, edge-case testing and latency. Every agent there must pass at least five simulated-customer scenarios ([StartupGrantsIndia](https://www.startupgrantsindia.com/competitions/the-golden-hour-a-voice-ai-hackathon)). Expect Bolna's interviews to probe the same things. Put together, the target is a **B2B workflow that runs on a real Indian phone number with real users, uses several of these new features, and reports a measurable outcome**.

## Reliability limits shrink the safe zone to short, expected calls

The brief's limit, "narrow scripted calls only", has strong support in the research. On Sierra's tau-Voice benchmark of policy-bound customer-service tasks, the best voice agent finishes **67% of tasks on the first try** (April 2026). That is up from 30% in August 2025, but still below the roughly 85% that text agents reach ([Sierra](https://sierra.ai/blog/tau-voice-benchmarking-real-time-voice-agents-on-real-world-tasks)). In the original paper, realistic noise and accents cut scores further, to 26–38% ([arXiv 2603.13686](https://arxiv.org/abs/2603.13686)). Long conversations make things worse. LLMs lose **39% of their performance** on average when a task is spread over many turns, because they guess early and do not recover ([arXiv 2505.06120](https://arxiv.org/abs/2505.06120)). Consistency is also weak. On EVA-Bench, systems that *can* pass a scenario often fail it on a repeat run ([arXiv 2605.13841](https://arxiv.org/abs/2605.13841)). Older phone-system data points the same way: each extra detail the caller must give (a tracking number, an address, a date) lowers completion ([Cekura](https://www.cekura.ai/blogs/containment-rate)).

The Indian phone line adds its own problems. Hindi speech recognition from Sarvam Saaras v3 gets about 12% of words wrong on clean audio and about 22% in heavy noise ([arXiv 2606.21408](https://arxiv.org/pdf/2606.21408)). That error rate is fine for "haan / nahi" (yes / no) and choices from a short list. It is **not reliable for names, addresses or ID numbers**. Across about 10,000 production agents, typical turn delay is 1.5–1.7 seconds, and the slowest 5% of turns take 3–5 seconds ([Hamming](https://hamming.ai/blog/7-voice-agent-asr-failure-modes-in-production)). Pickup is the other big wall. Truecaller users ignored **81% of calls from India's 140x promotional series and 79% from the 1600x service series** ([TechCrunch](https://techcrunch.com/2026/07/08/truecaller-clashes-with-indias-telecom-regulator-over-anti-spam-rules/)). Warm, expected calls do much better. Vendors report 40–70% connection when the call follows a user action within a minute, against about 8–15% for cold lists ([Brilo AI](https://www.brilo.ai/resources/best-voice-ai-for-outbound-sales-calls)). Treat these as vendor figures, not controlled studies.

The rules point the same way. Since February 2025, Indian telemarketing from ordinary 10-digit numbers has been barred, and repeat offenders can lose all telecom lines for a year ([TRAI](https://cms.trai.gov.in/sites/default/files/2025-02/PR_No.11of2025.pdf)). A new 1601 series covers service calls from utilities and logistics firms ([MediaNama](https://www.medianama.com/2026/08/223-trai-1601-series-logistics-courier-services/)). A September 2026 rule reportedly treats all software-placed calls, including AI calls, as A2P (application-to-person) traffic that must be declared to the operator in advance ([Nokiamob](https://nokiamob.net/2026/09/19/indias-telecom-regulator-targets-ai-robocalls-and-caller-id-apps/), a secondary source). In the US, AI voices fall under the TCPA (the US law on automated calls), which requires prior consent ([Hunton](https://huntonak.com/privacy-and-information-security-law/fcc-issues-declaratory-ruling-that-tcpa-applies-to-ai-generated-voice-calls)). For the pilot this means: call only people who agreed to be called, say "this is an AI assistant calling for X" at the start, offer "say stop" or "press 9" to opt out, and never cold-call a bought list.

Every idea below follows one design that keeps it inside the safe zone. The call is **triggered by a business event the other person knows about** and announced by WhatsApp or SMS first. The agent **speaks** the hard details (invoice numbers, claim IDs, values), because text-to-speech is reliable. It only **listens** for yes/no answers, numbers and short-list choices. It reads back what it heard and asks for a keypad confirm. Extraction is limited to allowed values. Voicemail or no answer is treated as a normal outcome that triggers a WhatsApp follow-up. A "needs human" queue catches the rest.

## Ten new ideas that fit the safe zone

None of these repeats the team's 17 earlier ideas. Where an idea sits close to one of them, we say so. The ideas appear in ranked order. All "funded analog" claims come from the sources cited. Where we write "none found", that means our searches of YC lists, funding maps and Indian funding data turned up nothing. It does not prove that no company exists.

### 1. KaamHua: proof-of-service calls that decide technician payouts

**One-liner.** When a technician marks a job done, an AI calls the customer within minutes to confirm the work really happened. The technician's payout is released only on a "yes". (*Kaam hua?* means "Was the work done?")

**Who is on the call, and why they pick up.** The customer who just had an AC, water purifier, solar panel or broadband connection installed or repaired. The call comes minutes after the technician leaves, in the brand's name, announced by a WhatsApp message ("You'll get a 1-minute call from X to confirm your service"). Customers want the job closed properly and the warranty registered.

**The narrow script.** AI disclosure and brand name. "Did the technician visit today and finish the AC installation?" (yes / no / partly). "Is it working now?" (yes / no). "Did you pay any extra cash to the technician?" (yes / no, then an amount). "Rate the technician from 1 to 5." Read back, then "press 1 to confirm". Serial numbers are not collected by voice. They come as a WhatsApp photo, or not at all.

**Structured output and B2B buyer.** One row per job: visited, completed, working, extra cash and amount, rating, issue code from a fixed list, and a needs-human flag. It feeds the service CRM and a payout sheet. "Yes" auto-approves the payout. "No" reopens the job and holds the payout. Buyers are brand service heads, franchise service partners, solar installers, internet providers and home-services platforms. Snabbit, a house-help platform, is already a Bolna customer ([TechCrunch](https://techcrunch.com/2026/01/20/bolna-nabs-6-3-million-from-general-catalyst-for-its-india-focused-voice-orchestration-platform/)).

**Funded analog and Indian competition.** Acrely (YC S25) handles the *start* of a home-service job: greeting, booking and dispatch ([YC](https://www.ycombinator.com/companies/acrely)). We found no funded company that owns *proof* at the end of the job. In India, horizontal platforms already run survey calls (GoKwik runs surveys on Bolna, per [Bolna](https://www.bolna.ai/customer-story/gokwik)). A plain satisfaction call is therefore a commodity. Ringg's co-founder calls simple high-volume calling "a price game" ([TechCrunch](https://techcrunch.com/2026/08/25/indias-ringg-gets-backing-from-peak-xv-as-it-pushes-voice-ai-past-the-phone-call/)). The moat has to be the **payout rule and the link to the job system**, not the call itself.

**Real users by Oct 31.** Pick one local service business with 5–20 jobs a day: an AC repair shop, a water-purifier service franchise, a solar installer, a broadband franchise, or a housing society's facility manager. Technicians already send "done" on WhatsApp. Give them a one-tap form or copy jobs into a Google Sheet. Run 7–10 days in "shadow mode": calls happen, and the payout rule is only advisory. Target 50–150 real calls. Report the pickup rate, the share of jobs confirmed, and the count of "closed but customer says not done" cases. Ask the owner for a letter of intent.

**Live demo moment.** A teammate taps "Job done" on stage. Within 15 seconds a judge's phone rings; the judge opted in through a QR code. The judge says, in Hinglish, "AC lag gaya par cooling nahi ho rahi" ("The AC is installed but it is not cooling"). The dashboard flips: job reopened, payout held, manager alerted on WhatsApp. Then show the real numbers from the pilot week.

**Bolna features shown.** An API-triggered outbound call per job. A graph agent with allowed-values extraction, with extracted data sent in webhooks. Keypad confirmation. Starting the call in the customer's language. Bulbul v4 Flash voices. Transfer to a human when the customer is upset.

**Main risk.** Customers ignore the call, given the 79–81% ignore rates on commercial number series. Pre-call WhatsApp and speed are the fixes. Technicians may stand beside the customer and coach the answers. Call only after the technician has left, and add a few random checks. The "extra cash" question can create friction with the partner business, so make it optional.

### 2. ShiftPakka: night-before shift confirmation with automatic backups

**One-liner.** The evening before each shift, an AI calls every rostered gig worker to confirm they will come. When someone says no, it immediately calls the next backup worker until the slot is filled. (*Pakka* means "for sure".)

**Who is on the call, and why they pick up.** Warehouse pickers, dark-store staff, housekeeping and event staff, and security guards. The shift is their income. The call comes from the agency that pays them, at a time they know.

**The narrow script.** "Kal subah 7 baje, Warehouse X, Sector 63. Aap aa rahe hain?" ("Tomorrow 7 a.m., Warehouse X, Sector 63. Are you coming?") Answers: yes / no / not sure. On "no", the reason comes from a short list: sick, other job, travel, or no reason. Backup call: "Ek shift khali hai, kal 7 baje. Lena chahenge?" ("A shift is open, tomorrow 7 a.m. Do you want it?") Yes or no. Read back and confirm.

**Structured output and B2B buyer.** A live roster: status per slot, fill rate, minutes to backfill, no-show reasons, and a reliability score per worker. Buyers are staffing agencies and gig platforms serving quick-commerce, warehouses, events and facility management. Fill rate is the promise these agencies make to their clients. Awign, a gig-staffing firm, is a Bolna case study ([Bolna](https://www.bolna.ai/customer-story/awign)).

**Funded analog and Indian competition.** We found no funded voice company for daily shift operations. Nearby companies handle hiring instead: Vahan, an Indian blue-collar recruiter ($10M Series B) ([AgentVoice](https://agentvoice.com/blog/ai-voice-agents-funding-market-map/)), and Alex, which does screening calls ($17M Series A) ([TechBuzz](https://www.techbuzz.ai/articles/ai-recruiter-alex-lands-17m-to-replace-human-screening-calls)). The real competitor is a large staffing platform building this in-house on Bolna. Note the **overlap with JoinCall**: both ask "will you show up?" ShiftPakka differs because it runs every day and acts on the answer by calling backups. If JoinCall was dropped because of its HR buyer, the same doubt applies here.

**Real users by Oct 31.** A small staffing, event, catering or security-guard agency, or a cloud kitchen with part-time staff. Run the calls every evening for 10 days. Report the confirm rate, the minutes to backfill a "no", and no-shows compared with the week before.

**Live demo moment.** A five-slot roster is on screen, and three judges' phones act as workers. Judge 1 says "Nahi aa paunga, beemar hoon" ("I can't come, I'm sick"). The slot turns red. Within seconds Judge 2's phone rings with the backup offer. Judge 2 says yes, and the slot turns green. **The agent acts on what it hears**, which is the "real-world action" judges reward.

**Bolna features shown.** Batch campaigns with workflow execution webhooks. API-triggered follow-up calls. Allowed-values extraction. Hindi start language. Keyword biasing for site and area names.

**Main risk.** "Is voice essential?" Some workers will reply on WhatsApp instead. The answer is that low-literacy workers respond better to calls, and the pilot should measure this rather than assume it. The second risk is getting a real roster from an agency within days.

### 3. NakliGrahak: an Indic test harness that phones your voice agent

**One-liner.** Dozens of simulated Hinglish callers, with background noise, accents and language-switching, phone a company's voice agent and return a pass/fail scorecard before real customers ever hear it. (*Nakli grahak* means "fake customer".)

**Who is on the call, and why they pick up.** The other side is the customer's own voice agent, on Bolna or elsewhere. It always answers. Each simulated caller follows a short, fixed persona, so every call is narrow by design. For example: "Kannada-accented customer reschedules a delivery, gives an address with a landmark, interrupts twice, traffic noise behind."

**The narrow script.** Each test has a persona, a goal, and an expected final state, such as "the booking moved to Tuesday" or "the lead was tagged hot".

**Structured output and B2B buyer.** A scorecard per test, judged on the final data state, not on how the transcript reads. This is the tau-Voice method ([arXiv 2603.13686](https://arxiv.org/abs/2603.13686)). It includes pass^k over five repeat runs, P50/P95 latency, how the agent handled interruptions, and errors on names and numbers, plus a "what got worse" diff after every prompt change. Buyers are teams shipping voice agents in India: Bolna's paying customers, BFSI and e-commerce firms with quality teams, and Bolna's own forward-deployed engineers.

**Funded analog and Indian competition.** Hamming (YC S24) ([RoundFunded](https://www.roundfunded.com/en/yc-startups/summer-2024)) and Roark (YC W25) ([YC](https://www.ycombinator.com/companies/industry/Conversational%20AI)) both test and monitor voice agents. Cekura co-ran a YC voice-agents hackathon ([Pipecat GitHub](https://github.com/pipecat-ai/yc-voice-agents-hackathon)). The research found **no Indic task-completion benchmark for voice agents**, only speech-recognition benchmarks. We found no Indian competitor. The risk is that a global player adds Hindi, or that Bolna builds it in-house. That second outcome could also become a partnership.

**Real users by Oct 31.** This is the idea's unfair advantage: **hundreds of buildathon teams are building Bolna agents right now.** Offer a free run of 20 Hinglish callers against their agent in the Bolna Builders Slack. Fifteen to thirty teams with scorecards and quotes would be real developer users, and that is the kind of traction Grey Baker built Dependabot on.

**Live demo moment.** Take Bolna's own template agent, or a judge's agent. Press "Run 20 callers". Calls fire in parallel, and the scorecard fills: "14/20 pass on clean audio, 8/20 with traffic noise; fails on addresses." Add keyword biasing, rerun, and watch the score rise. The visible before-and-after fix is the "wow".

**Bolna features shown.** SIP trunks and numbers, the MCP server and Claude connector (to create test agents and read results in code), batch calling, extraction, keyword biasing across STT providers, and bring-your-own TTS for varied caller voices.

**Main risk.** Bots talking to bots is less dramatic than a human phone ringing. Bolna's shortlisters may also see it as tooling rather than a business with Indian enterprise buyers. Simulating realistic 8 kHz phone audio takes real engineering. Running many calls costs credits, so budget for it.

### 4. GaadiKahan: automatic check calls to truck drivers

**One-liner.** The AI calls the driver at set points in each trip to get the expected arrival time, the reason for any delay, and proof-of-delivery status. It then updates the shipper automatically. (*Gaadi kahan?* means "Where is the truck?")

**Who is on the call, and why they pick up.** The truck driver or the fleet owner hired by a transporter or 3PL (third-party logistics firm). Human coordinators already phone drivers during trips, so the call itself is familiar; the AI takes over those calls. (We have no published count of such calls per trip, so check this with your first transporter.) The call comes from the company paying them. **Safety rule:** the agent first asks "Kya aap gaadi chala rahe hain?" ("Are you driving?"). If yes, it promises a callback in 10 minutes and hangs up. Better still, schedule calls for planned stops.

**The narrow script.** "Gaadi MH12AB1234, Pune se Delhi. Abhi kaun se shehar ke paas hain?" ("Truck MH12AB1234, Pune to Delhi. Which city are you near now?") Then: delivery today, tomorrow, or later? Any delay? The reason comes from a list: traffic, breakdown, waiting to load, checkpost, rest. After delivery: "POD mil gaya? Photo WhatsApp par bhejiye." ("Did you get the proof of delivery? Please send a photo on WhatsApp.")

**Structured output and B2B buyer.** A trip-status row with rough location, expected arrival, delay code and POD status, plus an exceptions queue and automatic WhatsApp updates to the shipper. GPS shows *where* a truck is. The call captures what GPS cannot: the reason for the delay, a promised arrival time, and the POD. Buyers are small and mid-size transporters, 3PLs and shippers' logistics teams.

**Funded analog and Indian competition.** HappyRobot raised a $15.6M Series A led by a16z, with YC participating, for freight carrier calls. One customer made 100k+ AI calls ([Pulse2](https://pulse2.com/happyrobot-ai-based-voice-solutions-company-raises-15-6-million-series-a)). We found no funded Indian voice startup focused on logistics, although Bolna lists logistics as a vertical ([Bolna](https://www.bolna.ai/newsroom/bolna-bags-63-million-seed-funding-led-by-general-catalyst-to-build-indias-voice-ai-platform)). TRAI's new 1601 series for logistics firms gives a clear legal path to production ([MediaNama](https://www.medianama.com/2026/08/223-trai-1601-series-logistics-courier-services/)).

**Real users by Oct 31.** Only feasible if one teammate's family or friends run a transport business, or the team can reach a small 3PL quickly. Target 20–50 real trip calls.

**Live demo moment.** Three trucks are on a map. A judge plays the driver while highway noise plays through a speaker: "Kharkhoda ke paas hoon, toll pe jam hai, kal subah tak pahunchunga" ("I'm near Kharkhoda, there's a jam at the toll, I'll arrive by tomorrow morning"). The row updates to delay "traffic", arrival "tomorrow 8 a.m.", and the shipper's WhatsApp pings.

**Bolna features shown.** Noise handling, keyword biasing for city and highway names, scheduled batch calls, allowed-values extraction and webhooks. It also lands on Bolna's own named pain points: noise and place recognition.

**Main risk.** Place names in dialect over a noisy cabin line, where Hindi errors approach 22%. Driver safety. And finding a real transporter in 13 days. **If the team has a transporter contact, this idea moves up to the top two**, because its venture story (a HappyRobot for India) is the strongest of all ten.

### 5. MilaanCall: GST mismatch follow-up calls to suppliers

**One-liner.** It calls suppliers whose invoices are missing from the buyer's GST records and gets a dated promise to file, so the buyer can claim its tax credit. (*Milaan* means "matching" or "reconciliation".)

**Background in plain words.** Under India's GST, a business can subtract the tax it paid to suppliers from the tax it owes. This is called input tax credit, or ITC. The credit shows up only if the supplier reports that invoice in its own GST return. The government's GSTR-2B statement tells the buyer which invoices suppliers have reported. Missing invoices mean the buyer loses real money until the supplier files.

**Who is on the call, and why they pick up.** The supplier's accountant or owner, usually a small business. The call comes from their own customer, a relationship they want to keep, and it is about a fixable paperwork gap.

**The narrow script.** "Calling for the accounts team of [Buyer]. Invoice 1234, dated 5 September, for ₹48,000, does not show in our GST records. Have you filed it?" Answers: filed / will file / dispute / wrong GSTIN (the supplier's GST registration number). On "will file", the agent asks when: this week, by the next filing date, or next month. Read back and confirm. **The agent speaks all the invoice details**, and the supplier only answers with short words or dates.

**Structured output and B2B buyer.** A status for each invoice, matched to GSTR-2B: filed, promised by a date, disputed, or wrong GSTIN. It comes with a follow-up queue and a "₹ of credit at risk" counter. Buyers are CA firms (chartered accountants; one firm serves dozens of client companies) and finance teams at mid-size companies. This is finance-operations software, close to Grey Baker's GoCardless and Pincites background ([YC blog](https://www.ycombinator.com/blog/chris-golda-and-grey-baker-general-partners)).

**Funded analog and Indian competition.** None found, in the US or India. This problem exists only in India. Reconciliation software that *finds* mismatches is common. MilaanCall takes over the *chasing*, which today happens by phone and email. Before pitching, check which reconciliation tools already offer automated supplier follow-up.

**Real users by Oct 31.** One or two CA firms; most teams know a CA. Use one consenting client's real mismatch list and call 20–40 suppliers. Report the share who give a dated promise. Actual filing will lag past October 31, so present it as a leading indicator.

**Live demo moment.** Upload a mismatch file. The screen shows "₹3.2 lakh credit at risk". Click "Chase". Judges' phones ring as suppliers. One says "Haan, 11 tareekh tak file kar denge" ("Yes, we'll file by the 11th"). That row turns amber with a date, and the at-risk counter drops.

**Bolna features shown.** A batch campaign from a CSV with per-call variables, numbers spoken in English (a Bolna India feature, per [TechCrunch](https://techcrunch.com/2026/01/20/bolna-nabs-6-3-million-from-general-catalyst-for-its-india-focused-voice-orchestration-platform/)), date and allowed-values extraction, workflow webhooks and MCP.

**Main risk.** Busy suppliers who find the call annoying. The tone can feel close to collections (Vasooli), so keep it strictly about filing, never about payment. Financial data is sensitive. And the real outcome, credit recovered, arrives after the deadline.

### 6. StockPucho: parallel stock checks across medicine distributors

**One-liner.** When a hospital pharmacy or chemist cannot find a medicine, the AI calls 5–10 distributors at the same time. It returns a ranked list of who has the item, how much they have, at what price, and how fast they can deliver. (*Stock pucho* means "ask about stock".)

**Who is on the call, and why they pick up.** The distributor's order desk. A buyer is calling, and taking orders is their business. The agent only asks. It never bargains, which keeps it clear of MolBhav.

**The narrow script.** "Calling for ABC Pharmacy, Indiranagar. Do you have Meropenem 1 g injection?" Yes or no. Then quantity, price per unit, and delivery today or tomorrow. Read back.

**Structured output and B2B buyer.** A ranked table (distributor, available, quantity, price, delivery time) and a button that sends a purchase order on WhatsApp. Buyers are hospital pharmacies, pharmacy chains and nursing homes. The same pattern can later cover auto parts and building materials.

**Funded analog and Indian competition.** The hackathon precedents are strong: Procuro, judges "blown away" ([ElevenLabs](https://elevenlabs.io/blog/announcing-the-winners-of-the-elevenlabs-worldwide-hackathon)), and Call My Parts ([Google Cloud](https://cloud.google.com/blog/topics/developers-practitioners/winners-and-highlights-of-the-gemini-live-agent-challenge)). The closest funded company is Mercura (YC W25), which captures quotes and orders for distributors ([Extruct W25](https://www.extruct.ai/data-room/ycombinator-companies-w25/)). The pattern is now **overdone in hackathon galleries** ([Cartesia gallery](https://cerebralvalley.ai/e/cartesia-voice-agents-hackathon/hackathon/gallery)), so the pharma-specific, Indian-language angle must be loud.

**Real users by Oct 31.** One local chemist or small hospital pharmacy, working on its real shortages for a week. Call only distributors it already buys from, with its permission and with AI disclosure.

**Live demo moment.** Type in a drug name. Three judges' phones ring *at once* as distributors, and the table fills live. One says "Nahi hai, kal aayega" ("Don't have it, it arrives tomorrow"), and that row drops in the ranking.

**Bolna features shown.** Concurrent outbound calls. Sarvam keyword biasing for up to 50 drug names, which is a near-perfect showcase of the October feature. Extraction. Webhooks.

**Main risk.** Drug names misheard on noisy lines. Distributors annoyed by AI calls. And a simpler competitor: if distributors already answer WhatsApp broadcasts faster, voice adds little. Test that first.

### 7. CritAlert: critical lab results called through to the doctor, with proof

**One-liner.** When a diagnostic lab finds a dangerous test value, the AI calls the referring doctor, reads the result, and asks the doctor to repeat it back. It logs who acknowledged it and when, and escalates if nobody answers.

**Who is on the call, and why they pick up.** The referring doctor or their clinic nurse. They want urgent results about their own patient. The lab wants a written record of who was told and when. Lab quality standards usually expect that record, but confirm the exact accreditation (NABL) rule with a lab before pitching it.

**The narrow script.** "This is the automated critical-result line of XYZ Labs. Patient initials R.K., 64, male. Potassium 6.9, critical high. Please repeat the value." The agent checks the read-back against the report. "Am I speaking with Dr. Sharma?" Yes or no. If there is no answer in 5 minutes, it calls a second number, then hands over to the lab's pathologist (a human).

**Structured output and B2B buyer.** An audit log for each result: test, value, who was called, time, who acknowledged, whether the read-back matched, and each escalation step. Buyers are mid-size lab chains and hospital labs.

**Funded analog and Indian competition.** None found anywhere.

**Real users by Oct 31.** Hard. No lab will let a two-week-old bot call doctors about real patients. The realistic version is a shadow pilot: replay anonymised past critical results to volunteer doctors, or run the lab's internal test calls, and collect a lab's letter of intent.

**Live demo moment.** Judge 1, the doctor, does not pick up. Judge 2's phone rings next. Judge 2 repeats "5.9". The agent corrects: "The value is 6.9, please repeat." The log turns green with a timestamp.

**Bolna features shown.** An escalation workflow, transfer to a human, keypad confirmation, keyword biasing for medical terms, and webhooks into the lab's system.

**Main risk.** Clinical liability and patient-data rules (DPDP). Doctors who dislike robot calls. And voicemail detection, which is unreliable, so treat voicemail as "not acknowledged".

### 8. PreAuthPing: claim-status calls from hospitals to insurance TPAs

**One-liner.** It calls insurance TPA helpdesks for hospital billing desks to get the status of cashless pre-authorisations and claims, then updates the billing sheet. A TPA, or third-party administrator, processes health-insurance claims for insurers. Pre-authorisation is the insurer's approval before cashless treatment.

**Who is on the call, and why they pick up.** A TPA helpdesk agent. Answering these calls is their job.

**The narrow script.** "Calling from City Hospital billing. Claim ID [spoken by the agent]. What is the status?" Approved / query raised / pending / rejected. If approved, the amount. If a query was raised, which document is needed, from a list: discharge summary, bills, ID proof, or other.

**Structured output and B2B buyer.** A claim-status row, the approved amount, the type of pending document, and an alert to the billing desk. Buyers are hospital billing and revenue teams and nursing homes.

**Funded analog and Indian competition.** This has the best-proven model of all ten. SuperDial raised a $15M Series A to automate insurer calls ([Fierce Healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/voice-ai-company-superdial-picks-15m-series-automate-insurance-calls)). LunaBill (YC F25) ([Extruct F25](https://www.extruct.ai/data-room/ycombinator-companies-f25/)) and Toothy AI (YC W25) ([YC](https://www.ycombinator.com/companies/industry/Conversational%20AI)) call insurers too. We found no Indian analog.

**Real users by Oct 31.** Hard. It needs a hospital's real claims and access to TPA phone lines.

**Live demo moment.** The agent works through a fake TPA phone menu using keypad tones, then a judge, playing the TPA rep, gives a status. The billing sheet updates.

**Bolna features shown.** Keypad tones sent over SIP to navigate phone menus, patience on hold, extraction and MCP.

**Main risk.** Phone menus and long hold times. The research found **no data on how well AI agents navigate phone menus**. TPA reps may refuse to share data with a bot. Patient data is sensitive. Hospital sales cycles are slow.

### 9. ReConfirm: hotel booking reconfirmation for travel agencies

**One-liner.** A few days before a guest arrives, it calls the hotel to reconfirm the booking a travel agent made. Missing or changed bookings are flagged before the guest reaches the front desk.

**Who is on the call, and why they pick up.** Hotel front-desk or reservations staff. Reconfirmation calls are routine, and hotels want to keep agency business.

**The narrow script.** "Calling from XYZ Travels. Booking for Mr. Rao, two deluxe rooms, 22 to 24 November, confirmation number ABC123 [spoken by the agent]. Is it in your system?" Yes / not found / changed. Then: breakfast included? Early check-in possible?

**Structured output and B2B buyer.** A booking-status table and an issues queue. Buyers are small travel agencies, destination-management companies, corporate travel desks and wedding planners.

**Funded analog and Indian competition.** Codyco (YC F25) and Riviera (YC W25) build AI for the hotel's *inbound* side ([YC](https://www.ycombinator.com/companies/industry/Conversational%20AI); [Extruct W25](https://www.extruct.ai/data-room/ycombinator-companies-w25/)). As hotels adopt them, ReConfirm becomes an agent-to-agent call, the GibberLink story in B2B form. We found no Indian competitor.

**Real users by Oct 31.** Travel agents are easy to find. Call their real upcoming bookings with their consent and aim for 30–80 calls.

**Live demo moment.** The judge, playing the front desk, says "Mr. Rao? Nahi mil raha" ("Can't find Mr. Rao"). A red flag appears and the agency gets a WhatsApp alert: "Fix before the guest lands."

**Bolna features shown.** Scheduled batch calls, a start language chosen by the hotel's state, extraction, and transfer to the agent.

**Main risk.** Modest venture scale. Larger hotels already confirm through booking software, so the market is mainly small, unconnected hotels.

### 10. RosterCall: cab-pickup confirmation for night-shift tech workers

**One-liner.** The evening before, it calls night-shift employees at IT, BPO and GCC (global capability centre) offices to confirm their cab pickup, so transport vendors stop sending cabs for people who are not coming.

**Who is on the call, and why they pick up.** The employee, who wants a reliable pickup.

**The narrow script.** "Your pickup tomorrow is 9:40 p.m. from Prestige Tech Park Gate 2. Are you coming?" Yes / no / different time, chosen from a short list of slots.

**Structured output and B2B buyer.** A confirmed roster and cancelled seats, which feed routing. Buyers are transport vendors and facilities teams at tech offices. This is the most "tech industry" buyer on the list.

**Funded analog and Indian competition.** None found for voice. Most offices already use a transport app with in-app confirmation, so first find out what share of employees ignore it.

**Real users by Oct 31.** Hard. It needs a company's live roster.

**Live demo moment.** A judge changes the pickup time by voice, and the route map redraws.

**Bolna features shown.** Batch calls, extraction, and English/Hindi switching.

**Main risk.** **It fails the "is voice essential?" test** if an app button already does the job. We kept it only as the most tech-industry option.

**Near misses we dropped.** Daily mandi-price collection from commission agents is real but agricultural, and its venture case is unclear. Warehouse dock-slot confirmation is narrow but small. Distributor stock and claims reporting is too close to BeatBot. Frontline-worker daily reporting is too close to FieldLog. Cash-on-delivery and address confirmation is crowded, and addresses are exactly where Indian speech recognition fails.

## KaamHua, ShiftPakka and NakliGrahak lead the scoring

We scored each idea from 1 (weak) to 5 (strong) on seven tests that come from the evidence above. **Wants the call**: will the other side pick up and cooperate? **Narrow and reliable**: does the script stay inside yes/no, numbers and short lists? **Users by Oct 31**: can a two-person team get real calls or real users in 13 days? **Demo impact**: is there a live moment judges can touch? **Venture and YC story**: is there a large market and a funded analog? **Bolna fit**: does it match Bolna's verticals, new features and stated pain points? **Open space**: how few competitors are there (5 means wide open)? The scores are our judgement, built on the cited research. They are not measured data.

| Rank | Idea | Wants the call | Narrow and reliable | Users by Oct 31 | Demo impact | Venture and YC story | Bolna fit | Open space | **Total /35** |
|---|---|---|---|---|---|---|---|---|---|
| 1 | KaamHua (proof-of-service) | 4 | 5 | 4 | 5 | 4 | 4 | 5 | **31** |
| 2 | ShiftPakka (shift confirmation) | 5 | 5 | 4 | 4 | 4 | 5 | 3 | **30** |
| 3 | NakliGrahak (Indic agent testing) | 5 | 5 | 5 | 3 | 4 | 4 | 3 | **29** |
| 4 | GaadiKahan (truck check calls) | 4 | 4 | 3 | 4 | 5 | 5 | 4 | **29** |
| 5 | MilaanCall (GST mismatch chasing) | 3 | 5 | 3 | 4 | 4 | 4 | 5 | **28** |
| 6 | StockPucho (pharma stock checks) | 4 | 4 | 3 | 5 | 4 | 5 | 2 | **27** |
| 7 | CritAlert (critical lab results) | 5 | 5 | 2 | 4 | 3 | 3 | 5 | **27** |
| 8 | PreAuthPing (TPA claim status) | 4 | 4 | 2 | 3 | 5 | 3 | 5 | **26** |
| 9 | ReConfirm (hotel reconfirmation) | 4 | 4 | 4 | 3 | 3 | 3 | 4 | **25** |
| 10 | RosterCall (cab pickup) | 4 | 5 | 2 | 3 | 3 | 3 | 3 | **23** |

Ties are broken by "Users by Oct 31", because the brief asks for real users. That puts NakliGrahak above GaadiKahan and StockPucho above CritAlert.

**First: KaamHua.** It has the cleanest story for both gates. For Bolna, it is a measurable rupee outcome (payouts held on jobs that were not really done), in a home-services vertical Bolna already sells to. For Grey Baker, it is a workflow product with a payment rule at its core, not "a voice bot". The demo is the strongest of the ten: a tap on stage, a phone ringing, a payout flipping to "held". Draft 200-character description: *"KaamHua calls customers minutes after a technician closes a job, confirms in Hindi or English that the work was done, and releases the technician's payout only on a yes. Built on Bolna."*

**Second: ShiftPakka.** It has the best pickup and the best Bolna fit. The call is about the worker's own income, and Bolna's case studies already include a staffing firm. The chained backup calls show an agent *acting* on what it hears. The JoinCall overlap is its main weakness. Draft: *"ShiftPakka calls every gig worker the night before a shift, and when someone says no it instantly calls backups until the roster is full. Fewer no-shows for staffing agencies."*

**Third: NakliGrahak.** It is the only idea whose users are guaranteed to exist before October 31: the other buildathon teams. It also speaks directly to a judge who built a developer tool. Choose it if the team would rather ship a developer product than run a field pilot. Draft: *"NakliGrahak phones your voice agent with 20 noisy, accented Hinglish callers and scores every call on the final result, so Indian teams catch failures before real customers do."*

## Conclusion

The research changes the question from "which voice idea is clever?" to "**which phone call does someone already expect, and what business decision does its answer trigger?**" The winners that called real people did not win because the conversation was smart. They won because a phone rang and something changed on screen. The Indian evidence (79–81% of commercial-series calls ignored, 12–22% Hindi error rates, new A2P rules) makes the same filter stricter: a consented, event-triggered call where the agent does the talking and the human gives short answers. The most useful insight for venture scale is that the **call itself is a commodity**, a "price game" in Ringg's words. Defensibility comes from what the answer controls: a technician payout, a filled roster, a tax credit, a test result. Pitch the control point, not the voice.

Two practical implications follow for the 13 days left. First, the strongest evidence a two-person team can bring to Bolna's interviews is **a week of real calls with an honest outcome metric** (resolution with hang-ups excluded, not inflated "containment"), plus a small repeat-run test score. NakliGrahak's method can be applied to whichever idea the team builds, at almost no extra cost. Second, the ranking depends on who the team can reach. A transporter contact makes GaadiKahan a top-two pick. A CA in the family makes MilaanCall competitive. Pick the idea whose first real user you can phone tomorrow.
