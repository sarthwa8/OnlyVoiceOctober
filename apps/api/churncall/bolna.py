"""Thin Bolna API client.

Endpoint paths and payload field names are our best understanding of Bolna's API and are
marked VERIFY: confirm them against the Bolna docs on Day 0 before relying on them.
"""

from __future__ import annotations

import os

import httpx


class BolnaClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, agent_id: str | None = None):
        self.api_key = api_key or os.environ.get("BOLNA_API_KEY", "")
        self.base_url = (base_url or os.environ.get("BOLNA_API_BASE", "https://api.bolna.ai")).rstrip("/")
        self.agent_id = agent_id or os.environ.get("BOLNA_AGENT_ID", "")

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def start_outbound_call(self, phone_e164: str, user_data: dict, timeout: float = 15.0) -> dict:
        """Place a call the user explicitly requested ("call me now"). Never use for cold calls."""
        payload = {
            "agent_id": self.agent_id,  # VERIFY field name
            "recipient_phone_number": phone_e164,  # VERIFY field name
            "user_data": user_data,  # VERIFY: injected into the prompt as variables
        }
        resp = httpx.post(f"{self.base_url}/call", json=payload, headers=self._headers(), timeout=timeout)  # VERIFY path
        resp.raise_for_status()
        return resp.json()
