"""Invite links for churned users: storage, funnel, and the /invites routes.

Each churned user gets a private token. Everything that happens to an invite is an append-only
event, and status and funnel numbers are worked out from those events. Storage is JSONL under
CHURNCALL_DATA_DIR for the kill test; it moves to Supabase after a go.
See build-plans/01-invite-page.md.
"""

from __future__ import annotations

import hmac
import json
import os
import re
import secrets
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .bolna import BolnaClient
from .guide import TRIGGERS, Company, Contact, prompt_variables, render_prompt
from .webhook import CallRecord

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+[1-9]\d{7,14}$")
START_EVENTS = {"started_web": "web", "started_phone": "phone"}
MAX_STARTS = 3
MIN_USER_TURNS = 3  # a "completed" call only counts if the user actually talked
# Bolna statuses that mean the call ended without a conversation.
NOT_CONNECTED = {"no-answer", "busy", "failed", "canceled", "stopped", "error", "balance-low"}


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


# ---------- storage ----------

def _data_dir() -> Path:
    # Read on every call so tests (and scripts) can point it somewhere else.
    path = Path(os.environ.get("CHURNCALL_DATA_DIR", "data"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def _read(name: str) -> list[dict]:
    path = _data_dir() / name
    if not path.exists():
        return []
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def _append(name: str, row: dict) -> None:
    with (_data_dir() / name).open("a") as f:
        f.write(json.dumps(row) + "\n")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_company(slug: str) -> Company:
    path = _data_dir() / "companies" / f"{slug}.json"
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
        created_at=_now(),
    )
    _append("invites.jsonl", invite.model_dump())
    return invite


def all_invites() -> list[Invite]:
    return [Invite.model_validate(r) for r in _read("invites.jsonl")]


def get_invite(token: str) -> Invite | None:
    return next((i for i in reversed(all_invites()) if i.token == token), None)


def log_event(token: str, event: str, meta: dict | None = None) -> None:
    _append("invite_events.jsonl", {"token": token, "event": event, "at": _now(), "meta": meta or {}})


def events_by_token() -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for e in _read("invite_events.jsonl"):
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


def token_for_execution(execution_id: str) -> str | None:
    """Fallback link from a Bolna execution back to its invite, if the webhook doesn't echo user_data."""
    if not execution_id:
        return None
    for e in reversed(_read("invite_events.jsonl")):
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
    events = events_for(token)
    if any(e["event"] == "completed" for e in events):
        return False
    log_event(token, "completed", {"execution_id": execution_id, "channel": channel or _channel_for(events, execution_id)})
    return True


def _call_variables(payload: dict) -> dict:
    """The user_data we sent, as echoed in the webhook. Its exact place isn't confirmed, so check both."""
    ctx = payload.get("context_details") or payload.get("user_data") or {}
    if not isinstance(ctx, dict):
        return {}
    nested = ctx.get("recipient_data")
    return {**(nested if isinstance(nested, dict) else {}), **ctx}


def record_call_outcome(payload: dict, record: CallRecord) -> str | None:
    """Update the invite funnel from one Bolna webhook. Bolna posts on every status change, so this
    ignores in-between statuses and is safe to run more than once for the same call."""
    vars_ = _call_variables(payload)
    token = vars_.get("invite_token") or token_for_execution(record.execution_id)
    if not token or get_invite(token) is None:
        return None
    status = record.status.lower()
    if status == "completed":
        user_turns = sum(1 for t in record.turns if t.speaker == "user")
        if user_turns >= MIN_USER_TURNS:
            mark_completed(token, record.execution_id, channel=vars_.get("channel"))
        else:
            _log_once(token, "call_too_short", record.execution_id, {"user_turns": user_turns})
    elif status in NOT_CONNECTED:
        _log_once(token, "call_not_connected", record.execution_id, {"status": status})
    return token


def _log_once(token: str, event: str, execution_id: str, meta: dict) -> None:
    if any(e["event"] == event and e.get("meta", {}).get("execution_id") == execution_id for e in events_for(token)):
        return
    log_event(token, event, {"execution_id": execution_id, **meta})


def build_user_data(invite: Invite, channel: str) -> dict:
    """Per-call variables for Bolna. Built on the server from the invite only, never from browser input."""
    company = load_company(invite.company_slug)
    if invite.incentive:  # a per-user incentive (A/B test) overrides the company default
        company = company.model_copy(update={"incentive": invite.incentive})
    return {
        **prompt_variables(company, invite.contact),
        "invite_token": invite.token,
        "channel": channel,
        # Fallback in case Bolna lets user_data override the agent prompt; harmless if it doesn't [verify].
        "system_prompt": render_prompt(company, invite.contact),
    }


# ---------- funnel ----------

STAGES = ["invited", "opened", "started", "completed", "opted_out"]


def _stages_reached(events: list[dict]) -> set[str]:
    names = {e["event"] for e in events}
    reached = {"invited"}
    if names & {"opened", "web_connected", "mic_denied", "call_ended_client"} or names & START_EVENTS.keys():
        reached.add("opened")  # anyone who started must have opened, even if the beacon was lost
    if names & START_EVENTS.keys():
        reached.add("started")
    if "completed" in names:
        reached |= {"opened", "started", "completed"}
    if "opted_out" in names:
        reached.add("opted_out")
    return reached


def _summarise(rows: list[tuple[Invite, list[dict]]]) -> dict:
    counts = Counter()
    started_by, completed_by = Counter(), Counter()
    for _, events in rows:
        reached = _stages_reached(events)
        counts.update(reached)
        for channel in {START_EVENTS[e["event"]] for e in events if e["event"] in START_EVENTS}:
            started_by[channel] += 1
        done = next((e for e in events if e["event"] == "completed"), None)
        if done:
            completed_by[done["meta"].get("channel") or "unknown"] += 1
    out = {stage: counts[stage] for stage in STAGES}
    out["started_by_channel"] = dict(started_by)
    out["completed_by_channel"] = dict(completed_by)
    return out


def funnel() -> dict:
    """Unique users per stage, overall and split the ways the Oct 21 go/no-go needs."""
    events = events_by_token()
    incentive_default: dict[str, bool] = {}
    rows = []
    for invite in all_invites():
        rows.append((invite, events.get(invite.token, [])))
        if invite.company_slug not in incentive_default:
            try:
                incentive_default[invite.company_slug] = bool(load_company(invite.company_slug).incentive)
            except FileNotFoundError:
                incentive_default[invite.company_slug] = False

    def group(key) -> dict:
        buckets: dict[str, list] = {}
        for row in rows:
            buckets.setdefault(key(row[0]), []).append(row)
        return {k: _summarise(v) for k, v in sorted(buckets.items())}

    return {
        "overall": _summarise(rows),
        "by_company": group(lambda i: i.company_slug),
        "by_incentive": group(lambda i: "yes" if (i.incentive or incentive_default[i.company_slug]) else "none"),
        "by_email_variant": group(lambda i: i.email_variant or "unknown"),
    }


# ---------- routes ----------

router = APIRouter(prefix="/invites", tags=["invites"])


def _mask_phone(phone: str | None) -> str | None:
    if not phone:
        return None
    return f"{phone[:3]} {'•' * (len(phone) - 6)}{phone[-3:]}"


class PublicInvite(BaseModel):
    """What the invite page is allowed to see. Never the email or the full phone number."""

    first_name: str
    company_name: str
    founder_name: str
    trigger_short: str
    incentive: str | None
    phone_hint: str | None
    status: str


class CallIn(BaseModel):
    phone_e164: str | None = None
    consent: bool = False


class EventIn(BaseModel):
    event: Literal["opened", "web_connected", "mic_denied", "call_ended_client"]
    meta: dict = {}


def _require(token: str) -> Invite:
    invite = get_invite(token)
    if invite is None:
        raise HTTPException(status_code=404, detail="unknown invite")
    return invite


def _require_startable(token: str) -> Invite:
    """An invite can start at most MAX_STARTS calls, and none once completed or opted out."""
    invite = _require(token)
    events = events_for(token)
    if status_of(events) in ("completed", "opted_out"):
        raise HTTPException(status_code=409, detail="this invite is already finished")
    if starts_count(events) >= MAX_STARTS:
        raise HTTPException(status_code=429, detail="too many attempts for this invite")
    return invite


# Declared before the /{token} routes so "funnel" is never read as a token.
@router.get("/funnel")
def get_funnel(key: str = "") -> dict:
    expected = os.environ.get("ADMIN_KEY", "")
    if not expected or not hmac.compare_digest(key, expected):
        raise HTTPException(status_code=401, detail="bad admin key")
    return funnel()


@router.get("/{token}", response_model=PublicInvite)
def get_public_invite(token: str) -> PublicInvite:
    invite = _require(token)
    company = load_company(invite.company_slug)
    return PublicInvite(
        first_name=invite.contact.name.split()[0],
        company_name=company.name,
        founder_name=company.founder_name,
        trigger_short=TRIGGERS.get(invite.contact.trigger, TRIGGERS["cancelled"])[1],
        incentive=invite.incentive or company.incentive,
        phone_hint=_mask_phone(invite.phone_e164),
        status=status_of(events_for(token)),
    )


@router.post("/{token}/event")
def post_event(token: str, body: EventIn) -> dict:
    _require(token)
    if body.event == "opened" and any(e["event"] == "opened" for e in events_for(token)):
        return {"ok": True, "duplicate": True}
    log_event(token, body.event, body.meta)
    return {"ok": True}


@router.post("/{token}/optout")
def post_optout(token: str) -> dict:
    _require(token)
    if status_of(events_for(token)) != "opted_out":
        log_event(token, "opted_out")
    return {"ok": True}


@router.post("/{token}/web-session")
def post_web_session(token: str) -> dict:
    """The Web Call SDK posts here when the user taps "Talk in browser". Any body it sends is ignored:
    user_data comes from the invite, so nobody can change the prompt or pose as another invite.
    Tapping after the on-page disclosure is the request; the agent repeats the disclosure first."""
    invite = _require_startable(token)
    try:
        session = BolnaClient().mint_web_session(build_user_data(invite, "web"))
    except httpx.HTTPStatusError as exc:
        _append("errors.jsonl", {"token": token, "at": _now(), "where": "mint_web_session", "error": exc.response.text[:500]})
        # Pass Bolna's status through (e.g. 429 at capacity) so the SDK reports the right error code.
        raise HTTPException(status_code=exc.response.status_code, detail="couldn't start the browser call") from None
    except httpx.HTTPError as exc:
        _append("errors.jsonl", {"token": token, "at": _now(), "where": "mint_web_session", "error": repr(exc)})
        raise HTTPException(status_code=502, detail="couldn't start the browser call") from None

    run_id = session.get("execution_id") or session.get("run_id") if isinstance(session, dict) else None
    log_event(token, "started_web", {"execution_id": run_id} if run_id else {})
    return session  # unchanged: the SDK knows its shape


@router.post("/{token}/call")
def post_call(token: str, body: CallIn) -> dict:
    """User tapped "Call me now" with the consent box ticked. Their tap is the consent; we refuse without it."""
    invite = _require_startable(token)
    if body.consent is not True:
        raise HTTPException(status_code=400, detail="consent required: the user must request the call")
    phone = re.sub(r"[\s\-().]", "", body.phone_e164 or "") or invite.phone_e164 or ""
    if not PHONE_RE.match(phone):
        raise HTTPException(status_code=422, detail="phone number must include the country code, e.g. +919800000000")

    try:
        result = BolnaClient().start_outbound_call(phone, user_data=build_user_data(invite, "phone"))
    except httpx.HTTPError as exc:
        detail = exc.response.text[:500] if isinstance(exc, httpx.HTTPStatusError) else repr(exc)
        _append("errors.jsonl", {"token": token, "at": _now(), "where": "start_outbound_call", "error": detail})
        raise HTTPException(status_code=502, detail="couldn't start the call") from None

    execution_id = result.get("execution_id")
    log_event(token, "started_phone", {"execution_id": execution_id})
    _append("calls.jsonl", {"token": token, "at": _now(), "channel": "phone", "bolna": result})
    return {"ok": True}
