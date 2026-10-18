"""Normalises Bolna post-call webhook payloads into one internal shape.

Bolna's exact payload shape is not confirmed yet (VERIFY with a real call on Day 0), so the
parser accepts the field names we expect plus a few likely alternatives, and keeps the raw payload.
"""

from __future__ import annotations

from pydantic import BaseModel


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


def parse_bolna_webhook(payload: dict) -> CallRecord:
    telephony = payload.get("telephony_data") or {}
    return CallRecord(
        execution_id=str(_first(payload, "id", "execution_id", "call_id", default="")),
        status=str(_first(payload, "status", "call_status", default="unknown")),
        duration_s=_first(payload, "conversation_duration", "duration", default=None) or _first(telephony, "duration"),
        recording_url=_first(payload, "recording_url", default=None) or _first(telephony, "recording_url"),
        turns=_parse_transcript(_first(payload, "transcript", "conversation", default=[])),
        raw=payload,
    )
