"""Admin routes (not forwarded by Next.js; call FastAPI directly). Protected by the X-Admin-Key header,
never a query param, so the key doesn't land in access logs."""

from __future__ import annotations

import hmac

from fastapi import APIRouter, Depends, Header, HTTPException

from ..config import get_settings
from ..funnel import funnel


def require_admin(x_admin_key: str | None = Header(default=None)) -> None:
    expected = get_settings().admin_key
    if not expected or not hmac.compare_digest(x_admin_key or "", expected):
        raise HTTPException(status_code=401, detail="bad admin key")


router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/funnel")
def get_funnel() -> dict:
    return funnel()
