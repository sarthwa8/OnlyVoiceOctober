"""Builds the per-call interviewer prompt from company + contact context."""

from __future__ import annotations

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


def prompt_variables(company: Company, contact: Contact) -> dict[str, str]:
    """Values for the prompt's placeholders. Bolna fills its {{name}} copy of the prompt from these via user_data."""
    long_trigger, short_trigger = TRIGGERS.get(contact.trigger, TRIGGERS["cancelled"])
    goals = "\n".join(f"{i}. {g}" for i, g in enumerate(company.research_goals, 1))
    offer_rule = (
        f"- Only near the end, and only if they sound open to it, you may mention: {company.win_back_offer}"
        if company.win_back_offer
        else "- Do not make any offers or try to win them back."
    )
    incentive_line = f"As a thank-you, {company.incentive} is on its way. " if company.incentive else ""
    values = {
        "company_name": company.name,
        "product_description": company.product_description,
        "founder_name": company.founder_name,
        "contact_name": contact.name,
        "trigger_description": long_trigger,
        "trigger_short": short_trigger,
        "research_goals": goals,
        "example_vague": "it wasn't working for us",
        "offer_rule": offer_rule,
        "plan": contact.plan,
        "tenure_days": contact.tenure_days if contact.tenure_days is not None else "an unknown number of",
        "usage_facts": "; ".join(contact.usage_facts) or "none provided",
        "incentive_line": incentive_line,
    }
    return {key: str(val) for key, val in values.items()}


def render_prompt(company: Company, contact: Contact, template: str | None = None) -> str:
    template = template if template is not None else PROMPT_PATH.read_text()
    out = template
    for key, val in prompt_variables(company, contact).items():
        out = out.replace("{" + key + "}", val)
    return out
