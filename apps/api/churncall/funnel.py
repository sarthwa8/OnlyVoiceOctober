"""Funnel numbers for the go/no-go: unique users per stage, split by company, channel, incentive and
email variant. Worked out from the invite event log; nothing here writes."""

from __future__ import annotations

from collections import Counter

from .invites import START_EVENTS, Invite, all_invites, events_by_token, load_company

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
        counts.update(_stages_reached(events))
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
