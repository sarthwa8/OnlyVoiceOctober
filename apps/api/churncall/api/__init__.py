"""The FastAPI app: mounts the routers and turns domain errors into HTTP statuses, in one place."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ..config import get_settings
from ..errors import (
    BolnaUnavailable,
    ChurnCallError,
    ConsentRequired,
    InvalidPhone,
    InviteFinished,
    InviteNotFound,
    TooManyAttempts,
)
from . import admin, bolna_webhook, public

# The invite page depends on these exact codes (InviteClient.tsx stateForCallResponse).
STATUS = {InviteNotFound: 404, InviteFinished: 409, TooManyAttempts: 429, ConsentRequired: 400, InvalidPhone: 422}


def _status_for(exc: ChurnCallError) -> int:
    if isinstance(exc, BolnaUnavailable):
        return exc.status or 502
    return STATUS.get(type(exc), 500)


def create_app() -> FastAPI:
    local = get_settings().is_local  # API docs only on a developer's machine
    app = FastAPI(
        title="ChurnCall API",
        docs_url="/docs" if local else None,
        redoc_url=None,
        openapi_url="/openapi.json" if local else None,
    )

    @app.exception_handler(ChurnCallError)
    async def _domain_error(_: Request, exc: ChurnCallError) -> JSONResponse:
        return JSONResponse({"detail": str(exc)}, status_code=_status_for(exc))

    @app.get("/healthz")
    def healthz() -> dict:
        # Says whether real calls can start, without revealing any values.
        return {"ok": True, "missing_for_calls": get_settings().missing_for_calls()}

    app.include_router(public.router)
    app.include_router(admin.router)
    app.include_router(bolna_webhook.router)
    return app
