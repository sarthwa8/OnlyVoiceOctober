"""results.py: the read-only joins behind the results page (build plan 03)."""

import json

import pytest
from fastapi.testclient import TestClient

from churncall import invites, results
from churncall.api import create_app
from churncall.errors import InviteNotFound
from churncall.interview import Contact


def _invite(token, name, company="acme", mrr=49.0, incentive=None, variant=None):
    return invites.Invite(token=token, company_slug=company, contact=Contact(name=name, plan="pro", tenure_days=30),
                          email=f"{token}@example.com", mrr=mrr, incentive=incentive, email_variant=variant,
                          created_at="2026-10-20T09:00:00+00:00")


def _insight(code, quote, savable=0.7):
    reason = {"code": code, "detail": f"detail for {code}", "evidence": [{"quote": quote}]}
    return {"completed": True, "primary_reason": reason, "secondary_reasons": [], "switched_to": None, "feature_gaps": [],
            "price_sensitivity": "not_mentioned", "savable_score": savable, "savable_condition": None,
            "best_quotes": [{"quote": quote + " too"}], "summary": "two sentences"}


def _transcript(eid, status="completed"):
    return {"execution_id": eid, "status": status, "duration_s": 200.0, "recording_url": f"https://rec/{eid}.mp3",
            "turns": [{"speaker": "agent", "text": "why?"}, {"speaker": "user", "text": "because"}]}


def _jsonl(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def _ev(token, event, at, **meta):
    return {"token": token, "event": event, "at": f"2026-10-20T{at}+00:00", "meta": meta}


@pytest.fixture(autouse=True)
def data(tmp_path, monkeypatch):
    monkeypatch.setenv("CHURNCALL_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("ADMIN_KEY", "test-admin")
    (tmp_path / "companies").mkdir()
    (tmp_path / "companies" / "acme.json").write_text(json.dumps(
        {"name": "Acme Inc", "product_description": "x", "founder_name": "Priya", "incentive": "a $5 voucher"}))
    (tmp_path / "companies" / "beta.json").write_text(json.dumps(
        {"name": "Beta", "product_description": "y", "founder_name": "Ravi"}))
    _jsonl(tmp_path / "invites.jsonl", [r.model_dump() for r in [
        _invite("done", "Asha Rao", mrr=100.0, variant="founder"),       # completed + insight, after a retry
        _invite("failx", "Ben", company="beta", mrr=20.0),               # completed, extraction failed
        _invite("open", "Cara"),                                          # only opened
        _invite("price", "Dev", company="beta", mrr=30.0),               # completed + insight, another reason
        _invite("price2", "Eve", mrr=50.0),                               # same reason as Dev
    ]])
    _jsonl(tmp_path / "invite_events.jsonl", [
        _ev("done", "opened", "10:00:00"),
        _ev("done", "started_phone", "10:01:00", execution_id="e1"),
        _ev("done", "call_not_connected", "10:02:00", execution_id="e1", status="no-answer"),
        _ev("done", "started_web", "10:05:00", execution_id="r2"),
        _ev("done", "completed", "10:10:00", execution_id="r2", channel="web"),
        _ev("failx", "started_phone", "11:00:00", execution_id="e3"),
        _ev("failx", "completed", "11:05:00", execution_id="e3", channel="phone"),
        _ev("open", "opened", "12:00:00"),
        _ev("price", "started_phone", "13:00:00", execution_id="e4"),
        _ev("price", "completed", "13:05:00", execution_id="e4", channel="phone"),
        _ev("price2", "started_web", "14:00:00", execution_id="r5"),
        _ev("price2", "completed", "14:05:00", execution_id="r5", channel="web"),
    ])
    _jsonl(tmp_path / "transcripts.jsonl", [_transcript(e) for e in ("r2", "e3", "e4", "r5", "stray")])
    _jsonl(tmp_path / "insights.jsonl", [
        {"execution_id": "r2", "user_talk_ratio": 0.8, "quotes_dropped": 1, "insight": _insight("onboarding_friction", "never got set up")},
        {"execution_id": "e4", "user_talk_ratio": 0.7, "quotes_dropped": 0, "insight": _insight("price_value_mismatch", "not worth it", 0.3)},
        {"execution_id": "r5", "user_talk_ratio": 0.6, "quotes_dropped": 0, "insight": _insight("price_value_mismatch", "too pricey for us", 0.9)},
    ])
    _jsonl(tmp_path / "errors.jsonl", [
        {"at": "2026-10-20T11:06:00+00:00", "step": "extraction", "execution_id": "e3", "error": "RuntimeError('no LLM')"},
        {"at": "2026-10-20T12:30:00+00:00", "token": "open", "where": "start_outbound_call", "error": "no number"},
    ])
    return tmp_path


def test_invite_row_summarises_the_completed_call():
    rows = {r.token: r for r in results.list_invites()}
    done = rows["done"]
    assert (done.name, done.company, done.status, done.channel) == ("Asha Rao", "Acme Inc", "completed", "web")
    assert (done.primary_reason, done.savable_score, done.duration_s, done.incentive) == ("onboarding_friction", 0.7, 200.0, True)
    assert rows["open"].status == "opened" and rows["open"].primary_reason is None
    assert rows["failx"].incentive is False  # beta has no incentive
    assert [r.token for r in results.list_invites()][0] == "price2"  # newest activity first


def test_detail_has_every_call_newest_first_with_transcript_insight_and_recording():
    d = results.invite_detail("done")
    assert [c.execution_id for c in d.calls] == ["r2", "e1"]
    web, missed = d.calls
    assert web.status == "completed" and web.channel == "web" and web.recording_url == "https://rec/r2.mp3"
    assert web.insight.primary_reason.code == "onboarding_friction" and web.quotes_dropped == 1 and web.user_talk_ratio == 0.8
    assert [t.speaker for t in web.turns] == ["agent", "user"]
    assert missed.status == "no-answer" and missed.channel == "phone" and missed.turns == [] and missed.insight is None
    assert [e["event"] for e in d.events][0] == "opened" and d.email == "done@example.com"


def test_failed_extraction_still_shows_transcript_and_error():
    call = results.invite_detail("failx").calls[0]
    assert call.insight is None and call.turns and call.errors[0]["step"] == "extraction"


def test_start_errors_and_unknown_invites():
    assert results.invite_detail("open").start_errors[0]["error"] == "no number"
    with pytest.raises(InviteNotFound):
        results.invite_detail("nope")


def test_unlinked_transcripts_are_listed_not_dropped():
    assert [c.execution_id for c in results.unlinked_calls()] == ["stray"]


def test_filters():
    assert {r.token for r in results.list_invites(company="beta")} == {"failx", "price"}
    assert {r.token for r in results.list_invites(status="completed")} == {"done", "failx", "price", "price2"}


def test_reasons_grouped_with_mrr_savable_and_quotes():
    groups = results.reasons()
    assert [g.code for g in groups] == ["price_value_mismatch", "onboarding_friction"]
    price = groups[0]
    assert (price.count, price.mrr, price.savable) == (2, 80.0, 1)
    assert price.quotes == ["not worth it", "not worth it too"] and set(price.tokens) == {"price", "price2"}
    assert [g.code for g in results.reasons(company="acme")] == ["onboarding_friction", "price_value_mismatch"]


def test_seed_demo_data_loads_cleanly_and_refuses_the_real_dir(tmp_path, monkeypatch, data):
    from conftest import load_script

    seed = load_script("scripts/seed_results_demo.py")
    demo = tmp_path / "demo"
    assert seed.main(["--data-dir", str(demo)]) == 0
    with pytest.raises(SystemExit):
        seed.main(["--data-dir", str(data)])  # CHURNCALL_DATA_DIR points here: the "real" dir
    monkeypatch.setenv("CHURNCALL_DATA_DIR", str(demo))
    assert len(results.list_invites()) == 12 and len(results.reasons()) == 4
    assert [c.execution_id for c in results.unlinked_calls()] == ["ex-dashboard-test"]


def test_admin_results_routes_need_the_key():
    client = TestClient(create_app())
    for path in ("/admin/reasons", "/admin/calls", "/admin/calls/done"):
        assert client.get(path).status_code == 401
        assert client.get(path, headers={"X-Admin-Key": "test-admin"}).status_code == 200
    assert client.get("/admin/calls/nope", headers={"X-Admin-Key": "test-admin"}).status_code == 404
    body = client.get("/admin/calls?status=completed", headers={"X-Admin-Key": "test-admin"}).json()
    assert len(body["invites"]) == 4 and [c["execution_id"] for c in body["unlinked"]] == ["stray"]
