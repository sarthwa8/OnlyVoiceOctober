import json
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(ROOT / "scripts"))

from churncall import invites  # noqa: E402

ASHA = {"name": "Asha Rao", "email": "asha@example.com", "phone_e164": "+919800000123", "plan": "pro",
        "mrr": "49", "trigger": "cancelled", "tenure_days": "140", "incentive": "$5 voucher", "email_variant": "founder"}
BEN = {"name": "Ben", "email": "ben@example.com", "trigger": "trial_ended", "email_variant": "generic"}


@pytest.fixture(autouse=True)
def data_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("CHURNCALL_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("ADMIN_KEY", "test-admin")
    (tmp_path / "companies").mkdir()
    (tmp_path / "companies" / "acme.json").write_text(json.dumps(
        {"name": "Acme", "product_description": "invoicing for freelancers", "founder_name": "Priya"}))
    return tmp_path


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(invites.router)
    return TestClient(app)


def test_create_invite_validates_and_stores():
    inv = invites.create_invite("acme", ASHA)
    assert inv.contact.name == "Asha Rao" and inv.contact.tenure_days == 140 and inv.mrr == 49.0
    assert invites.get_invite(inv.token) == inv
    for bad, msg in [({**BEN, "email": "nope"}, "bad email"), ({**BEN, "phone_e164": "98000"}, "bad phone"),
                     ({**BEN, "trigger": "angry"}, "unknown trigger"), ({**BEN, "name": ""}, "missing name")]:
        with pytest.raises(ValueError, match=msg):
            invites.create_invite("acme", bad)


def test_make_invites_script_writes_links(data_dir, tmp_path_factory, capsys):
    import make_invites

    csv_path = tmp_path_factory.mktemp("in") / "acme.csv"
    csv_path.write_text("name,email,phone_e164,email_variant\nAsha,asha@example.com,+919800000123,founder\n"
                        "Ben,not-an-email,,generic\nCara,cara@example.com,,generic\n")
    assert make_invites.main(["--company", "acme", "--csv", str(csv_path), "--base-url", "https://x.test/"]) == 0
    links = (data_dir / "links" / "acme.csv").read_text().splitlines()
    assert links[0] == "name,email,link,email_variant" and len(links) == 3
    tokens = [line.split(",")[2].rsplit("/", 1)[1] for line in links[1:]]
    assert len(set(tokens)) == 2 and all(invites.get_invite(t) for t in tokens)
    assert "row 3: bad email" in capsys.readouterr().out


def test_public_view_hides_email_and_masks_phone(client):
    inv = invites.create_invite("acme", ASHA)
    body = client.get(f"/invites/{inv.token}").json()
    assert body == {"first_name": "Asha", "company_name": "Acme", "founder_name": "Priya", "trigger_short": "cancelled",
                    "incentive": "$5 voucher", "phone_hint": "+91 •••••••123", "status": "invited"}
    assert "asha@example.com" not in json.dumps(body)
    assert client.get("/invites/not-a-token").status_code == 404


def test_opened_is_deduped_and_unknown_events_rejected(client):
    inv = invites.create_invite("acme", ASHA)
    for _ in range(2):
        assert client.post(f"/invites/{inv.token}/event", json={"event": "opened"}).status_code == 200
    assert [e["event"] for e in invites.events_for(inv.token)] == ["opened"]
    assert client.post(f"/invites/{inv.token}/event", json={"event": "completed"}).status_code == 422
    assert client.get(f"/invites/{inv.token}").json()["status"] == "opened"


def test_optout_is_idempotent_and_wins(client):
    inv = invites.create_invite("acme", ASHA)
    client.post(f"/invites/{inv.token}/optout")
    client.post(f"/invites/{inv.token}/optout")
    assert [e["event"] for e in invites.events_for(inv.token)] == ["opted_out"]
    assert client.get(f"/invites/{inv.token}").json()["status"] == "opted_out"


def test_mark_completed_once_with_channel_from_execution_id():
    inv = invites.create_invite("acme", ASHA)
    invites.log_event(inv.token, "started_phone", {"execution_id": "exec_1"})
    assert invites.token_for_execution("exec_1") == inv.token
    assert invites.mark_completed(inv.token, "exec_1") is True
    assert invites.mark_completed(inv.token, "exec_1") is False
    done = [e for e in invites.events_for(inv.token) if e["event"] == "completed"]
    assert len(done) == 1 and done[0]["meta"]["channel"] == "phone"


def test_web_channel_found_via_web_connected():
    inv = invites.create_invite("acme", BEN)
    invites.log_event(inv.token, "started_web")
    invites.log_event(inv.token, "web_connected", {"execution_id": "run_9"})
    assert invites.token_for_execution("run_9") == inv.token
    invites.mark_completed(inv.token, "run_9")
    assert invites.events_for(inv.token)[-1]["meta"]["channel"] == "web"


def test_funnel_counts_unique_users_and_splits(client):
    asha, ben, cara = (invites.create_invite("acme", r) for r in (ASHA, BEN, {**BEN, "email": "c@example.com"}))
    for token in (asha.token, ben.token):
        client.post(f"/invites/{token}/event", json={"event": "opened"})
    invites.log_event(asha.token, "started_phone", {"execution_id": "e1"})
    invites.log_event(asha.token, "started_phone", {"execution_id": "e2"})  # pressed twice: still one person
    invites.mark_completed(asha.token, "e2")
    invites.log_event(cara.token, "opted_out")

    assert client.get("/invites/funnel").status_code == 401
    assert client.get("/invites/funnel?key=wrong").status_code == 401
    f = client.get("/invites/funnel?key=test-admin").json()
    assert f["overall"] == {"invited": 3, "opened": 2, "started": 1, "completed": 1, "opted_out": 1,
                            "started_by_channel": {"phone": 1}, "completed_by_channel": {"phone": 1}}
    assert f["by_incentive"]["yes"]["completed"] == 1 and f["by_incentive"]["none"]["invited"] == 2
    assert f["by_email_variant"]["generic"]["invited"] == 2
    assert f["by_company"]["acme"]["invited"] == 3


def test_main_app_mounts_invite_routes(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)  # main.py creates its data dir relative to the working directory
    from churncall.main import app

    paths = set(app.openapi()["paths"])
    assert {"/invites/funnel", "/invites/{token}", "/invites/{token}/event", "/invites/{token}/optout"} <= paths
