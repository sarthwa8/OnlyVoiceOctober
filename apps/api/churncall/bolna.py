"""Everything that knows Bolna's API shapes: the HTTP client, webhook parsing, statuses and source IPs.

If Bolna's payloads turn out different from what we expect (where user_data comes back in the webhook
is still unconfirmed), this is the one file to change.

Endpoint paths and payload field names marked VERIFY are our best understanding of Bolna's API;
confirm them against the Bolna docs before relying on them.
"""

from __future__ import annotations

import httpx
from pydantic import BaseModel

from .config import get_settings

# Bolna posts a webhook on every status change; only "completed" carries the full transcript.
COMPLETED = "completed"
# Statuses that mean the call ended without a conversation.
NOT_CONNECTED = {"no-answer", "busy", "failed", "canceled", "stopped", "error", "balance-low"}
# Bolna's published webhook source IPs (agent create API docs, checked 2026-10-20).
WEBHOOK_IPS = {"13.203.39.153", "13.126.9.249", "13.202.133.53"}


class BolnaClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, agent_id: str | None = None):
        s = get_settings()
        self.api_key = api_key or s.bolna_api_key
        self.base_url = (base_url or s.bolna_api_base).rstrip("/")
        self.agent_id = agent_id or s.bolna_agent_id

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def start_outbound_call(
        self, phone_e164: str, user_data: dict, bypass_guardrails: bool = True, timeout: float = 15.0
    ) -> dict:
        """Place a call the user explicitly requested ("call me now"). Never use for cold calls.

        bypass_guardrails: the user asked for this call right now, so Bolna's calling-hours guardrails
        must not block it (e.g. a tap at 11 pm). Bolna's /call documents `bypass_call_guardrails` [VERIFY name].
        user_data fills the {{variables}} in the agent prompt; include invite_token/channel so the webhook can link back.
        """
        payload = {
            "agent_id": self.agent_id,  # VERIFY field name
            "recipient_phone_number": phone_e164,  # VERIFY field name
            "user_data": user_data,  # fills {{variables}} in the agent prompt
            "bypass_call_guardrails": bypass_guardrails,  # VERIFY field name
        }
        resp = httpx.post(f"{self.base_url}/call", json=payload, headers=self._headers(), timeout=timeout)  # VERIFY path
        resp.raise_for_status()
        return resp.json()

    def mint_web_session(self, user_data: dict, timeout: float = 15.0) -> dict:
        """Mint a single-use (~120 s) browser call session for the Web Call SDK.

        The SDK never sees our API key: the browser asks our server, our server asks Bolna.
        POST /web-call/freeswitch-session, per the @bolna/web-call 3.0.1 README (the docs page says
        /web-call/session, which is older). The response includes run_id (the execution id). Needs the
        Web Call SDK enabled on the account.
        """
        payload = {"agent_id": self.agent_id, "user_data": user_data}
        resp = httpx.post(f"{self.base_url}/web-call/freeswitch-session", json=payload, headers=self._headers(), timeout=timeout)
        resp.raise_for_status()
        return resp.json()


# ---------- webhook payloads ----------
# Bolna's exact payload shape is not confirmed yet (VERIFY with a real call), so the parser accepts the
# field names we expect plus a few likely alternatives, and keeps the raw payload.

class Turn(BaseModel):
    speaker: str  # "agent" or "user"
    text: str


class CallRecord(BaseModel):
    execution_id: str
    status: str
    duration_s: float | None
    recording_url: str | None
    turns: list[Turn]
    raw: dict

    @property
    def transcript_text(self) -> str:
        return "\n".join(f"{t.speaker}: {t.text}" for t in self.turns)

    @property
    def user_talk_ratio(self) -> float:
        user = sum(len(t.text.split()) for t in self.turns if t.speaker == "user")
        total = sum(len(t.text.split()) for t in self.turns)
        return user / total if total else 0.0

    @property
    def user_turns(self) -> int:
        return sum(1 for t in self.turns if t.speaker == "user")


_AGENT_NAMES = {"assistant", "agent", "bot", "ai"}


def _first(d: dict, *keys, default=None):
    for k in keys:
        if d.get(k) is not None:
            return d[k]
    return default


def _parse_transcript(value) -> list[Turn]:
    if isinstance(value, list):
        turns = []
        for item in value:
            role = str(_first(item, "role", "speaker", default="user")).lower()
            text = str(_first(item, "content", "text", "message", default="")).strip()
            if text:
                turns.append(Turn(speaker="agent" if role in _AGENT_NAMES else "user", text=text))
        return turns
    if isinstance(value, str):
        turns = []
        for line in value.splitlines():
            if ":" not in line:
                continue
            role, text = line.split(":", 1)
            role = role.strip().lower()
            if text.strip():
                turns.append(Turn(speaker="agent" if role in _AGENT_NAMES else "user", text=text.strip()))
        return turns
    return []


def parse_webhook(payload: dict) -> CallRecord:
    telephony = payload.get("telephony_data") or {}
    return CallRecord(
        execution_id=str(_first(payload, "id", "execution_id", "call_id", default="")),
        status=str(_first(payload, "status", "call_status", default="unknown")).lower(),
        duration_s=_first(payload, "conversation_duration", "duration", default=None) or _first(telephony, "duration"),
        recording_url=_first(payload, "recording_url", default=None) or _first(telephony, "recording_url"),
        turns=_parse_transcript(_first(payload, "transcript", "conversation", default=[])),
        raw=payload,
    )


def call_variables(payload: dict) -> dict:
    """The user_data we sent, as echoed in the webhook. Its exact place isn't confirmed, so check both
    context_details and context_details.recipient_data (batch calls put CSV columns there)."""
    ctx = payload.get("context_details") or payload.get("user_data") or {}
    if not isinstance(ctx, dict):
        return {}
    nested = ctx.get("recipient_data")
    return {**(nested if isinstance(nested, dict) else {}), **ctx}
