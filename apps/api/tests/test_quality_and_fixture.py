"""Interview-quality checker (eval/interviews/quality.py) and the reconstructed browser-call webhook fixture."""

import json
from pathlib import Path

import pytest

from conftest import REPO_ROOT, load_script

FIXTURES = Path(__file__).parent / "fixtures"
quality = load_script("eval/interviews/quality.py")


def test_first_real_interview_fails_every_check_it_should():
    """The first real call (2026-10-20) is our 'before' example: these numbers match Pranav's write-up."""
    m = quality.score(quality.parse_lines((FIXTURES / "first_interview_2026-10-20.txt").read_text()))
    assert m["user_talk_ratio"] == 0.29 and m["agent_avg_words"] == 28.7 and m["agent_max_words"] == 50
    assert m["multi_question_turns"] == 2 and m["leading_questions"] == 1
    assert m["ignored_end_requests"] == 1  # asked "anything else?" after "can we end this call now"
    assert not m["passes"]


def test_good_interview_passes():
    good = """assistant: Hi Alex, thanks for joining. I'm an AI assistant helping Priya at Shoplytics. This is recorded. Is now a good time?
user: sure go ahead
assistant: What were you hoping Shoplytics would do?
user: I wanted to find winning products for my store without spending hours in spreadsheets every single week, because that was eating my whole Sunday
assistant: When did you start thinking about cancelling?
user: honestly after the second month, when the product suggestions were mostly things I already sold or things that were clearly out of season
assistant: Mostly things you already sold. Compared to what?
user: a competitor showed me trending products in my niche that I had never heard of, and two of them actually sold well in the first week, so the choice was easy
assistant: Thank you, this is genuinely useful. Anything else Priya should know?
user: no that's it
assistant: Thanks Alex, goodbye."""
    m = quality.score(quality.parse_lines(good))
    assert m["passes"], m["failures"]


@pytest.mark.parametrize("text,key", [
    ("What do you use now, and what about that works better?", "multi_question_turns"),
    ("Why? And what did you try?", "multi_question_turns"),
    ("Was it the price?", "leading_questions"),
    ("What made you feel it was too expensive for what it offered?", "leading_questions"),
])
def test_single_turn_violations(text, key):
    m = quality.score([{"speaker": "agent", "text": "opener"}, {"speaker": "user", "text": "ok"},
                       {"speaker": "agent", "text": text}])
    assert m[key] == 1


def test_reconstructed_webcall_webhook_completes_invite_and_shows_on_results(tmp_path, monkeypatch):
    from churncall import invites, results, webhooks
    from churncall.interview import Contact

    monkeypatch.setenv("CHURNCALL_DATA_DIR", str(tmp_path))
    (tmp_path / "companies").mkdir()
    (tmp_path / "companies" / "shoplytics.json").write_text(json.dumps(
        {"name": "Shoplytics", "product_description": "analytics", "founder_name": "Priya"}))
    inv = invites.Invite(token="fixturetok", company_slug="shoplytics", contact=Contact(name="Pranav"),
                         email="p@example.com", created_at="2026-10-20T15:00:00+00:00")
    (tmp_path / "invites.jsonl").write_text(inv.model_dump_json() + "\n")
    invites.log_event("fixturetok", "opened")
    invites.log_event("fixturetok", "started_web", {"execution_id": "fixture-exec-0001"})

    seen = []
    monkeypatch.setattr(webhooks, "extract_insight", lambda rec, company_context: seen.append(rec.execution_id) or (None, 0))
    payload = json.loads((FIXTURES / "bolna_completed_webcall.json").read_text())
    webhooks.handle_bolna_webhook({**payload, "status": "call-disconnected"})  # in-between status: ignored
    webhooks.handle_bolna_webhook(payload)
    webhooks.handle_bolna_webhook(payload)  # resend: no double completion or extraction

    detail = results.invite_detail("fixturetok")
    assert detail.status == "completed" and detail.channel == "web"
    assert [e["event"] for e in detail.events].count("completed") == 1
    assert seen == ["fixture-exec-0001"]
    call = next(c for c in detail.calls if c.execution_id == "fixture-exec-0001")
    assert call.turns and call.turns[0].speaker == "agent"
    assert (REPO_ROOT / "eval" / "interviews" / "quality.py").exists()
