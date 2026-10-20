import os

# Tests never read the real .env (it holds live keys). Set before any churncall import.
os.environ["CHURNCALL_LOAD_DOTENV"] = "0"
