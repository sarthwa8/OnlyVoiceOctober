"""Fill a SEPARATE data dir with realistic fake churn interviews, to build and demo the results page
before real interviews exist (build plan 03, Step 4).

    python scripts/seed_results_demo.py --data-dir /tmp/churncall-demo
    CHURNCALL_DATA_DIR=/tmp/churncall-demo uvicorn churncall.main:app --port 8000   # then open /results

Everything here is invented. The script refuses the real data dir (settings.data_dir) unless --force,
so fake rows never mix with real results.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from churncall.config import get_settings
from churncall.extraction import _normalise

COMPANY = {"name": "Shoplytics", "product_description": "analytics dashboards for small online stores",
           "founder_name": "Priya", "incentive": "a $5 Amazon voucher"}

# (token, name, plan, mrr, trigger, email_variant)
PEOPLE = [
    ("dm-asha", "Asha Rao", "Growth", 79, "cancelled", "founder"),
    ("dm-ben", "Ben Carter", "Starter", 29, "cancelled", "generic"),
    ("dm-cara", "Cara Lopez", "Growth", 79, "downgraded", "founder"),
    ("dm-dev", "Dev Malhotra", "Pro", 199, "cancelled", "founder"),
    ("dm-eli", "Eli Brooks", "Starter", 29, "trial_ended", "generic"),
    ("dm-fatima", "Fatima Khan", "Growth", 79, "cancelled", "generic"),
    ("dm-gopal", "Gopal Iyer", "Starter", 29, "inactive", "founder"),
    ("dm-hana", "Hana Sato", "Pro", 199, "cancelled", "generic"),
    ("dm-ivan", "Ivan Petrov", "Starter", 29, "trial_ended", "founder"),
    ("dm-jo", "Jo Adeyemi", "Growth", 79, "cancelled", "generic"),
    ("dm-kim", "Kim Nguyen", "Starter", 29, "cancelled", "founder"),
    ("dm-leo", "Leo Martin", "Growth", 79, "inactive", "generic"),
]

# Completed interviews: token -> (execution_id, channel, user lines, reason code, detail, quotes, savable, condition, switched_to, gaps, price)
INTERVIEWS = {
    "dm-asha": ("ex-asha", "web", [
        "Sure, I have a few minutes.",
        "I wanted one place to see which products were actually making money.",
        "Honestly I never got my Shopify store connected. The import kept failing at the orders step.",
        "I tried three times over two weeks, then I just went back to my spreadsheet.",
        "If the import had worked on day one I would still be paying for it.",
    ], "onboarding_friction", "The Shopify import failed at the orders step, so she never saw her data.",
        ["I never got my Shopify store connected", "If the import had worked on day one I would still be paying for it"],
        0.8, "a working Shopify import", "a spreadsheet", ["reliable shopify import"], "value_not_price"),
    "dm-dev": ("ex-dev", "phone", [
        "Yeah, go ahead.",
        "We needed weekly reports for our investors, mostly revenue by channel.",
        "The setup took forever. Our developer spent a whole afternoon on the tracking script and it still missed refunds.",
        "We moved to Lifetimely because it was plug and play.",
        "Maybe, if setup was ten minutes and refunds were right.",
    ], "onboarding_friction", "Tracking setup took a developer an afternoon and still missed refunds.",
        ["The setup took forever", "it still missed refunds"], 0.6, "ten-minute setup with correct refunds",
        "Lifetimely", ["refund tracking", "faster setup"], "value_not_price"),
    "dm-fatima": ("ex-fatima", "web", [
        "Hi, yes that's fine.",
        "I liked the dashboards, but I only opened them once a month.",
        "For one report a month it just wasn't worth seventy nine dollars.",
        "Now I export from Shopify and make a chart myself.",
        "A cheaper monthly plan would bring me back, like twenty dollars.",
    ], "price_value_mismatch", "She used it once a month, which didn't justify the Growth price.",
        ["For one report a month it just wasn't worth seventy nine dollars", "A cheaper monthly plan would bring me back"],
        0.9, "a ~$20 light plan", "Shopify exports", ["light plan"], "price_is_the_issue"),
    "dm-hana": ("ex-hana", "phone", [
        "Okay.",
        "We used it daily for inventory forecasts.",
        "Two outages during our Black Friday week. We lost a day of data each time.",
        "After that the team didn't trust the numbers anymore.",
        "Probably not, we already switched to Triple Whale.",
    ], "reliability_bugs", "Two outages during Black Friday week lost data and broke the team's trust.",
        ["Two outages during our Black Friday week", "the team didn't trust the numbers anymore"],
        0.2, None, "Triple Whale", [], "not_mentioned"),
    "dm-jo": ("ex-jo", "web", [
        "Sure.",
        "I wanted to compare my ad spend to sales in one view.",
        "It was fine but too expensive for a store my size, to be honest.",
        "When you say expensive, it's more that I didn't use half the features.",
        "If I could pay only for the ads report I'd come back.",
    ], "price_value_mismatch", "Paying for features he didn't use; wanted only the ads report.",
        ["too expensive for a store my size", "If I could pay only for the ads report I'd come back"],
        0.7, "an ads-report-only plan", None, ["ads report on its own"], "value_not_price"),
    "dm-kim": ("ex-kim", "phone", [
        "Hello, yes.",
        "I was hoping it would tell me which customers come back.",
        "There was no cohort view at all, which is the one thing I needed.",
        "I use Google Sheets with a template now.",
        "If you add cohorts, I'll try again.",
    ], "missing_feature", "No cohort / repeat-customer view, the one thing she needed.",
        ["There was no cohort view at all", "If you add cohorts, I'll try again"], 0.75, "cohort analysis",
        "Google Sheets", ["cohort view"], "not_mentioned"),
}

AGENT_LINES = [
    "Hi, thanks for joining. Is now a good time?",
    "Take me back to when you first signed up. What were you hoping it would do?",
    "When did you first start thinking about cancelling? What happened?",
    "What do you use now instead?",
    "If that were fixed, would you consider coming back?",
]


def _transcript(execution_id: str, user_lines: list[str]) -> dict:
    turns = []
    for agent, user in zip(AGENT_LINES, user_lines):
        turns += [{"speaker": "agent", "text": agent}, {"speaker": "user", "text": user}]
    return {"execution_id": execution_id, "status": "completed", "duration_s": 60.0 + 25 * len(user_lines),
            "recording_url": None, "turns": turns}


def _insight(user_lines, code, detail, quotes, savable, condition, switched_to, gaps, price) -> dict:
    said = _normalise(" ".join(user_lines))
    for q in quotes:  # the real pipeline drops unverified quotes; demo data must pass the same check
        assert _normalise(q) in said, f"demo quote not in transcript: {q!r}"
    return {"completed": True, "primary_reason": {"code": code, "detail": detail, "evidence": [{"quote": q} for q in quotes[:1]]},
            "secondary_reasons": [], "switched_to": switched_to, "feature_gaps": gaps, "price_sensitivity": price,
            "savable_score": savable, "savable_condition": condition, "best_quotes": [{"quote": q} for q in quotes[1:]],
            "summary": detail + (f" Would return for {condition}." if condition else " Unlikely to return.")}


def _at(hour: int, minute: int) -> str:
    return f"2026-10-21T{hour:02d}:{minute:02d}:00+00:00"


def seed(data_dir: Path) -> None:
    (data_dir / "companies").mkdir(parents=True, exist_ok=True)
    (data_dir / "companies" / "demo.json").write_text(json.dumps(COMPANY, indent=2))
    invites, events, transcripts, insights, errors = [], [], [], [], []

    for i, (token, name, plan, mrr, trigger, variant) in enumerate(PEOPLE):
        invites.append({"token": token, "company_slug": "demo", "email": f"{token}@example.com", "phone_e164": None,
                        "contact": {"name": name, "trigger": trigger, "plan": plan, "tenure_days": 30 + 20 * i, "usage_facts": []},
                        "mrr": float(mrr), "incentive": None, "email_variant": variant, "created_at": _at(8, i)})
        ev = lambda event, minute, **meta: events.append({"token": token, "event": event, "at": _at(9 + i // 2, minute), "meta": meta})  # noqa: E731

        if token in INTERVIEWS:
            eid, channel, lines, *rest = INTERVIEWS[token]
            ev("opened", 1)
            if channel == "web":
                ev("started_web", 2, execution_id=eid)
                ev("web_connected", 3, execution_id=eid)
                ev("call_ended_client", 8, reason="remote-hangup")
            else:
                ev("started_phone", 2, execution_id=eid)
            ev("completed", 9, execution_id=eid, channel=channel)
            transcripts.append(_transcript(eid, lines))
            insights.append({"execution_id": eid, "user_talk_ratio": 0.72, "quotes_dropped": 0, "insight": _insight(lines, *rest)})
        elif token == "dm-ben":  # completed, but extraction failed (e.g. no LLM key yet)
            ev("opened", 1)
            ev("started_phone", 2, execution_id="ex-ben")
            ev("completed", 7, execution_id="ex-ben", channel="phone")
            transcripts.append(_transcript("ex-ben", ["Yes.", "Tracking sales.", "It was slow to load.", "Nothing for now.", "Maybe."]))
            errors.append({"at": _at(9, 8), "step": "extraction", "execution_id": "ex-ben",
                           "error": "RuntimeError('Set LLM_MODEL (and LLM_BASE_URL / LLM_API_KEY) for LLM_PROVIDER=openai_compat')"})
        elif token == "dm-cara":  # mic blocked, asked for a call, didn't answer
            ev("opened", 1)
            ev("mic_denied", 2)
            ev("started_phone", 3, execution_id="ex-cara")
            ev("call_not_connected", 5, execution_id="ex-cara", status="no-answer")
        elif token == "dm-eli":  # hung up almost straight away
            ev("opened", 1)
            ev("started_web", 2, execution_id="ex-eli")
            ev("call_too_short", 3, execution_id="ex-eli", user_turns=1)
        elif token == "dm-gopal":
            ev("opened", 1)
            ev("opted_out", 2)
        elif token == "dm-ivan":
            ev("opened", 1)
        # dm-leo: invited, never opened

    transcripts.append(_transcript("ex-dashboard-test", ["Testing, one two.", "Just checking the agent.", "Okay", "Fine", "Bye"]))

    for name, rows in (("invites.jsonl", invites), ("invite_events.jsonl", events), ("transcripts.jsonl", transcripts),
                       ("insights.jsonl", insights), ("errors.jsonl", errors)):
        (data_dir / name).write_text("".join(json.dumps(r) + "\n" for r in rows))
    print(f"Seeded {len(invites)} invites, {len(transcripts)} transcripts, {len(insights)} insights into {data_dir}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-dir", required=True, type=Path, help="where to write the fake data (wiped first)")
    parser.add_argument("--force", action="store_true", help="allow writing into the real CHURNCALL_DATA_DIR")
    args = parser.parse_args(argv)

    target, real = args.data_dir.resolve(), get_settings().data_dir.resolve()
    if target == real and not args.force:
        parser.error(f"{target} is the real data dir (CHURNCALL_DATA_DIR); pass a different --data-dir")
    if target.exists():
        shutil.rmtree(target)
    seed(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
