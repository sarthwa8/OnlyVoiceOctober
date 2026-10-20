import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from churncall.extraction import CallInsight, Quote, Reason, verify_quotes  # noqa: E402
from churncall.guide import Company, Contact, render_prompt  # noqa: E402
from churncall.webhook import parse_bolna_webhook  # noqa: E402

PAYLOAD = {
    "id": "exec_123",
    "status": "completed",
    "conversation_duration": 212.4,
    "telephony_data": {"recording_url": "https://example.com/rec.mp3"},
    "transcript": "assistant: Hi Alex, what made you start looking elsewhere?\n"
    "user: Honestly I never figured out how to connect my Shopify store.\n"
    "assistant: What happened when you tried?\n"
    "user: The import just spun forever, so we went with Competitor Y.",
}


def test_webhook_parses_string_transcript():
    rec = parse_bolna_webhook(PAYLOAD)
    assert rec.execution_id == "exec_123"
    assert rec.recording_url == "https://example.com/rec.mp3"
    assert [t.speaker for t in rec.turns] == ["agent", "user", "agent", "user"]
    assert 0.5 < rec.user_talk_ratio < 1


def test_webhook_parses_list_transcript():
    rec = parse_bolna_webhook({"execution_id": "e2", "transcript": [
        {"role": "agent", "content": "Hello"}, {"role": "user", "content": "Hi there"}]})
    assert rec.execution_id == "e2" and rec.turns[1].speaker == "user"


def _insight(quotes):
    return CallInsight(
        completed=True,
        primary_reason=Reason(code="onboarding_friction", detail="Shopify import failed",
                              evidence=[Quote(quote=q) for q in quotes]),
        secondary_reasons=[], switched_to="Competitor Y", feature_gaps=["shopify_import"],
        price_sensitivity="not_mentioned", savable_score=0.7, savable_condition="working import",
        best_quotes=[], summary="x",
    )


def test_verify_quotes_keeps_verbatim_and_drops_invented():
    rec = parse_bolna_webhook(PAYLOAD)
    insight, dropped = verify_quotes(
        _insight([
            "never figured out how to connect my Shopify store",  # verbatim (case/punct-insensitive)
            "The import just spun forever, so we went with Competitor Y",
            "the product was too expensive",  # invented
            "what made you start looking elsewhere",  # agent's words, not the user's
        ]),
        rec,
    )
    assert dropped == 2
    assert len(insight.primary_reason.evidence) == 2


def test_render_prompt_fills_placeholders_and_rules():
    prompt = render_prompt(
        Company(name="Shoplytics", product_description="analytics", founder_name="Priya"),
        Contact(name="Alex", trigger="trial_ended"),
    )
    assert "{{" not in prompt and "}}" not in prompt
    assert "Priya" in prompt and "finished a trial" in prompt
    assert "Do not make any offers" in prompt


def test_openai_compat_extraction_retries_on_bad_json(monkeypatch):
    import json as _json

    from churncall import llm
    from churncall.extraction import extract_insight

    monkeypatch.setenv("LLM_PROVIDER", "openai_compat")
    monkeypatch.setenv("LLM_BASE_URL", "http://fake")
    monkeypatch.setenv("LLM_MODEL", "free-model")
    good = _insight(["never figured out how to connect my Shopify store"]).model_dump_json()
    replies = iter(["Sure! here you go: not json", "```json\n" + good + "\n```"])
    calls = []

    class Resp:
        def __init__(self, text):
            self.text = text

        def raise_for_status(self):
            pass

        def json(self):
            return {"choices": [{"message": {"content": self.text}}]}

    def fake_post(url, json=None, headers=None, timeout=None):
        calls.append(json)
        return Resp(next(replies))

    monkeypatch.setattr(llm.httpx, "post", fake_post)
    insight, dropped = extract_insight(parse_bolna_webhook(PAYLOAD), "ctx")
    assert len(calls) == 2 and calls[0]["response_format"] == {"type": "json_object"}
    assert insight.primary_reason.code == "onboarding_friction" and dropped == 0
    _ = _json  # silence linters


def test_openai_compat_requires_model(monkeypatch):
    import pytest

    from churncall import llm

    monkeypatch.setenv("LLM_PROVIDER", "openai_compat")
    monkeypatch.delenv("LLM_MODEL", raising=False)
    with pytest.raises(RuntimeError):
        llm.model_for("smart")


def test_prompt_template_variables_all_have_values():
    from churncall.guide import PROMPT_PATH, prompt_variables
    import re

    used = set(re.findall(r"\{\{(\w+)\}\}", PROMPT_PATH.read_text()))
    have = prompt_variables(Company(name="A", product_description="b", founder_name="C"), Contact(name="D"))
    assert used <= have.keys(), used - have.keys()


def test_opening_line_differs_by_channel_and_always_discloses_ai():
    from churncall.guide import opening_line

    c, k = Company(name="Shoplytics", product_description="x", founder_name="Priya"), Contact(name="Alex")
    phone, web = opening_line(c, k, "phone"), opening_line(c, k, "web")
    assert "calling on behalf of" in phone and "calling on behalf of" not in web
    for line in (phone, web):
        assert "AI assistant" in line and "recorded" in line


def test_webhook_skips_non_completed_and_repeats(tmp_path, monkeypatch):
    import churncall.main as m

    monkeypatch.setattr(m, "DATA_DIR", tmp_path)
    seen = []
    monkeypatch.setattr(m, "extract_insight", lambda rec, company_context: (seen.append(rec.execution_id) or _insight(["x"]), 0))
    m._process({**PAYLOAD, "status": "call-disconnected"})
    assert not (tmp_path / "transcripts.jsonl").exists() and seen == []
    m._process(PAYLOAD)
    m._process(PAYLOAD)  # Bolna can resend; must not extract twice
    assert seen == ["exec_123"]
    assert len((tmp_path / "transcripts.jsonl").read_text().splitlines()) == 1


def test_guardrails_bypass_sent_on_user_requested_calls(monkeypatch):
    from churncall import bolna

    sent = {}

    class R:
        def raise_for_status(self):
            pass

        def json(self):
            return {"execution_id": "e1"}

    monkeypatch.setattr(bolna.httpx, "post", lambda url, json=None, headers=None, timeout=None: sent.update(json) or R())
    bolna.BolnaClient(api_key="k", agent_id="a").start_outbound_call("+911234567890", {"x": "y"})
    assert sent["bypass_call_guardrails"] is True and sent["user_data"] == {"x": "y"}


def test_invite_user_data_uses_channel_specific_opener():
    """Browser calls must not say 'calling on behalf of' (build_user_data passes the channel through)."""
    from churncall import invites
    from churncall.guide import Company, Contact

    company = Company(name="Shoplytics", product_description="x", founder_name="Priya")
    inv = type("Inv", (), {"company_slug": "x", "incentive": None, "contact": Contact(name="Alex"), "token": "t"})()
    orig = invites.load_company
    invites.load_company = lambda slug: company
    try:
        web, phone = invites.build_user_data(inv, "web"), invites.build_user_data(inv, "phone")
    finally:
        invites.load_company = orig
    assert "calling on behalf of" not in web["opening_line"] and "calling on behalf of" in phone["opening_line"]
    assert web["channel"] == "web" and web["invite_token"] == "t"
