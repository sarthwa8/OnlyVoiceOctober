# ChurnCall: the evidence it should exist

> Researched 2026-10-18. Each claim has a source and a reliability rating: 🟢 primary or reputable · 🟡 secondary or vendor · 🔴 unverified.
> Rule for the pitch: cite only 🟢 claims, or say "vendor-reported".

## 1. Investors are paying for AI customer interviews (the category is real)
| Claim | Source | Rating |
|---|---|---|
| **Listen Labs** raised a $69M Series B (Ribbit Capital, with Sequoia, Conviction and Pear), has run more than 1M interviews, and its customers include Microsoft, Perplexity and Robinhood. Its valuation is reported above $500M. | [Pulse 2.0](https://pulse2.com/listen-labs-69-million-series-b/), [eWeek](https://www.eweek.com/news/listen-labs-ai-startup-microsoft-customers/) | 🟢 / 🟡 (valuation) |
| Listen Labs is reportedly in talks for a $125M Series C at a $1.5B valuation (Aug 2026, not confirmed) | [Dealroom](https://dealroom.co/news/143721-listen-labs-targets-125m-series-c-at-1-5b-valuation/) | 🟡 |
| **Outset** raised a $30M Series B (Dec 2025, Radical Ventures and Microsoft's fund M12), bringing its total to $51M | [GlobeNewswire](https://www.globenewswire.com/de/news-release/2025/12/10/3203401/0/en/p.html) | 🟢 |
| **Clozd** (human-run win-loss interviews) raised a $52M Series A (Greycroft) | [Clozd](https://clozd.com/blog/clozd-raises-52-million-in-series-a-round) | 🟢 |

**What this tells us:** customer interviewing is a venture-scale category. The leaders run *scheduled studies* in text or video, not interviews triggered by churn and weighted by revenue. That's our slice.

## 2. Churn is a big, recurring problem
| Claim | Source | Rating |
|---|---|---|
| B2B SaaS churn is about 3.5–5%. Sources disagree on whether that's monthly or annual; most treat it as annual for B2B overall. | [Vitally](https://vitally.io/post/saas-churn-benchmarks), [Vena](https://www.venasolutions.com/blog/saas-churn-rate) | 🟡 |
| **SMB SaaS** churns **3–7% a month** (30–58% a year), which is our wedge segment | [Vena](https://www.venasolutions.com/blog/saas-churn-rate) | 🟡 |
| Median revenue churn for startups rose from 11.3% to 12.5% (Lighter Capital 2025 benchmark) | via [Orb](https://www.withorb.com/blog/saas-churn-statistics) | 🟡 |
| A 5% increase in retention lifts profits 25–95% (Bain / Reichheld) | widely cited, e.g. [Mailmodo](https://mailmodo.com/guides/customer-retention-statistics); primary not located | 🔴 classic stat; find the original HBR/Bain piece before citing |

## 3. Today's tools don't capture the real "why"
| Claim | Source | Rating |
|---|---|---|
| In about 340 cancellations, "too expensive" was the top reason picked (38%), but most of those users **never finished onboarding** | [SEOJuice founder audit](https://seojuice.io/blog/how-bad-exitsurvey-design-skews-your-saas-churn-data) | 🟡 single product, small sample |
| Exit surveys capture the "final straw", not the root cause. Answer order biases picks toward price (primacy effect). People rarely write in "Other". | [Enterpret](https://www.enterpret.com/guides/how-to-analyze-exit-survey-responses-to-understand-why-customers-cancel), [SEOJuice](https://seojuice.io/blog/how-bad-exitsurvey-design-skews-your-saas-churn-data) | 🟡 |
| Churn-survey completion is "notoriously low", since leaving users have no incentive | [Koji](https://www.koji.so/blog/why-price-is-never-the-real-churn-reason) | 🟡 vendor |

## 4. Voice gets more than text, and an AI listener can get more honesty
| Claim | Source | Rating |
|---|---|---|
| In a **randomised** survey experiment, spoken open-ended answers were **longer and contained more information and personal experiences** than typed ones | [Galasso, Nannicini & Nozza, IZA DP 17488 (2024)](https://docs.iza.org/dp17488.pdf) | 🟢 |
| People who believed they were talking to a **computer** (not a human) disclosed more and managed their image less (USC, 239 participants) | [Lucas et al. 2014, *Computers in Human Behavior* 37:94–100](https://psmag.com/social-justice/id-never-admit-doctor-computer-sure-84001/) | 🟢 one lab study, not about churn |
| A 2024 study found AI conversational interviewing produces data comparable to traditional interviews | cited in the search summary; paper not located | 🔴 |
| An AI-interview vendor reports ~90% completion vs ~46% for static surveys | vendor claim | 🔴 don't cite |

## 5. Consent rules support our "user starts the call" design
| Claim | Source | Rating |
|---|---|---|
| The **FCC (Feb 8, 2024)** ruled that AI-generated voices are "artificial" voices under the US robocall law (the TCPA). Outbound AI calls generally need **prior express consent**, plus disclosure and opt-out. | [Hunton](https://huntonak.com/privacy-and-information-security-law/fcc-issues-declaratory-ruling-that-tcpa-applies-to-ai-generated-voice-calls), [Womble Bond Dickinson](https://www.womblebonddickinson.com/us/insights/blogs/fcc-adopts-declaratory-ruling-confirming-ai-voice-calls-are-subject-tcpa-takes) | 🟢 |

**Implication:** browser voice plus calls the user asks for is a requirement, not just good UX.

## 6. ⚠️ Competitors found during this research (new)
- **Koji** (koji.so) and **Perspective AI** (getperspective.ai) market AI interviews for churn and exit intent. **We need to look at them closely on Day 1:** channel (text or voice?), whether interviews are triggered by events, pricing.
- **What could still set us apart:** voice and phone (not a chat widget), weighting by revenue from Stripe, Indian-language support, and closing the loop with win-back and tickets. Claim none of this until we've verified what they actually do.

## 7. What the evidence does NOT prove (be honest in the pitch)
- That **churned users will talk to an AI by voice at a useful rate.** No source measures this. **Our Oct 21 kill test is the evidence.**
- Any reliable statistic on what share of "too expensive" answers are really something else. The 38% figure comes from one founder's data.
- That voice beats a good text AI interviewer specifically for churn. The IZA result is about surveys in general.

## Pitch-safe one-liners
1. "Investors have put over $100M into AI customer interviews. Listen Labs alone raised $69M. But they run scheduled studies. Nobody interviews the customer at the moment they leave."
2. "Small SaaS companies lose 3–7% of customers every month, and their exit survey says 'too expensive'."
3. "A randomised study found spoken answers carry more information than typed ones, and people disclose more to a computer than to a person."
4. "Since 2024, AI voice calls need consent in the US, so in ChurnCall the user always starts the conversation."
5. "We measured it: X% of churned users completed an interview, and here's what they said." ← from the kill test.
