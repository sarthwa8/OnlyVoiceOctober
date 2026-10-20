// Browser-side calls to the invite API (Next.js forwards /api/invites/* to FastAPI).

export type PublicInvite = {
  first_name: string;
  company_name: string;
  founder_name: string;
  trigger_short: string;
  incentive: string | null;
  phone_hint: string | null;
  status: string;
};

export type ClientEvent = "opened" | "web_connected" | "mic_denied" | "call_ended_client";
export type CallResult = "ringing" | "bad_phone" | "finished" | "error";

export function inviteUrl(token: string, path: string): string {
  return `/api/invites/${encodeURIComponent(token)}/${path}`;
}

function post(token: string, path: string, body?: unknown): Promise<Response> {
  return fetch(inviteUrl(token, path), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

/** Fire-and-forget: a lost event must never break the page. */
export function logEvent(token: string, event: ClientEvent, meta?: Record<string, unknown>): void {
  post(token, "event", { event, ...(meta ? { meta } : {}) }).catch(() => {});
}

/** "Call me now". The status codes are the API's contract (build plan 01 §4). */
export async function callMe(token: string, phone: string, consent: boolean): Promise<CallResult> {
  const res = await post(token, "call", { phone_e164: phone.trim() || null, consent }).catch(() => null);
  if (res?.status === 200) return "ringing";
  if (res?.status === 422) return "bad_phone";
  if (res?.status === 409 || res?.status === 429) return "finished";
  return "error";
}

export async function optOut(token: string): Promise<boolean> {
  const res = await post(token, "optout").catch(() => null);
  return !!res?.ok;
}
