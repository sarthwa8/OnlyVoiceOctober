"""ChurnCall API: Day-1 minimum. Webhook ingest, "call me now", and stored results.

Storage is a local JSONL file for the kill test; it moves to Supabase once the test passes.
"""

from __future__ import annotations

import hmac
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException
from pydantic import BaseModel

from .bolna import BolnaClient
from .extraction import extract_insight
from .guide import Company, Contact, render_prompt
from .webhook import parse_bolna_webhook

load_dotenv()

DATA_DIR = Path(os.environ.get("CHURNCALL_DATA_DIR", "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="ChurnCall API")


class CallMeRequest(BaseModel):
    phone_e164: str
    company: Company
    contact: Contact
    consent: bool


def _append(name: str, row: dict) -> None:
    with (DATA_DIR / name).open("a") as f:
        f.write(json.dumps(row) + "\n")


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True}


@app.post("/calls")
def call_me_now(req: CallMeRequest) -> dict:
    """User tapped "call me now". Their tap is the consent; we refuse without it."""
    if not req.consent:
        raise HTTPException(status_code=400, detail="consent required: the user must request the call")
    prompt = render_prompt(req.company, req.contact)
    result = BolnaClient().start_outbound_call(
        req.phone_e164,
        user_data={"system_prompt": prompt, "contact_name": req.contact.name, "company_name": req.company.name},
    )
    _append("calls.jsonl", {"contact": req.contact.model_dump(), "company": req.company.name, "bolna": result})
    return {"ok": True, "bolna": result}


def _process(payload: dict) -> None:
    record = parse_bolna_webhook(payload)
    _append("transcripts.jsonl", record.model_dump(exclude={"raw"}))
    if not record.turns:
        return
    context = payload.get("context_details") or payload.get("user_data") or {}
    try:
        insight, dropped = extract_insight(record, company_context=json.dumps(context))
    except Exception as exc:  # keep the transcript even if extraction fails
        _append("errors.jsonl", {"execution_id": record.execution_id, "error": repr(exc)})
        return
    _append(
        "insights.jsonl",
        {
            "execution_id": record.execution_id,
            "user_talk_ratio": round(record.user_talk_ratio, 2),
            "quotes_dropped": dropped,
            "insight": insight.model_dump(),
        },
    )


@app.post("/bolna/webhook")
def bolna_webhook(payload: dict, background: BackgroundTasks, x_webhook_secret: str | None = Header(default=None)) -> dict:
    expected = os.environ.get("WEBHOOK_SECRET", "")
    if expected and not hmac.compare_digest(x_webhook_secret or "", expected):
        raise HTTPException(status_code=401, detail="bad webhook secret")
    background.add_task(_process, payload)
    return {"ok": True}
