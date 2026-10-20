"""What happens when Bolna sends a webhook.

Bolna posts on every status change of a call. Steps, in order:
  1. save the raw payload (so no call is ever lost, whatever fails later)
  2. update the invite funnel (completed / too short / not connected)
  3. on the final "completed" status only, once per call: store the transcript
  4. extract the churn insight (verified quotes) with the configured LLM
A failing step is logged to errors.jsonl and never stops the steps after it.
"""

from __future__ import annotations

import json

from . import invites, store
from .bolna import COMPLETED, NOT_CONNECTED, CallRecord, call_variables, parse_webhook
from .extraction import extract_insight

MIN_USER_TURNS = 3  # a "completed" call only counts if the user actually talked


def record_call_outcome(payload: dict, record: CallRecord) -> str | None:
    """Update the invite funnel from one Bolna webhook. Ignores in-between statuses and is safe to run
    more than once for the same call. Returns the invite token, if the call belongs to an invite."""
    variables = call_variables(payload)
    token = variables.get("invite_token") or invites.token_for_execution(record.execution_id)
    if not token or invites.get_invite(token) is None:
        return None
    if record.status == COMPLETED:
        if record.user_turns >= MIN_USER_TURNS:
            invites.mark_completed(token, record.execution_id, channel=variables.get("channel"))
        else:
            invites.log_event_once(token, "call_too_short", {"user_turns": record.user_turns}, execution_id=record.execution_id)
    elif record.status in NOT_CONNECTED:
        invites.log_event_once(token, "call_not_connected", {"status": record.status}, execution_id=record.execution_id)
    return token


def _step(name: str, execution_id: str, fn) -> None:
    try:
        fn()
    except Exception as exc:  # one failing step must never lose the call
        store.append("errors.jsonl", {"at": store.now(), "step": name, "execution_id": execution_id, "error": repr(exc)})


def _store_transcript_once(record: CallRecord) -> bool:
    """Store the transcript of a completed call exactly once. Keyed on transcripts (not insights) so a
    failed extraction isn't retried, and the transcript isn't stored again, every time Bolna resends."""
    with store.locked():
        if record.status != COMPLETED or (
            record.execution_id and store.has("transcripts.jsonl", execution_id=record.execution_id)
        ):
            return False
        store.append("transcripts.jsonl", record.model_dump(exclude={"raw"}))
        return True


def _extract(payload: dict, record: CallRecord) -> None:
    insight, dropped = extract_insight(record, company_context=json.dumps(call_variables(payload)))
    store.append(
        "insights.jsonl",
        {
            "execution_id": record.execution_id,
            "user_talk_ratio": round(record.user_talk_ratio, 2),
            "quotes_dropped": dropped,
            "insight": insight.model_dump(),
        },
    )


def handle_bolna_webhook(payload: dict) -> None:
    store.append("webhooks.jsonl", {"at": store.now(), "payload": payload})
    record = parse_webhook(payload)
    _step("funnel", record.execution_id, lambda: record_call_outcome(payload, record))
    if not _store_transcript_once(record) or not record.turns:
        return
    _step("extraction", record.execution_id, lambda: _extract(payload, record))
