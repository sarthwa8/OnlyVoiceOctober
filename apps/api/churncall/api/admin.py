"""Admin routes (not forwarded by Next.js; call FastAPI directly). Protected by the X-Admin-Key header,
never a query param, so the key doesn't land in access logs."""

from __future__ import annotations

import hmac

from fastapi import APIRouter, Depends, Header, HTTPException

from .. import results
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


@router.get("/reasons", response_model=list[results.ReasonGroup])
def get_reasons(company: str | None = None) -> list[results.ReasonGroup]:
    return results.reasons(company)


@router.get("/calls")
def get_calls(company: str | None = None, status: str | None = None) -> dict:
    return {"invites": results.list_invites(company, status), "unlinked": results.unlinked_calls()}


@router.get("/calls/{token}", response_model=results.InviteDetail)
def get_call_detail(token: str) -> results.InviteDetail:
    return results.invite_detail(token)
