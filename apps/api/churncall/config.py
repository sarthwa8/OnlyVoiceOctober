"""All configuration, in one place.

Values come from environment variables; the repo-root `.env` is loaded once on first use and never
overrides variables that are already set. Settings are read fresh on every call (it's a handful of dict
lookups), so tests and scripts can change env vars without restarting anything.
Set CHURNCALL_LOAD_DOTENV=0 to skip `.env` entirely (the test suite does, so tests never see real keys).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel

REPO_ROOT = Path(__file__).resolve().parents[3]
_dotenv_loaded = False


class Settings(BaseModel):
    env: Literal["local", "production"] = "production"
    data_dir: Path = Path("data")
    public_base_url: str = ""  # where invite links point; no default, so links are never built against a wrong host
    admin_key: str = ""
    webhook_secret: str = ""
    bolna_api_key: str = ""
    bolna_agent_id: str = ""
    bolna_api_base: str = "https://api.bolna.ai"
    llm_provider: str = "anthropic"
    llm_base_url: str = ""
    llm_api_key: str = ""
    llm_model: str = ""
    llm_model_cheap: str = ""
    prompt_path: Path = REPO_ROOT / "agents" / "interviewer" / "prompt.md"

    @property
    def is_local(self) -> bool:
        return self.env == "local"

    def missing_for_calls(self) -> list[str]:
        """Env vars that must be set before a real call can start. Shown by /healthz; never the values."""
        required = {"BOLNA_API_KEY": self.bolna_api_key, "BOLNA_AGENT_ID": self.bolna_agent_id}
        return [name for name, value in required.items() if not value]


def _load_dotenv_once() -> None:
    global _dotenv_loaded
    if not _dotenv_loaded and os.environ.get("CHURNCALL_LOAD_DOTENV", "1") != "0":
        load_dotenv(REPO_ROOT / ".env")
    _dotenv_loaded = True


def get_settings() -> Settings:
    _load_dotenv_once()
    env = os.environ.get
    return Settings(
        env="local" if env("CHURNCALL_ENV", "").lower() == "local" else "production",
        data_dir=Path(env("CHURNCALL_DATA_DIR") or "data"),
        public_base_url=(env("PUBLIC_BASE_URL") or "").rstrip("/"),
        admin_key=env("ADMIN_KEY", ""),
        webhook_secret=env("WEBHOOK_SECRET", ""),
        bolna_api_key=env("BOLNA_API_KEY", ""),
        bolna_agent_id=env("BOLNA_AGENT_ID", ""),
        bolna_api_base=(env("BOLNA_API_BASE") or "https://api.bolna.ai").rstrip("/"),
        llm_provider=(env("LLM_PROVIDER") or "anthropic").lower(),
        llm_base_url=(env("LLM_BASE_URL") or "").rstrip("/"),
        llm_api_key=env("LLM_API_KEY", ""),
        llm_model=env("LLM_MODEL", ""),
        llm_model_cheap=env("LLM_MODEL_CHEAP", ""),
    )
