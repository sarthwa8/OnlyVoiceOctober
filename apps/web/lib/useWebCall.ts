"use client";

import { useEffect, useRef } from "react";
import type { BolnaWebCall } from "@bolna/web-call";
import { inviteUrl, logEvent } from "./api";

export type WebCallState = "connecting" | "live" | "ended" | "mic_denied" | "busy" | "error";

/**
 * The Bolna Web Call SDK for one invite: loaded in the browser only, one client per page.
 * Our server mints the session (/api/invites/<token>/web-session), so the browser never holds a Bolna key.
 * `start()` must be called directly from a click handler (browsers block audio otherwise).
 */
export function useWebCall(token: string, enabled: boolean, onState: (state: WebCallState) => void) {
  const callRef = useRef<BolnaWebCall | null>(null);
  const onStateRef = useRef(onState);
  onStateRef.current = onState;
  const live = useRef(false);

  useEffect(() => {
    if (!enabled) return;
    let call: BolnaWebCall | null = null;
    let cancelled = false;
    const emit = (s: WebCallState) => onStateRef.current(s);

    import("@bolna/web-call").then(({ BolnaWebCall }) => {
      if (cancelled) return;
      call = new BolnaWebCall({ sessionUrl: inviteUrl(token, "web-session") });
      call.on("state-change", (s) => {
        if (s === "connecting" || s === "ringing") emit("connecting");
      });
      call.on("call-start", () => {
        live.current = true;
        emit("live");
        logEvent(token, "web_connected", { execution_id: call?.getRunId() }); // links the webhook back to this invite
      });
      call.on("call-end", ({ reason }) => {
        if (live.current) emit("ended");
        live.current = false;
        logEvent(token, "call_ended_client", { reason });
      });
      call.on("error", (e) => {
        if (e.code === "already_active") return;
        if (e.code === "microphone_denied") {
          logEvent(token, "mic_denied");
          return emit("mic_denied");
        }
        if (e.code === "at_capacity") return emit("busy");
        emit("error"); // mint_failed, connect_failed, call_rejected, autoplay_blocked
      });
      callRef.current = call;
    });

    return () => {
      cancelled = true;
      call?.stop();
    };
  }, [token, enabled]);

  return {
    start: () => {
      onStateRef.current("connecting");
      callRef.current?.start().catch(() => {}); // failures arrive through the "error" event
    },
    stop: () => {
      callRef.current?.stop();
    },
  };
}
