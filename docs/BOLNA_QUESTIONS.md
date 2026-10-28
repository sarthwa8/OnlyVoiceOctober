# Message to Bolna (paste into the Builders Slack or email support@bolna.ai)

> v2 · 2026-10-28. Rewritten after the first real interview: web calls already work, and items 3–5 are answered from that call, so this only asks what still blocks us. Add your account email and agent ID.

Hi Bolna team! We're building **ChurnCall** for the Buildathon: an AI voice interviewer that talks to a SaaS company's churned users and turns the calls into churn reasons with exact quotes. Browser calls work well on our account. A few things would unblock our pilot this week:

1. **Trial limit:** outbound calls fail with *"Trial accounts can only make calls to verified phone numbers."* Could you lift it for the Buildathon, or tell us how to upgrade? Our users tap "call me now" themselves (never cold calls).
2. **Phone number:** our account lists no phone number. Which countries could a number call (India first, maybe the US)?
3. **Concurrent calls:** our limit is 2. Could it go to 5–10 for this week, so invite waves don't hit "busy"?
4. **Cost units:** a 2.7-minute browser call shows `total_cost` 16.5. Is that US cents? Our wallet shows 500, so we'd like to know how many calls that covers.
5. **Credits:** is there a Buildathon credit allowance for a ~50–100-call pilot?
6. **Keyword boosting:** what's the transcriber config field for boosting product names with Deepgram nova-3 (e.g. `keywords` / `keyterm`)? Can it take a `{{variable}}` from `user_data`?

Thanks! Account email: ___ · Agent ID: ___

---
**Already answered (from our first real call on 2026-10-20, no need to ask):** web calls are enabled; `user_data` comes back under `context_details.recipient_data`; webhooks arrive from your published IPs (we check those, so no secret header is needed); `POST /call` accepts `bypass_call_guardrails`.
