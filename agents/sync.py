"""Push the interviewer agent to Bolna: create it if BOLNA_AGENT_ID is empty, otherwise update it.

    python agents/sync.py --dry-run        # print the payload, send nothing
    python agents/sync.py                  # create (and save the new id to .env) or update

Builds the payload from agents/interviewer/config.json (Bolna settings) and prompt.md (the prompt).
prompt.md uses Bolna's {{double_brace}} placeholders (guide.py fills the same ones locally); any stray
{single_brace} ones are converted here. Bolna fills them from a call's user_data. The prompt's opener becomes the welcome message, which
Bolna speaks first, so the prompt tells the LLM not to repeat it. When PUBLIC_BASE_URL is an https URL,
the agent's webhook is set to <PUBLIC_BASE_URL>/api/bolna/webhook (Next.js forwards it to FastAPI).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / "agents" / "interviewer"
ENV_PATH = ROOT / ".env"
OPENER_HEADING = "## Open the call exactly like this"


def to_bolna_placeholders(text: str) -> str:
    return re.sub(r"(?<!\{)\{([a-z_]+)\}(?!\})", r"{{\1}}", text)


def build_payload() -> dict:
    config = json.loads((AGENT_DIR / "config.json").read_text())
    config.pop("_comment", None)
    prompt = (AGENT_DIR / "prompt.md").read_text()
    prompt = re.sub(r"<!--.*?-->\n?", "", prompt, flags=re.S)  # drop the note meant for humans

    opener = re.search(re.escape(OPENER_HEADING) + r'\n"(.+?)"\n', prompt)
    if not opener:
        raise SystemExit(f"couldn't find the quoted opener under '{OPENER_HEADING}' in prompt.md")
    prompt = prompt.replace(
        f'{OPENER_HEADING}\n"{opener.group(1)}"\n',
        "## Opening (already spoken)\n"
        f'You have already said this to them as your first line: "{opener.group(1)}"\n'
        "Do not repeat it. Continue from their answer.\n",
    )

    config["agent_welcome_message"] = to_bolna_placeholders(opener.group(1))
    base = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")
    if base.startswith("https://"):  # Bolna can't reach localhost; only set a public webhook
        config["webhook_url"] = f"{base}/api/bolna/webhook"
    return {"agent_config": config, "agent_prompts": {"task_1": {"system_prompt": to_bolna_placeholders(prompt)}}}


def save_agent_id(agent_id: str) -> None:
    lines = ENV_PATH.read_text().splitlines() if ENV_PATH.exists() else []
    for i, line in enumerate(lines):
        if line.startswith("BOLNA_AGENT_ID="):
            lines[i] = f"BOLNA_AGENT_ID={agent_id}"
            break
    else:
        lines.append(f"BOLNA_AGENT_ID={agent_id}")
    ENV_PATH.write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    load_dotenv(ENV_PATH)
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="print the payload and exit")
    args = parser.parse_args(argv)

    payload = build_payload()
    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return 0

    key = os.environ.get("BOLNA_API_KEY")
    if not key:
        raise SystemExit("BOLNA_API_KEY is not set in .env")
    base = os.environ.get("BOLNA_API_BASE", "https://api.bolna.ai").rstrip("/")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    agent_id = os.environ.get("BOLNA_AGENT_ID", "").strip()

    if agent_id:
        resp = httpx.put(f"{base}/v2/agent/{agent_id}", json=payload, headers=headers, timeout=30)
    else:
        resp = httpx.post(f"{base}/v2/agent", json=payload, headers=headers, timeout=30)
    if resp.status_code >= 400:
        print(f"Bolna returned {resp.status_code}: {resp.text}", file=sys.stderr)
        return 1

    body = resp.json()
    if agent_id:
        print(f"Updated agent {agent_id}: {body}")
    else:
        save_agent_id(body["agent_id"])
        print(f"Created agent {body['agent_id']} ({body.get('state')}); saved BOLNA_AGENT_ID to .env")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
