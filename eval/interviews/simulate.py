"""Text-only interview simulator: our interviewer prompt vs LLM-played churned-user personas.

Run:  python eval/interviews/simulate.py --persona terse --turns 10
      python eval/interviews/simulate.py --all          # all 6 personas + a score table
Writes transcripts to eval/interviews/runs/ and scores each one with quality.py (the same checks we run
on real calls). Costs real API money (or free-tier quota); keep runs small.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from churncall import llm
from churncall.interview import Company, Contact, render_prompt
from quality import score  # eval/interviews/quality.py (this script's folder is on sys.path)

ROOT = Path(__file__).resolve().parents[2]

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

def run(persona: str, turns: int) -> dict:
    interviewer_system = render_prompt(COMPANY, CONTACT)
    persona_system = (
        f"You are {CONTACT.name}, who recently cancelled {COMPANY.name}. {PERSONAS[persona]} "
        "You are on a phone call with an AI interviewer. Reply with only what you'd say out loud, 1-3 sentences."
    )
    interviewer_msgs: list[dict] = [{"role": "user", "content": "(The call has connected. Begin.)"}]
    persona_msgs: list[dict] = []
    log = []
    for _ in range(turns):
        agent_text = llm.complete(interviewer_system, interviewer_msgs, kind="smart", max_tokens=400, effort="low").strip()
        log.append({"speaker": "agent", "text": agent_text})
        interviewer_msgs.append({"role": "assistant", "content": agent_text})
        persona_msgs.append({"role": "user", "content": agent_text})
        user_text = llm.complete(persona_system, persona_msgs, kind="cheap", max_tokens=300).strip()
        log.append({"speaker": "user", "text": user_text})
        persona_msgs.append({"role": "assistant", "content": user_text})
        interviewer_msgs.append({"role": "user", "content": user_text})
        if re.search(r"\b(goodbye|bye)\b", agent_text, re.I):
            break
    report = {"persona": persona, **score(log), "turns": log}
    out = ROOT / "eval" / "interviews" / "runs"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{datetime.now():%Y%m%d-%H%M%S}-{persona}.json").write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--persona", choices=sorted(PERSONAS), default="price_cover")
    p.add_argument("--all", action="store_true", help="run every persona and print a score table")
    p.add_argument("--turns", type=int, default=10)
    args = p.parse_args()
    if not args.all:
        r = run(args.persona, args.turns)
        print(json.dumps({k: v for k, v in r.items() if k != "turns"}, indent=2))
    else:
        cols = ["user_talk_ratio_excl_opener", "agent_avg_words_excl_opener", "multi_question_turns",
                "leading_questions", "ignored_end_requests", "passes"]
        print("| persona | " + " | ".join(cols) + " |\n|" + "---|" * (len(cols) + 1))
        for persona in sorted(PERSONAS):
            r = run(persona, args.turns)
            print(f"| {persona} | " + " | ".join(str(r[c]) for c in cols) + " |")
