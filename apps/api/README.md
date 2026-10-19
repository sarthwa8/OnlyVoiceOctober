# ChurnCall API: Person A's Day-1 build

## What's here
| Path | What it does |
|---|---|
| `../../agents/interviewer/prompt.md` | Interviewer system prompt v1, with placeholders filled per call |
| `../../agents/interviewer/config.json` | Intended Bolna agent settings (fields marked VERIFY) |
| `churncall/guide.py` | Fills the prompt from company + contact context |
| `churncall/bolna.py` | Starts a "call me now" outbound call through Bolna |
| `churncall/webhook.py` | Parses Bolna's post-call webhook (transcript, recording, duration) and computes the user talk ratio |
| `churncall/llm.py` | Provider switch: Anthropic (default) or any OpenAI-compatible endpoint, including free tiers. JSON + schema validation + one retry for non-Anthropic models. |
| `churncall/extraction.py` | Structured extraction through `llm.py` of the churn insight, then **drops any quote not found word for word in the user's lines** |
| `churncall/main.py` | FastAPI: `GET /healthz`, `POST /calls` (refuses without consent), `POST /bolna/webhook` |
| `../../eval/interviews/simulate.py` | Text simulation: our interviewer vs 6 churned-user personas, with talk ratio and leading-question checks |

## Run
```bash
python3 -m venv .venv && .venv/bin/pip install -r apps/api/requirements.txt
cp .env.example .env   # fill ANTHROPIC_API_KEY, BOLNA_API_KEY, BOLNA_AGENT_ID, WEBHOOK_SECRET
.venv/bin/python -m pytest -q apps/api/tests
cd apps/api && ../../.venv/bin/uvicorn churncall.main:app --reload
# expose the webhook for Bolna:  ngrok http 8000  → set https://<id>.ngrok.app/bolna/webhook in Bolna
python eval/interviews/simulate.py --persona price_cover   # costs API money; keep runs small
```
Results go to `data/*.jsonl` (transcripts, insights, errors). That's enough for the kill test; Supabase comes after it.

## Day-0 checklist: confirm against the Bolna docs or dashboard (I couldn't reach bolna.ai from my environment)
- [ ] Outbound call endpoint path + field names (`/call`, `agent_id`, `recipient_phone_number`, `user_data`) in `bolna.py`
- [ ] How `user_data` reaches the prompt. If Bolna can't take a whole system prompt per call, put the template in the agent and pass only the variables.
- [ ] Web Call SDK: how to start a browser session and pass per-session context
- [ ] Webhook payload: save one real payload to `apps/api/tests/fixtures/` and adjust `webhook.py`
- [ ] Webhook auth: does Bolna sign webhooks or support a custom header? Wire it into `WEBHOOK_SECRET`.
- [ ] Turn-taking settings in `config.json` (endpointing, silence re-prompt, hangup, max duration)

## Using a free LLM instead of Claude
Set `LLM_PROVIDER=openai_compat`, `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` (and optionally `LLM_MODEL_CHEAP`) in `.env`. See `.env.example`.
Free models are weaker at structured output, so `llm.py` asks for JSON, validates it against the schema and retries once; the verbatim-quote check still runs. Compare the free model's extraction against Claude on the same 5 transcripts before trusting it. Free tiers have rate limits and may use your data for training, so don't send real customer transcripts to a provider whose terms you haven't read.
