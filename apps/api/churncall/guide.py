"""Builds the per-call interviewer variables and prompt from company + contact context.

agents/interviewer/prompt.md is the Bolna agent prompt, written with {{double_brace}} variables.
In production Bolna fills them from user_data (prompt_variables). Locally, render_prompt() fills the
same template so simulate.py and tests see exactly what the agent would.
"""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel, Field

PROMPT_PATH = Path(__file__).resolve().parents[3] / "agents" / "interviewer" / "prompt.md"

TRIGGERS = {
    "cancelled": ("cancelled their subscription", "cancelled"),
    "downgraded": ("downgraded their plan", "downgraded"),
    "trial_ended": ("finished a trial without upgrading", "finished your trial"),
    "inactive": ("stopped using the product recently", "stopped using it"),
}

DEFAULT_GOALS = [
    "What they originally hoped the product would do (the job they hired it for).",
    "The moment or event that made them start thinking about leaving.",
    "The main reason they left, explored with at least two follow-ups.",
    "What they use or do now instead, and why that works better.",
    "What, if anything, would have kept them (or would bring them back).",
]


class Company(BaseModel):
    name: str
    product_description: str
    founder_name: str
    research_goals: list[str] = Field(default_factory=lambda: list(DEFAULT_GOALS))
    win_back_offer: str | None = None
    incentive: str | None = None


class Contact(BaseModel):
    name: str
    trigger: str = "cancelled"
    plan: str = "unknown"
    tenure_days: int | None = None
    usage_facts: list[str] = Field(default_factory=list)


def opening_line(company: Company, contact: Contact, channel: str = "phone") -> str:
    """The first thing the agent says. Always discloses AI + recording and offers an out."""
    _, short = TRIGGERS.get(contact.trigger, TRIGGERS["cancelled"])
    founder, name = company.founder_name, contact.name
    if channel == "web":
        return (
            f"Hi {name}, thanks for joining. I'm an AI assistant helping {founder} at {company.name}. "
            f"You recently {short}, and {founder} would really value your honest take on what didn't work. "
            "It takes about four minutes, and this conversation is recorded so the team can learn from it. "
            "Is now a good time?"
        )
    return (
        f"Hi {name}, I'm an AI assistant calling on behalf of {founder} at {company.name}. "
        f"You recently {short}, and {founder} would really value your honest take on what didn't work. "
        "It takes about four minutes, and this call is recorded so the team can learn from it. Is now okay?"
    )


def prompt_variables(company: Company, contact: Contact, channel: str = "phone") -> dict[str, str]:
    """Flat string variables for Bolna's user_data. Keys match the {{names}} in prompt.md."""
    long_trigger, _ = TRIGGERS.get(contact.trigger, TRIGGERS["cancelled"])
    goals = "\n".join(f"{i}. {g}" for i, g in enumerate(company.research_goals, 1))
    offer_rule = (
        f"- Only near the end, and only if they sound open to it, you may mention: {company.win_back_offer}"
        if company.win_back_offer
        else "- Do not make any offers or try to win them back."
    )
    return {
        "company_name": company.name,
        "product_description": company.product_description,
        "founder_name": company.founder_name,
        "contact_name": contact.name,
        "trigger_description": long_trigger,
        "trigger_short": TRIGGERS.get(contact.trigger, TRIGGERS["cancelled"])[1],
        "research_goals": goals,
        "example_vague": "it wasn't working for us",
        "offer_rule": offer_rule,
        "plan": contact.plan,
        "tenure_days": str(contact.tenure_days) if contact.tenure_days is not None else "an unknown number of",
        "usage_facts": "; ".join(contact.usage_facts) or "none provided",
        "incentive_line": f"As a thank-you, {company.incentive} is on its way. " if company.incentive else "",
        "opening_line": opening_line(company, contact, channel),
    }


_PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")


def render_prompt(company: Company, contact: Contact, template: str | None = None, channel: str = "phone") -> str:
    """Fill the {{variables}} locally, exactly as Bolna will. Raises if the template uses an unknown variable."""
    template = template if template is not None else PROMPT_PATH.read_text()
    values = prompt_variables(company, contact, channel)
    missing = sorted(set(_PLACEHOLDER.findall(template)) - values.keys())
    if missing:
        raise KeyError(f"prompt template uses variables with no value: {missing}")
    return _PLACEHOLDER.sub(lambda m: values[m.group(1)], template)
