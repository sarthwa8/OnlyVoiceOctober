"""Invites for churned users: creating them, their event log, status and start limits.

Each churned user gets a private token. Everything that happens to an invite is an append-only
event, and status (and the funnel, see funnel.py) is worked out from those events.
See build-plans/01-invite-page.md.
"""

from __future__ import annotations

import re
import secrets

from pydantic import BaseModel

from . import store
from .errors import InviteFinished, InviteNotFound, TooManyAttempts
from .interview import TRIGGERS, Company, Contact

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+[1-9]\d{7,14}$")
START_EVENTS = {"started_web": "web", "started_phone": "phone"}
MAX_STARTS = 3


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

def log_event(token: str, event: str, meta: dict | None = None) -> None:
    store.append("invite_events.jsonl", {"token": token, "event": event, "at": store.now(), "meta": meta or {}})


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
    if names & START_EVENTS.keys():
        return "started"
    if "opened" in names:
        return "opened"
    return "invited"


def starts_count(events: list[dict]) -> int:
    return sum(1 for e in events if e["event"] in START_EVENTS)


def record_opened(token: str) -> bool:
    """Log `opened` once per invite. Returns False if it was already logged."""
    with store.locked():
        if any(e["event"] == "opened" for e in events_for(token)):
            return False
        log_event(token, "opened")
        return True


def opt_out(token: str) -> None:
    with store.locked():
        if status_of(events_for(token)) != "opted_out":
            log_event(token, "opted_out")


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
        events = events_for(token)
        if any(e["event"] == "completed" for e in events):
            return False
        log_event(token, "completed", {"execution_id": execution_id, "channel": channel or _channel_for(events, execution_id)})
        return True


def log_once_per_call(token: str, event: str, execution_id: str, meta: dict) -> None:
    """Log `event` once per (invite, Bolna execution), since Bolna can resend the same webhook."""
    with store.locked():
        if any(e["event"] == event and e.get("meta", {}).get("execution_id") == execution_id for e in events_for(token)):
            return
        log_event(token, event, {"execution_id": execution_id, **meta})
