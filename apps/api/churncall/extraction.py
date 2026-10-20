"""Turns an interview transcript into a structured churn insight, with verified quotes.

Every quote the model returns must appear word for word in what the user said. Quotes
that don't are dropped, so no insight ever rests on invented evidence.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field

from . import llm
from .bolna import CallRecord

ReasonCode = Literal[
    "onboarding_friction",
    "missing_feature",
    "price_value_mismatch",
    "switched_to_competitor",
    "reliability_bugs",
    "support_experience",
    "no_longer_needed",
    "budget_cut",
    "other",
]


class Quote(BaseModel):
    quote: str = Field(description="Exact words the user said, copied verbatim from the transcript")


class Reason(BaseModel):
    code: ReasonCode
    detail: str = Field(description="One specific sentence in plain language")
    evidence: list[Quote]


class CallInsight(BaseModel):
    completed: bool = Field(description="True if the user meaningfully answered why they left")
    primary_reason: Reason
    secondary_reasons: list[Reason]
    switched_to: str | None = Field(description="Product or workaround they use now, if mentioned")
    feature_gaps: list[str]
    price_sensitivity: Literal["price_is_the_issue", "value_not_price", "not_mentioned"]
    savable_score: float = Field(description="0 to 1: how likely they'd return if the issue were fixed")
    savable_condition: str | None
    best_quotes: list[Quote]
    summary: str = Field(description="Two sentences for the founder")


SYSTEM = """You analyse customer churn interviews. Extract what the user actually said, not what you expect.
Rules:
- Quotes must be copied word for word from the user's lines. Never paraphrase inside a quote. Never quote the agent.
- If the user didn't say something, leave it empty. Don't infer.
- The primary reason is the root cause the user described, which may differ from their first answer."""


def _normalise(text: str) -> str:
    text = text.lower().replace("’", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"[^\w\s']", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def verify_quotes(insight: CallInsight, record: CallRecord) -> tuple[CallInsight, int]:
    """Drop any quote not found verbatim (after whitespace/punctuation normalisation) in the user's turns."""
    user_text = _normalise(" ".join(t.text for t in record.turns if t.speaker == "user"))
    dropped = 0

    def keep(quotes: list[Quote]) -> list[Quote]:
        nonlocal dropped
        kept = []
        for q in quotes:
            norm = _normalise(q.quote)
            if norm and norm in user_text:
                kept.append(q)
            else:
                dropped += 1
        return kept

    insight.primary_reason.evidence = keep(insight.primary_reason.evidence)
    for r in insight.secondary_reasons:
        r.evidence = keep(r.evidence)
    insight.best_quotes = keep(insight.best_quotes)
    return insight, dropped


def extract_insight(record: CallRecord, company_context: str, client=None) -> tuple[CallInsight, int]:
    """Structured extraction through the configured LLM provider, then verify quotes.
    Returns (insight, quotes_dropped)."""
    user = f"Company context:\n{company_context}\n\nTranscript:\n{record.transcript_text}"
    insight = llm.extract_structured(SYSTEM, user, CallInsight, client=client)
    return verify_quotes(insight, record)
