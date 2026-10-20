# Message to Bolna (paste into the Builders Slack or email support@bolna.ai)

> Send from the account that registered for the Buildathon. Add your account email and agent ID.

Hi Bolna team, we're building a Buildathon project that interviews churned SaaS users (AI voice interviewer). Could you help with a few things?

1. **Please enable the Web Call SDK** (beta) on our account (email: ___). We want users to talk to the agent from a browser tab.
2. **Outbound number:** which countries can our default outbound number call? Our pilot users are in India and possibly the US. If it's limited, how do we get a local number?
3. **Webhooks:** do they support a custom secret header, or should we allow only your published source IPs?
4. **`user_data`:** where does it appear in the post-call webhook, `context_details` or `context_details.recipient_data`? Can it override the whole system prompt, or only fill `{{variables}}`?
5. **Guardrails:** our users tap "call me now", so we send `bypass_call_guardrails: true`. Is that the right field, and is it allowed for user-requested calls?
6. **Credits:** is there a Buildathon credit allowance we can use for a ~100-call pilot this week?

Thanks! Agent ID: ___
