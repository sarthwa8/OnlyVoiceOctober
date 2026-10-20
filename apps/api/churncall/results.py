"""What the results page shows: every invite with its calls, transcripts, insights and errors, plus churn
reasons grouped across calls. Read-only: joins the files that invites, calls and webhooks already write.
See build-plans/03-results-page.md.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from pydantic import BaseModel

from . import store
from .bolna import Turn
from .errors import InviteNotFound
from .extraction import CallInsight
from .invites import START_EVENTS, Invite, all_invites, events_by_token, load_company, status_of

SAVABLE_AT = 0.6  # savable_score at or above this counts as "could be won back"


class CallView(BaseModel):
    """One Bolna call."""

    execution_id: str
    channel: str | None = None
    status: str | None = None
    started_at: str | None = None
    duration_s: float | None = None
    recording_url: str | None = None
    user_talk_ratio: float | None = None
    turns: list[Turn] = []
    insight: CallInsight | None = None
    quotes_dropped: int | None = None
    errors: list[dict] = []


class InviteRow(BaseModel):
    """One line in the results table: an invite (a person), summarised by its best call."""

    token: str
    name: str
    company: str
    email_variant: str | None
    incentive: bool
    mrr: float | None
    status: str
    channel: str | None
    primary_reason: str | None
    savable_score: float | None
    duration_s: float | None
    last_event_at: str | None


class InviteDetail(InviteRow):
    email: str
    phone_e164: str | None
    trigger: str
    plan: str
    tenure_days: int | None
    events: list[dict]
    calls: list[CallView]
    start_errors: list[dict]


class ReasonGroup(BaseModel):
    code: str
    count: int
    mrr: float
    savable: int
    quotes: list[str]
    tokens: list[str]


@dataclass
class _Index:
    """Everything read once per request, keyed for joining."""

    invites: list[Invite]
    events: dict[str, list[dict]]
    transcripts: dict[str, dict] = field(default_factory=dict)
    insights: dict[str, dict] = field(default_factory=dict)
    call_errors: dict[str, list[dict]] = field(default_factory=lambda: defaultdict(list))
    start_errors: dict[str, list[dict]] = field(default_factory=lambda: defaultdict(list))
    company_names: dict[str, str] = field(default_factory=dict)
    company_incentive: dict[str, bool] = field(default_factory=dict)


def _index() -> _Index:
    idx = _Index(invites=all_invites(), events=events_by_token())
    idx.transcripts = {t["execution_id"]: t for t in store.read("transcripts.jsonl") if t.get("execution_id")}
    idx.insights = {i["execution_id"]: i for i in store.read("insights.jsonl") if i.get("execution_id")}
    for err in store.read("errors.jsonl"):
        if err.get("execution_id"):
            idx.call_errors[err["execution_id"]].append(err)
        elif err.get("token"):
            idx.start_errors[err["token"]].append(err)
    for inv in idx.invites:
        if inv.company_slug not in idx.company_names:
            try:
                company = load_company(inv.company_slug)
                idx.company_names[inv.company_slug] = company.name
                idx.company_incentive[inv.company_slug] = bool(company.incentive)
            except FileNotFoundError:
                idx.company_names[inv.company_slug] = inv.company_slug
                idx.company_incentive[inv.company_slug] = False
    return idx


def _calls_for(events: list[dict], idx: _Index) -> list[CallView]:
    """Every Bolna call mentioned in an invite's events, newest first."""
    calls: dict[str, CallView] = {}
    for e in events:
        eid = e.get("meta", {}).get("execution_id")
        if not eid:
            continue
        call = calls.setdefault(eid, CallView(execution_id=eid, started_at=e["at"]))
        if e["event"] in START_EVENTS:
            call.channel = START_EVENTS[e["event"]]
        elif e["event"] == "web_connected":
            call.channel = "web"
        elif e["event"] == "completed":
            call.channel = e["meta"].get("channel") or call.channel
            call.status = "completed"
        elif e["event"] == "call_not_connected":
            call.status = e["meta"].get("status")
        elif e["event"] == "call_too_short":
            call.status = "too_short"
    for call in calls.values():
        _fill(call, idx)
    return sorted(calls.values(), key=lambda c: c.started_at or "", reverse=True)


def _fill(call: CallView, idx: _Index) -> None:
    if transcript := idx.transcripts.get(call.execution_id):
        call.status = call.status or transcript.get("status")
        call.duration_s = transcript.get("duration_s")
        call.recording_url = transcript.get("recording_url")
        call.turns = [Turn(**t) for t in transcript.get("turns", [])]
    if row := idx.insights.get(call.execution_id):
        call.insight = CallInsight.model_validate(row["insight"])
        call.user_talk_ratio = row.get("user_talk_ratio")
        call.quotes_dropped = row.get("quotes_dropped")
    call.errors = idx.call_errors.get(call.execution_id, [])


def _best_call(calls: list[CallView]) -> CallView | None:
    """The call that represents the invite: the completed one with an insight, else completed, else latest."""
    return (
        next((c for c in calls if c.status == "completed" and c.insight), None)
        or next((c for c in calls if c.status == "completed"), None)
        or (calls[0] if calls else None)
    )


def _row(inv: Invite, idx: _Index, calls: list[CallView]) -> dict:
    events = idx.events.get(inv.token, [])
    best = _best_call(calls)
    return {
        "token": inv.token,
        "name": inv.contact.name,
        "company": idx.company_names[inv.company_slug],
        "email_variant": inv.email_variant,
        "incentive": bool(inv.incentive) or idx.company_incentive[inv.company_slug],
        "mrr": inv.mrr,
        "status": status_of(events),
        "channel": best.channel if best else None,
        "primary_reason": best.insight.primary_reason.code if best and best.insight else None,
        "savable_score": best.insight.savable_score if best and best.insight else None,
        "duration_s": best.duration_s if best else None,
        "last_event_at": events[-1]["at"] if events else inv.created_at,
    }


def _matches(inv: Invite, row: dict, company: str | None, status: str | None) -> bool:
    return (not company or inv.company_slug == company) and (not status or row["status"] == status)


def list_invites(company: str | None = None, status: str | None = None) -> list[InviteRow]:
    idx = _index()
    rows = []
    for inv in idx.invites:
        row = _row(inv, idx, _calls_for(idx.events.get(inv.token, []), idx))
        if _matches(inv, row, company, status):
            rows.append(InviteRow(**row))
    return sorted(rows, key=lambda r: r.last_event_at or "", reverse=True)


def invite_detail(token: str) -> InviteDetail:
    idx = _index()
    inv = next((i for i in reversed(idx.invites) if i.token == token), None)
    if inv is None:
        raise InviteNotFound()
    calls = _calls_for(idx.events.get(token, []), idx)
    return InviteDetail(
        **_row(inv, idx, calls),
        email=inv.email,
        phone_e164=inv.phone_e164,
        trigger=inv.contact.trigger,
        plan=inv.contact.plan,
        tenure_days=inv.contact.tenure_days,
        events=idx.events.get(token, []),
        calls=calls,
        start_errors=idx.start_errors.get(token, []),
    )


def unlinked_calls() -> list[CallView]:
    """Transcripts that belong to no invite (e.g. a test call placed from Bolna's dashboard)."""
    idx = _index()
    linked = {e.get("meta", {}).get("execution_id") for events in idx.events.values() for e in events}
    calls = []
    for eid in idx.transcripts:
        if eid not in linked:
            call = CallView(execution_id=eid)
            _fill(call, idx)
            calls.append(call)
    return calls


def reasons(company: str | None = None) -> list[ReasonGroup]:
    """Completed calls with an insight, grouped by primary reason, biggest group first."""
    idx = _index()
    groups: dict[str, ReasonGroup] = {}
    for inv in idx.invites:
        if company and inv.company_slug != company:
            continue
        best = _best_call(_calls_for(idx.events.get(inv.token, []), idx))
        if not best or best.status != "completed" or not best.insight:
            continue
        insight = best.insight
        group = groups.setdefault(insight.primary_reason.code,
                                  ReasonGroup(code=insight.primary_reason.code, count=0, mrr=0.0, savable=0, quotes=[], tokens=[]))
        group.count += 1
        group.mrr += inv.mrr or 0.0
        group.savable += insight.savable_score >= SAVABLE_AT
        group.tokens.append(inv.token)
        for q in [*insight.primary_reason.evidence, *insight.best_quotes]:
            if len(group.quotes) < 2 and q.quote not in group.quotes:
                group.quotes.append(q.quote)
    return sorted(groups.values(), key=lambda g: (g.count, g.mrr), reverse=True)
