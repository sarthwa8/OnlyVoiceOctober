"""Entry point: `uvicorn churncall.main:app`. The app itself is built in churncall.api."""

from .api import create_app

app = create_app()
