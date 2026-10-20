"""Turn a pilot startup's churned-user CSV into one private invite link per user.

    python scripts/make_invites.py --company acme --csv pilots/acme.csv

Needs data/companies/<company>.json (a Company: name, product_description, founder_name, ...).
CSV columns: name,email (required) and phone_e164,plan,mrr,trigger,tenure_days,incentive,email_variant.
Writes invites to $CHURNCALL_DATA_DIR/invites.jsonl and a mail-merge file to
$CHURNCALL_DATA_DIR/links/<company>.csv with name,email,link,email_variant.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from churncall import store
from churncall.config import get_settings
from churncall.invites import create_invite, load_company


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--company", required=True, help="company slug, matching data/companies/<slug>.json")
    parser.add_argument("--csv", required=True, type=Path, help="churned users CSV from the pilot startup")
    parser.add_argument("--base-url", default=get_settings().public_base_url, help="defaults to $PUBLIC_BASE_URL")
    args = parser.parse_args(argv)

    if not args.base_url:
        parser.error("set PUBLIC_BASE_URL in .env or pass --base-url (the links are built from it)")
    try:
        load_company(args.company)
    except FileNotFoundError as exc:
        parser.error(str(exc))

    created, skipped = [], []
    with args.csv.open(newline="") as f:
        for row_number, row in enumerate(csv.DictReader(f), start=2):  # row 1 is the header
            try:
                created.append(create_invite(args.company, row))
            except ValueError as exc:
                skipped.append(f"row {row_number}: {exc}")

    links_dir = store.data_dir() / "links"
    links_dir.mkdir(exist_ok=True)
    links_path = links_dir / f"{args.company}.csv"
    with links_path.open("a" if links_path.exists() else "w", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["name", "email", "link", "email_variant"])
        for inv in created:
            writer.writerow([inv.contact.name, inv.email, f"{args.base_url.rstrip('/')}/i/{inv.token}", inv.email_variant or ""])

    print(f"Created {len(created)} invites, skipped {len(skipped)}. Links: {links_path}")
    for line in skipped:
        print(f"  skipped {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
