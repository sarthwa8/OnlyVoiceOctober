"""Characterization tests for build plan 02 (API architecture cleanup).

They pin down today's behaviour so the refactor can move code without changing what it does.
A snapshot may only change in a phase that lists the change in build-plans/02 §6.
Regenerate (deliberately) with:  UPDATE_SNAPSHOTS=1 pytest apps/api/tests/test_characterization.py
"""

import json
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from churncall import invites, store
from churncall.interview import Contact

SNAPSHOTS = Path(__file__).parent / "snapshots"
COMPANY = {"name": "Acme", "product_description": "invoicing for freelancers", "founder_name": "Priya",
           "incentive": "a $5 voucher"}


def _invite(token, name, *, phone=None, incentive=None, variant=None, trigger="cancelled", company="acme"):
    return invites.Invite(token=token, company_slug=company, contact=Contact(name=name, trigger=trigger, plan="pro",
                          tenure_days=140), email=f"{token}@example.com", phone_e164=phone, mrr=49.0,
                          incentive=incentive, email_variant=variant, created_at="2026-10-20T10:00:00+00:00")


def _check(name: str, actual) -> None:
    path = SNAPSHOTS / name
    text = json.dumps(actual, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if os.environ.get("UPDATE_SNAPSHOTS") == "1" or not path.exists():
        path.write_text(text)
    assert json.loads(path.read_text()) == json.loads(text), f"{name} changed: behaviour moved during the refactor"


@pytest.fixture(autouse=True)
def data_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("CHURNCALL_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("ADMIN_KEY", "test-admin")
    for slug, extra in (("acme", {}), ("beta", {"incentive": None, "name": "Beta"})):
        (tmp_path / "companies").mkdir(exist_ok=True)
        (tmp_path / "companies" / f"{slug}.json").write_text(json.dumps({**COMPANY, **extra}))
    return tmp_path


def _write_invites(data_dir, rows):
    (data_dir / "invites.jsonl").write_text("".join(json.dumps(r.model_dump()) + "\n" for r in rows))


def _write_events(data_dir, events):
    (data_dir / "invite_events.jsonl").write_text(
        "".join(json.dumps({"token": t, "event": e, "at": "2026-10-20T10:00:00+00:00", "meta": m}) + "\n"
                for t, e, m in events))


# 1. What Bolna receives for a call.
@pytest.mark.parametrize("channel", ["phone", "web"])
def test_user_data_snapshot(data_dir, channel):
    inv = _invite("tok_asha", "Asha Rao", phone="+919800000123", incentive="$5 voucher")
    from churncall import calls

    _check(f"user_data_{channel}.json", calls.build_user_data(inv, channel))


# 2. The funnel numbers for a fixed history covering every event type.
def test_funnel_snapshot(data_dir):
    _write_invites(data_dir, [
        _invite("a", "Asha", incentive="$5 voucher", variant="founder"),
        _invite("b", "Ben", variant="generic"),
        _invite("c", "Cara", variant="generic", company="beta"),
        _invite("d", "Dev", variant="founder", company="beta"),
        _invite("e", "Eve"),
    ])
    _write_events(data_dir, [
        ("a", "opened", {}), ("a", "started_phone", {"execution_id": "e1"}), ("a", "started_phone", {"execution_id": "e2"}),
        ("a", "completed", {"execution_id": "e2", "channel": "phone"}),
        ("b", "opened", {}), ("b", "started_web", {"execution_id": "r1"}), ("b", "web_connected", {"execution_id": "r1"}),
        ("b", "call_ended_client", {"reason": "remote-hangup"}), ("b", "completed", {"execution_id": "r1", "channel": "web"}),
        ("c", "opened", {}), ("c", "mic_denied", {}), ("c", "started_phone", {"execution_id": "e3"}),
        ("c", "call_not_connected", {"execution_id": "e3", "status": "no-answer"}),
        ("d", "started_web", {}), ("d", "call_too_short", {"execution_id": "r2", "user_turns": 1}),
        ("e", "opened", {}), ("e", "opted_out", {}),
    ])
    from churncall.funnel import funnel

    _check("funnel.json", funnel())


# 3. A realistic stream of Bolna webhooks for three invites.
def _webhook(execution_id, status, user_lines=3, token=None, channel=None):
    lines = []
    for i in range(user_lines):
        lines += [f"assistant: question {i}?", f"user: answer number {i} with some detail"]
    payload = {"id": execution_id, "status": status, "transcript": "\n".join(lines)}
    if token:
        payload["context_details"] = {"invite_token": token, **({"channel": channel} if channel else {})}
    return payload


def test_webhook_replay(data_dir, monkeypatch):
    from churncall import webhooks

    monkeypatch.setattr(webhooks, "extract_insight", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("no LLM in tests")))
    _write_invites(data_dir, [_invite("a", "Asha"), _invite("b", "Ben"), _invite("c", "Cara")])
    _write_events(data_dir, [("b", "started_phone", {"execution_id": "e9"})])

    for status in ("queued", "ringing", "in-progress", "call-disconnected", "completed", "completed"):
        webhooks.handle_bolna_webhook(_webhook("e1", status, token="a", channel="phone"))
    webhooks.handle_bolna_webhook(_webhook("e9", "no-answer", user_lines=0))  # no user_data: found via execution id
    webhooks.handle_bolna_webhook(_webhook("e3", "completed", user_lines=1, token="c"))

    events = [(e["token"], e["event"], e["meta"]) for e in store.read("invite_events.jsonl")]
    transcripts = [(r["execution_id"], r["status"]) for r in store.read("transcripts.jsonl")]
    errors = [r["execution_id"] for r in store.read("errors.jsonl")]
    _check("webhook_replay.json", {"events": events, "transcripts": transcripts, "extraction_errors": errors})


# 4. Status codes the invite page depends on (InviteClient.tsx stateForCallResponse etc.).
class _FakeBolna:
    def start_outbound_call(self, phone_e164, user_data, timeout=15.0):
        return {"status": "queued", "execution_id": "exec_x"}

    def mint_web_session(self, user_data, timeout=15.0):
        return {"run_id": "run_x", "expires_in": 120}


def test_route_contract(data_dir, monkeypatch):
    from churncall import calls, main

    monkeypatch.setattr(calls, "BolnaClient", _FakeBolna)
    _write_invites(data_dir, [_invite("live", "Asha", phone="+919800000123"), _invite("done", "Ben"),
                              _invite("busy", "Cara", phone="+14155550100")])
    _write_events(data_dir, [("done", "opted_out", {})] + [("busy", "started_phone", {})] * 3)
    c = TestClient(main.app)
    codes = {
        "public_view_ok": c.get("/invites/live").status_code,
        "public_view_unknown": c.get("/invites/nope").status_code,
        "event_ok": c.post("/invites/live/event", json={"event": "opened"}).status_code,
        "event_bad_name": c.post("/invites/live/event", json={"event": "completed"}).status_code,
        "call_no_consent": c.post("/invites/live/call", json={"consent": False}).status_code,
        "call_bad_phone": c.post("/invites/live/call", json={"consent": True, "phone_e164": "123"}).status_code,
        "call_ok": c.post("/invites/live/call", json={"consent": True}).status_code,
        "call_finished": c.post("/invites/done/call", json={"consent": True}).status_code,
        "call_too_many": c.post("/invites/busy/call", json={"consent": True}).status_code,
        "web_session_ok": c.post("/invites/live/web-session").status_code,
        "web_session_finished": c.post("/invites/done/web-session").status_code,
        "optout_ok": c.post("/invites/live/optout").status_code,
    }
    _check("route_contract.json", codes)
