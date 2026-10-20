"""The route Bolna posts to (through Next.js at /api/bolna/webhook). Authenticates, then hands the
payload to webhooks.handle_bolna_webhook in the background so Bolna gets a fast 200."""

from __future__ import annotations

import hmac
import ipaddress

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request

from .. import webhooks
from ..bolna import WEBHOOK_IPS
from ..config import get_settings

router = APIRouter(tags=["bolna"])


def _source_ip(request: Request) -> str | None:
    """The IP that reached our public edge: the right-most public address in X-Forwarded-For
    (ngrok and the Next.js proxy append to it, so earlier entries can be forged), else the socket peer."""
    hops = [h.strip() for h in request.headers.get("x-forwarded-for", "").split(",") if h.strip()]
    for hop in reversed(hops):
        try:
            ip = ipaddress.ip_address(hop)
        except ValueError:
            continue
        if not (ip.is_private or ip.is_loopback):
            return hop
    return request.client.host if request.client else None


@router.post("/bolna/webhook")
def bolna_webhook(
    payload: dict,
    request: Request,
    background: BackgroundTasks,
    x_webhook_secret: str | None = Header(default=None),
) -> dict:
    # With WEBHOOK_SECRET set: accept a matching X-Webhook-Secret header, or, if Bolna can't send custom
    # headers, a request from one of Bolna's published IPs. Without it (local dev): accept everything.
    expected = get_settings().webhook_secret
    if expected:
        if x_webhook_secret is not None:
            if not hmac.compare_digest(x_webhook_secret, expected):
                raise HTTPException(status_code=401, detail="bad webhook secret")
        elif _source_ip(request) not in WEBHOOK_IPS:
            raise HTTPException(status_code=401, detail="webhook not from Bolna")
    background.add_task(webhooks.handle_bolna_webhook, payload)
    return {"ok": True}
