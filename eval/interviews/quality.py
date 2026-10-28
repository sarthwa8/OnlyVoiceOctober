"""Interview-quality checks for one transcript, shared by simulate.py, real-call review and tests.

    python eval/interviews/quality.py path/to/transcript.txt     # "assistant: ..." / "user: ..." lines

Targets come from the spec (docs/CHURNCALL.md §6) and the first real interview
(docs/suggested-improvements.md §1-2): the user talks most, the AI keeps turns short,
one question per turn, never frames the answer, and stops when asked.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TARGETS = {
    "user_talk_ratio_min": 0.70,
    "agent_avg_words_max": 15,
    "agent_max_words_max": 25,
    "multi_question_turns_max": 0,
    "leading_questions_max": 0,
    "ignored_end_requests_max": 0,
}

_AGENT = {"assistant", "agent", "ai", "bot"}
# A second question glued on with "and"/"or": "What do you use now, and what about that works better?"
_JOINED = re.compile(r"[,;]?\s+(and|or)\s+(what|how|why|when|where|which|who|would|did|do|does|is|was|were|can|could)\b", re.I)
# Questions that hand the user an answer or describe their reason for them.
_LEADING = re.compile(
    r"\b(was it|is it because|did you leave because|was the (price|cost)|do you think it was|would you say|"
    r"made you feel|for what it offered)\b",
    re.I,
)
_END_REQUEST = re.compile(
    r"\b(end (this|the) call|can we (stop|end)|stop the call|i (have|need) to go|hang up|let'?s stop)\b", re.I
)


def parse_lines(text: str) -> list[dict]:
    turns = []
    for line in text.splitlines():
        if ":" not in line:
            continue
        role, said = line.split(":", 1)
        said = said.strip()
        if said:
            turns.append({"speaker": "agent" if role.strip().lower() in _AGENT else "user", "text": said})
    return turns


def _words(s: str) -> int:
    return len(s.split())


def _is_multi_question(text: str) -> bool:
    questions = [q for q in re.split(r"(?<=[?])\s+", text) if q.strip().endswith("?")]
    if len(questions) > 1:
        return True
    return bool(questions) and bool(_JOINED.search(questions[0]))


def score(turns: list[dict]) -> dict:
    """turns: [{"speaker": "agent"|"user", "text": str}, ...] in order."""
    agent = [t["text"] for t in turns if t["speaker"] == "agent"]
    user = [t["text"] for t in turns if t["speaker"] == "user"]
    total = sum(_words(t["text"]) for t in turns)
    ignored_end = 0
    for i, t in enumerate(turns):
        if t["speaker"] == "user" and _END_REQUEST.search(t["text"]):
            nxt = next((u for u in turns[i + 1 :] if u["speaker"] == "agent"), None)
            if nxt and "?" in nxt["text"]:
                ignored_end += 1
    m = {
        "agent_turns": len(agent),
        "user_turns": len(user),
        "user_talk_ratio": round(sum(map(_words, user)) / total, 2) if total else 0.0,
        "agent_avg_words": round(sum(map(_words, agent)) / len(agent), 1) if agent else 0.0,
        "agent_max_words": max(map(_words, agent), default=0),
        "multi_question_turns": sum(_is_multi_question(a) for a in agent),
        "leading_questions": sum(bool(_LEADING.search(a)) for a in agent),
        "ignored_end_requests": ignored_end,
    }
    # The opener is fixed text (AI disclosure, recording notice), so it's excluded from turn-length checks.
    body = agent[1:] if len(agent) > 1 else agent
    body_words = sum(map(_words, body)) + sum(map(_words, user))
    m["user_talk_ratio_excl_opener"] = round(sum(map(_words, user)) / body_words, 2) if body_words else 0.0
    m["agent_avg_words_excl_opener"] = round(sum(map(_words, body)) / len(body), 1) if body else 0.0
    m["agent_max_words_excl_opener"] = max(map(_words, body), default=0)
    failures = []
    # Gate on the ratio without the fixed opener (AI disclosure + recording notice), which every call must say.
    if m["user_talk_ratio_excl_opener"] < TARGETS["user_talk_ratio_min"]:
        failures.append(f"user talk ratio (excl. opener) {m['user_talk_ratio_excl_opener']} < {TARGETS['user_talk_ratio_min']}")
    if m["agent_avg_words_excl_opener"] > TARGETS["agent_avg_words_max"]:
        failures.append(f"AI averages {m['agent_avg_words_excl_opener']} words/turn > {TARGETS['agent_avg_words_max']}")
    if m["agent_max_words_excl_opener"] > TARGETS["agent_max_words_max"]:
        failures.append(f"longest AI turn {m['agent_max_words_excl_opener']} words > {TARGETS['agent_max_words_max']}")
    for key in ("multi_question_turns", "leading_questions", "ignored_end_requests"):
        if m[key] > TARGETS[f"{key}_max"]:
            failures.append(f"{key.replace('_', ' ')}: {m[key]}")
    m["failures"] = failures
    m["passes"] = not failures
    return m


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(json.dumps(score(parse_lines(Path(sys.argv[1]).read_text())), indent=2))
