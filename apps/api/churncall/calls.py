"""Starting interviews: "Call me now" (Bolna outbound) and "Talk in browser" (Bolna web session).

Each start checks the invite may start, builds Bolna's user_data on the server (never from browser
input), calls Bolna and logs the start event with Bolna's execution id so the webhook can find it later.
"""

from __future__ import annotations

import re

import httpx

from . import invites, store
from .bolna import BolnaClient
from .errors import BolnaUnavailable, ConsentRequired, InvalidPhone
from .interview import prompt_variables, render_prompt
from .invites import PHONE_RE, Invite


def build_user_data(invite: Invite, channel: str) -> dict:
    """Per-call variables for Bolna. Built on the server from the invite only, never from browser input."""
    company = invites.load_company(invite.company_slug)
    if invite.incentive:  # a per-user incentive (A/B test) overrides the company default
        company = company.model_copy(update={"incentive": invite.incentive})
    return {
        **prompt_variables(company, invite.contact, channel=channel),
        "invite_token": invite.token,
        "channel": channel,
        # Fallback in case Bolna lets user_data override the agent prompt; harmless if it doesn't [verify].
        "system_prompt": render_prompt(company, invite.contact, channel=channel),
    }


def _log_error(token: str, where: str, error: str) -> None:
    store.append("errors.jsonl", {"token": token, "at": store.now(), "where": where, "error": error})


def start_web_call(token: str) -> dict:
    """Mint a Bolna browser session for this invite. Returns Bolna's JSON unchanged (the SDK reads it).
    Tapping "Talk in browser" after the on-page disclosure is the request; the agent repeats the disclosure."""
    invite = invites.require_startable(token)
    try:
        session = BolnaClient().mint_web_session(build_user_data(invite, "web"))
    except httpx.HTTPStatusError as exc:
        _log_error(token, "mint_web_session", exc.response.text[:500])
        # Pass Bolna's status through (e.g. 429 at capacity) so the SDK reports the right error code.
        raise BolnaUnavailable("couldn't start the browser call", status=exc.response.status_code) from None
    except httpx.HTTPError as exc:
        _log_error(token, "mint_web_session", repr(exc))
        raise BolnaUnavailable("couldn't start the browser call") from None

    run_id = session.get("run_id") if isinstance(session, dict) else None  # the SDK's Session type names it run_id
    invites.log_event(token, "started_web", {"execution_id": run_id} if run_id else {})
    return session


def start_phone_call(token: str, phone_input: str | None, consent: bool) -> None:
    """User tapped "Call me now" with the consent box ticked. Their tap is the consent; refuse without it."""
    invite = invites.require_startable(token)
    if consent is not True:
        raise ConsentRequired()
    phone = re.sub(r"[\s\-().]", "", phone_input or "") or invite.phone_e164 or ""
    if not PHONE_RE.match(phone):
        raise InvalidPhone()

    try:
        result = BolnaClient().start_outbound_call(phone, user_data=build_user_data(invite, "phone"))
    except httpx.HTTPError as exc:
        _log_error(token, "start_outbound_call",
                   exc.response.text[:500] if isinstance(exc, httpx.HTTPStatusError) else repr(exc))
        raise BolnaUnavailable("couldn't start the call") from None

    invites.log_event(token, "started_phone", {"execution_id": result.get("execution_id")})
    store.append("calls.jsonl", {"token": token, "at": store.now(), "channel": "phone", "bolna": result})
