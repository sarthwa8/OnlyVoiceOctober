"""Text-only interview simulator: our interviewer prompt vs LLM-played churned-user personas.

Run:  python eval/interviews/simulate.py --persona terse --turns 10
Writes transcripts to eval/interviews/runs/ and prints simple checks (user talk ratio,
leading-question count, questions-per-turn). Costs real API money; keep runs small.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "api"))
from churncall.guide import Company, Contact, render_prompt  # noqa: E402

INTERVIEWER_MODEL = "claude-opus-5-5"
PERSONA_MODEL = "claude-haiku-5-5"

PERSONAS = {
    "terse": "You answer in a few words. You're busy and mildly annoyed but polite.",
    "rambler": "You talk a lot and drift off topic, but the real reason comes out if someone asks good follow-ups.",
    "price_cover": "You say 'too expensive' first. The real reason is you never got the Shopify import working.",
    "angry": "You're frustrated: two outages lost you sales. You calm down if someone listens.",
    "vague": "You say 'it just wasn't for us' and need gentle reframing before you get specific.",
    "hinglish": "You speak Hinglish (Hindi-English mix). You left because the reports were too slow to load.",
}

COMPANY = Company(
    name="Shoplytics",
    product_description="analytics dashboards for small online stores",
    founder_name="Priya",
    incentive="a $5 Amazon voucher",
)
CONTACT = Contact(name="Alex", plan="Growth", tenure_days=94, usage_facts=["opened reports 3 times last month"])

LEADING = re.compile(r"\b(was it|is it because|did you leave because|was the (price|cost))\b", re.I)


def run(persona: str, turns: int) -> dict:
    client = anthropic.Anthropic()
    interviewer_system = render_prompt(COMPANY, CONTACT)
    persona_system = (
        f"You are {CONTACT.name}, who recently cancelled {COMPANY.name}. {PERSONAS[persona]} "
        "You are on a phone call with an AI interviewer. Reply with only what you'd say out loud, 1-3 sentences."
    )
    interviewer_msgs: list[dict] = [{"role": "user", "content": "(The call has connected. Begin.)"}]
    persona_msgs: list[dict] = []
    log = []
    for _ in range(turns):
        a = client.messages.create(model=INTERVIEWER_MODEL, max_tokens=400, output_config={"effort": "low"},
                                   system=interviewer_system, messages=interviewer_msgs)
        agent_text = "".join(b.text for b in a.content if b.type == "text").strip()
        log.append({"speaker": "agent", "text": agent_text})
        interviewer_msgs.append({"role": "assistant", "content": a.content})
        persona_msgs.append({"role": "user", "content": agent_text})
        u = client.messages.create(model=PERSONA_MODEL, max_tokens=300, system=persona_system, messages=persona_msgs)
        user_text = "".join(b.text for b in u.content if b.type == "text").strip()
        log.append({"speaker": "user", "text": user_text})
        persona_msgs.append({"role": "assistant", "content": user_text})
        interviewer_msgs.append({"role": "user", "content": user_text})
        if re.search(r"\b(goodbye|bye)\b", agent_text, re.I):
            break
    agent_turns = [t["text"] for t in log if t["speaker"] == "agent"]
    words = lambda s: len(s.split())  # noqa: E731
    report = {
        "persona": persona,
        "user_talk_ratio": round(sum(words(t["text"]) for t in log if t["speaker"] == "user")
                                 / max(1, sum(words(t["text"]) for t in log)), 2),
        "leading_questions": sum(bool(LEADING.search(t)) for t in agent_turns),
        "multi_question_turns": sum(t.count("?") > 1 for t in agent_turns),
        "turns": log,
    }
    out = ROOT / "eval" / "interviews" / "runs"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{datetime.now():%Y%m%d-%H%M%S}-{persona}.json").write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--persona", choices=sorted(PERSONAS), default="price_cover")
    p.add_argument("--turns", type=int, default=10)
    r = run(p.parse_args().persona, p.parse_args().turns)
    print(json.dumps({k: v for k, v in r.items() if k != "turns"}, indent=2))
