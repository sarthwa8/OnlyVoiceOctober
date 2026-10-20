import importlib.util
import os
from pathlib import Path

# Tests never read the real .env (it holds live keys). Set before any churncall import.
os.environ["CHURNCALL_LOAD_DOTENV"] = "0"

REPO_ROOT = Path(__file__).resolve().parents[3]


def load_script(relpath: str):
    """Import a repo script (scripts/*.py, agents/*.py) by path, without editing sys.path."""
    path = REPO_ROOT / relpath
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
