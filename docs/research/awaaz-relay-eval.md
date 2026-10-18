# Evaluation: Awaaz Relay (AI phone relay for deaf and hard-of-hearing Indians)

> 2026-10-18 · Idea from a friend · Status: **evaluated, not adopted** (the locked build is still [ChurnCall](../CHURNCALL.md))

## The idea
The deaf user types or taps quick replies. The AI speaks into a normal phone call (Hindi, Tamil or English) and shows the other party's speech as live captions. Inbound calls are answered with "This caller uses a relay, please speak normally" and captioned live.

## Facts checked
- **Rylo (formerly Nagish)** raised **$85M** in June 2026 and says it has raised over $100M in total. One source reports a valuation of about $500M; another says it wasn't disclosed. It's FCC-certified and **free to users**. ([BusinessWire](https://www.businesswire.com/news/home/20260604498117/en/), [Hearing Review](https://hearingreview.com/hearing-products/amplification/amplified-caption-phones/rylo-raises-85-million-to-expand-ai-communication-platform-for-deaf-and-hard-of-hearing-users))
- **TRAI (2018)** recommended relay desks at emergency centres and special call-centre desks for persons with disabilities. I found **no evidence of a national relay service running in India**. ([MediaNama](https://www.medianama.com/2018/07/223-trai-accessibility/), [TRAI direction, Dec 2018](https://cms.trai.gov.in/sites/default/files/2024-09/Direction04122018.pdf))

## The crux: who pays in India?
Rylo can be free for users because the **US government's relay fund (the FCC's TRS Fund) reimburses certified providers per minute** for captioned and IP relay calls. That's the engine of its revenue. **India has no such fund.** Without one, paying customers would have to be:
- **businesses**: a bank, insurer, telco or hospital helpline offering an "accessible line" under the Rights of Persons with Disabilities Act, 2016
- **employers** with deaf staff
- **the government**, via tenders or a future relay mandate
- **consumers** on freemium, where willingness to pay is low

This is unproven, and it's the single biggest risk.

## Technical notes (Bolna)
- **The bridge is feasible:** use a custom LLM endpoint as the relay. It returns the deaf user's typed text verbatim for Bolna to speak, and forwards each turn from the other party to the user's app over a websocket as captions. While the user is typing, it plays a filler line ("one moment, they're typing").
- **Captions are per turn, not word by word** [verify whether Bolna streams partial transcripts]. Typing delay makes calls slow; quick replies and predictive suggestions help.
- **Inbound calls:** the user forwards their mobile number to our Bolna number with the carrier's call-forwarding code.
- **Outbound caller ID:** calls show our virtual number, not the user's registered mobile number. Banks and other OTP-based flows that check for the registered number may fail.
- **Regulation:** person-to-person calling through virtual numbers and internet-to-phone calling are regulated in India [verify licensing for relay use].

## Scorecard vs ChurnCall
| | Awaaz Relay | ChurnCall |
|---|---|---|
| Demo emotion | ✅✅ | 🟡 |
| Proven comparable | ✅ Rylo, $85M | 🟡 AI interview platforms |
| Real users by Oct 31 | ✅ via deaf associations and schools | ✅ via pilot startups |
| Who pays in India | ❌ no relay fund; B2B accessibility unproven | ✅ SaaS teams with budget |
| Fits the brief (B2B / tech / not social impact) | 🟡 accessibility infrastructure, but mostly framed as social impact | ✅ |
| Founder–market fit | 🟡 unless someone on the team has a deaf-community link | ✅ GTM + AI research |
| Bolna fit | ✅ Indian languages, telephony | ✅ web call + outbound |

## Verdict
It's a strong idea and the best stage demo we've seen, but its business model depends on a policy (a relay fund) that India doesn't have. Keep ChurnCall, unless the team has a personal connection to the deaf community *and* wants to pitch the B2B "accessible helpline" model.
