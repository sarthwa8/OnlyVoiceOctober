"""Routes the invite page calls (through Next.js at /api/invites/*). Thin: parse, call one use case, return."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from .. import calls, invites
from ..interview import trigger_phrases

router = APIRouter(prefix="/invites", tags=["invites"])


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


def _mask_phone(phone: str | None) -> str | None:
    if not phone:
        return None
    return f"{phone[:3]} {'•' * (len(phone) - 6)}{phone[-3:]}"


@router.get("/{token}", response_model=PublicInvite)
def get_public_invite(token: str) -> PublicInvite:
    invite = invites.require_invite(token)
    company = invites.load_company(invite.company_slug)
    return PublicInvite(
        first_name=invite.contact.name.split()[0],
        company_name=company.name,
        founder_name=company.founder_name,
        trigger_short=trigger_phrases(invite.contact.trigger)[1],
        incentive=invite.incentive or company.incentive,
        phone_hint=_mask_phone(invite.phone_e164),
        status=invites.status_of(invites.events_for(token)),
    )


@router.post("/{token}/event")
def post_event(token: str, body: EventIn) -> dict:
    invites.require_invite(token)
    if body.event == "opened":  # counted once per invite, however often the page loads
        return {"ok": True} if invites.log_event_once(token, "opened") else {"ok": True, "duplicate": True}
    invites.log_event(token, body.event, body.meta)
    return {"ok": True}


@router.post("/{token}/optout")
def post_optout(token: str) -> dict:
    invites.require_invite(token)
    invites.log_event_once(token, "opted_out")
    return {"ok": True}


@router.post("/{token}/web-session")
def post_web_session(token: str) -> dict:
    """The Web Call SDK posts here when the user taps "Talk in browser". Any body it sends is ignored:
    user_data comes from the invite, so nobody can change the prompt or pose as another invite."""
    return calls.start_web_call(token)


@router.post("/{token}/call")
def post_call(token: str, body: CallIn) -> dict:
    calls.start_phone_call(token, body.phone_e164, body.consent)
    return {"ok": True}
