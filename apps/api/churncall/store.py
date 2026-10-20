"""The only code that reads or writes stored data.

Storage is append-only JSONL files in the data dir (settings.data_dir) for the kill test. Moving to
Supabase after a "go" means rewriting this file; nothing else touches files.
"""

from __future__ import annotations

import json
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .config import get_settings

# One process (uvicorn) serves routes and webhooks in a thread pool. Hold this lock around any
# "check, then write" so two requests can't both pass the check (e.g. double "completed").
_lock = threading.RLock()


@contextmanager
def locked():
    with _lock:
        yield


def data_dir() -> Path:
    path = get_settings().data_dir
    path.mkdir(parents=True, exist_ok=True)
    return path


def path(relpath: str) -> Path:
    return data_dir() / relpath


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read(name: str) -> list[dict]:
    file = path(name)
    if not file.exists():
        return []
    with file.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def append(name: str, row: dict) -> None:
    with _lock, path(name).open("a") as f:
        f.write(json.dumps(row) + "\n")


def has(name: str, **match) -> bool:
    """True if any row in `name` has all the given field values."""
    return any(all(row.get(k) == v for k, v in match.items()) for row in read(name))
