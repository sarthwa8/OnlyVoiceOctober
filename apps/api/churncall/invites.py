"""Invites for churned users: creating them, their event log, status and start limits.

Each churned user gets a private token. Everything that happens to an invite is an append-only
event, and status (and the funnel, see funnel.py) is worked out from those events.
See build-plans/01-invite-page.md.
"""

from __future__ import annotations

import re
import secrets
from typing import Any, Literal

from pydantic import BaseModel

from . import store
from .errors import InviteFinished, InviteNotFound, TooManyAttempts
from .interview import TRIGGERS, Company, Contact

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+[1-9]\d{7,14}$")
# Attempts: what the user tapped. Counted against MAX_STARTS and used to tell which channel a call used.
START_EVENTS = {"started_web": "web", "started_phone": "phone"}
# What counts as "started" in status and the funnel: a phone call Bolna accepted, or a browser call that actually
# connected. Minting a browser session isn't enough: it happens before the mic prompt, so someone who then
# blocks the mic never started an interview.
STARTED_EVENTS = {"started_phone": "phone", "web_connected": "web"}
MAX_STARTS = 3

# Every event an invite can have. The on-disk format is unchanged; this just rejects unknown names.
EventName = Literal[
    "opened",               # the page ran in a real browser (not a link scanner)
    "started_web",          # a Bolna browser session was minted
    "web_connected",        # the browser call connected (meta: execution_id from the SDK)
    "started_phone",        # Bolna accepted the outbound call (meta: execution_id)
    "mic_denied",
    "call_ended_client",    # the browser SDK reported the call ended (meta: reason)
    "completed",            # Bolna's final webhook with enough user talk (meta: execution_id, channel)
    "call_too_short",
    "call_not_connected",   # no answer, busy, failed... (meta: status)
    "opted_out",
]


class Event(BaseModel):
    token: str
    event: EventName
    at: str
    meta: dict[str, Any] = {}


class Invite(BaseModel):
    token: str
    company_slug: str
    contact: Contact
    email: str
    phone_e164: str | None = None
    mrr: float | None = None
    incentive: str | None = None
    email_variant: str | None = None
    created_at: str


# ---------- invites ----------

def load_company(slug: str) -> Company:
    path = store.path(f"companies/{slug}.json")
    if not path.exists():
        raise FileNotFoundError(f"no company config at {path}")
    return Company.model_validate_json(path.read_text())


def create_invite(company_slug: str, row: dict) -> Invite:
    """Validate one CSV row and store it as an invite. Raises ValueError for a bad row."""
    clean = {k: (v or "").strip() for k, v in row.items() if k}
    name, email = clean.get("name", ""), clean.get("email", "")
    if not name:
        raise ValueError("missing name")
    if not EMAIL_RE.match(email):
        raise ValueError(f"bad email {email!r}")
    phone = clean.get("phone_e164") or None
    if phone and not PHONE_RE.match(phone):
        raise ValueError(f"bad phone {phone!r} (use E.164, e.g. +919800000000)")
    trigger = clean.get("trigger") or "cancelled"
    if trigger not in TRIGGERS:
        raise ValueError(f"unknown trigger {trigger!r} (one of {', '.join(TRIGGERS)})")
    try:
        tenure = int(clean["tenure_days"]) if clean.get("tenure_days") else None
        mrr = float(clean["mrr"]) if clean.get("mrr") else None
    except ValueError as exc:
        raise ValueError(f"bad number: {exc}") from None

    invite = Invite(
        token=secrets.token_urlsafe(9),
        company_slug=company_slug,
        contact=Contact(name=name, trigger=trigger, plan=clean.get("plan") or "unknown", tenure_days=tenure),
        email=email,
        phone_e164=phone,
        mrr=mrr,
        incentive=clean.get("incentive") or None,
        email_variant=clean.get("email_variant") or None,
        created_at=store.now(),
    )
    store.append("invites.jsonl", invite.model_dump())
    return invite


def all_invites() -> list[Invite]:
    return [Invite.model_validate(r) for r in store.read("invites.jsonl")]


def get_invite(token: str) -> Invite | None:
    return next((i for i in reversed(all_invites()) if i.token == token), None)


def require_invite(token: str) -> Invite:
    invite = get_invite(token)
    if invite is None:
        raise InviteNotFound()
    return invite


def require_startable(token: str) -> Invite:
    """An invite can start at most MAX_STARTS calls, and none once completed or opted out."""
    invite = require_invite(token)
    events = events_for(token)
    if status_of(events) in ("completed", "opted_out"):
        raise InviteFinished()
    if starts_count(events) >= MAX_STARTS:
        raise TooManyAttempts()
    return invite


# ---------- event log ----------

def log_event(token: str, event: EventName, meta: dict | None = None) -> None:
    """Append one event. The name is validated, so a typo fails loudly instead of skewing the funnel."""
    store.append("invite_events.jsonl", Event(token=token, event=event, at=store.now(), meta=meta or {}).model_dump())


def log_event_once(token: str, event: EventName, meta: dict | None = None, *, execution_id: str | None = None) -> bool:
    """Log `event` unless it's already logged for this invite, or, when `execution_id` is given, for this
    invite + Bolna call (Bolna can resend the same webhook). Returns False if it was already there."""
    with store.locked():
        for e in events_for(token):
            if e["event"] == event and (execution_id is None or e.get("meta", {}).get("execution_id") == execution_id):
                return False
        log_event(token, event, {**({"execution_id": execution_id} if execution_id else {}), **(meta or {})})
        return True


def events_by_token() -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for e in store.read("invite_events.jsonl"):
        grouped.setdefault(e["token"], []).append(e)
    return grouped


def events_for(token: str) -> list[dict]:
    return events_by_token().get(token, [])


def status_of(events: list[dict]) -> str:
    names = {e["event"] for e in events}
    if "opted_out" in names:
        return "opted_out"
    if "completed" in names:
        return "completed"
    if names & STARTED_EVENTS.keys():
        return "started"
    if "opened" in names or names & START_EVENTS.keys():  # an attempt means they opened, even if that beacon was lost
        return "opened"
    return "invited"


def starts_count(events: list[dict]) -> int:
    return sum(1 for e in events if e["event"] in START_EVENTS)


def token_for_execution(execution_id: str) -> str | None:
    """Fallback link from a Bolna execution back to its invite, if the webhook doesn't echo user_data."""
    if not execution_id:
        return None
    for e in reversed(store.read("invite_events.jsonl")):
        if e.get("meta", {}).get("execution_id") == execution_id:
            return e["token"]
    return None


def _channel_for(events: list[dict], execution_id: str | None) -> str | None:
    # The start event that holds this execution id wins; otherwise the latest start.
    # web_connected carries the web call's id (from the SDK's getRunId()).
    for e in reversed(events):
        if execution_id and e.get("meta", {}).get("execution_id") == execution_id:
            if e["event"] in START_EVENTS:
                return START_EVENTS[e["event"]]
            if e["event"] == "web_connected":
                return "web"
    starts = [e for e in events if e["event"] in START_EVENTS]
    return START_EVENTS[starts[-1]["event"]] if starts else None


def mark_completed(token: str, execution_id: str, channel: str | None = None) -> bool:
    """Log `completed` once per invite. Returns False if it was already completed."""
    with store.locked():
        channel = channel or _channel_for(events_for(token), execution_id)
        return log_event_once(token, "completed", {"execution_id": execution_id, "channel": channel})
