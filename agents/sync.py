"""Push the interviewer agent to Bolna: create it if BOLNA_AGENT_ID is empty, otherwise update it.

    python agents/sync.py --dry-run        # print the payload, send nothing
    python agents/sync.py                  # create (and save the new id to .env) or update

Builds the payload from agents/interviewer/config.json (Bolna settings) and prompt.md (the prompt).
prompt.md uses Bolna's {{double_brace}} placeholders, which Bolna fills from each call's user_data
(churncall.interview fills the same ones locally); a stray {single_brace} one is refused.

The prompt's opener becomes Bolna's welcome message, which Bolna speaks first, so the copy sent to Bolna
says the opener was "already spoken". prompt.md itself keeps "Open the call exactly like this", because
eval/interviews/simulate.py has no welcome message and needs the agent to say the opener as its first turn.

When PUBLIC_BASE_URL is an https URL, the agent's webhook is set to <PUBLIC_BASE_URL>/api/bolna/webhook
(Next.js forwards it to FastAPI).
"""

from __future__ import annotations

import argparse
import json
import re
import sys

import httpx

from churncall.bolna import BolnaClient
from churncall.config import REPO_ROOT, get_settings

AGENT_DIR = REPO_ROOT / "agents" / "interviewer"
ENV_PATH = REPO_ROOT / ".env"
OPENER_HEADING = "## Open the call exactly like this"
_SINGLE_BRACE = re.compile(r"(?<!\{)\{[a-z_]+\}(?!\})")


def build_payload() -> dict:
    config = json.loads((AGENT_DIR / "config.json").read_text())
    config.pop("_comment", None)
    prompt = (AGENT_DIR / "prompt.md").read_text()
    prompt = re.sub(r"<!--.*?-->\n?", "", prompt, flags=re.S)  # drop the note meant for humans
    if stray := _SINGLE_BRACE.findall(prompt):
        raise SystemExit(f"prompt.md has single-brace placeholders Bolna won't fill: {sorted(set(stray))} (use {{{{name}}}})")

    opener = re.search(re.escape(OPENER_HEADING) + r'\n"(.+?)"\n', prompt)
    if not opener:
        raise SystemExit(f"couldn't find the quoted opener under '{OPENER_HEADING}' in prompt.md")
    prompt = prompt.replace(
        f'{OPENER_HEADING}\n"{opener.group(1)}"\n',
        "## Opening (already spoken)\n"
        f'You have already said this to them as your first line: "{opener.group(1)}"\n'
        "Do not repeat it. Continue from their answer.\n",
    )

    config["agent_welcome_message"] = opener.group(1)
    base = get_settings().public_base_url
    if base.startswith("https://"):  # Bolna can't reach localhost; only set a public webhook
        config["webhook_url"] = f"{base}/api/bolna/webhook"
    return {"agent_config": config, "agent_prompts": {"task_1": {"system_prompt": prompt}}}


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
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="print the payload and exit")
    args = parser.parse_args(argv)

    payload = build_payload()
    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return 0

    settings = get_settings()
    if not settings.bolna_api_key:
        raise SystemExit("BOLNA_API_KEY is not set in .env")
    agent_id = settings.bolna_agent_id.strip() or None
    try:
        body = BolnaClient().upsert_agent(payload, agent_id=agent_id)
    except httpx.HTTPStatusError as exc:
        print(f"Bolna returned {exc.response.status_code}: {exc.response.text}", file=sys.stderr)
        return 1

    if agent_id:
        print(f"Updated agent {agent_id}: {body}")
    else:
        save_agent_id(body["agent_id"])
        print(f"Created agent {body['agent_id']} ({body.get('state')}); saved BOLNA_AGENT_ID to .env")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
