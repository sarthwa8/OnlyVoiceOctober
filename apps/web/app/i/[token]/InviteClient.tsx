"use client";

import { useEffect, useState } from "react";

export type PublicInvite = {
  first_name: string;
  company_name: string;
  founder_name: string;
  trigger_short: string;
  incentive: string | null;
  phone_hint: string | null;
  status: string;
};

type State = "idle" | "calling" | "ringing" | "bad_phone" | "finished" | "opted_out" | "error";

const STATUS_TEXT: Record<State, string> = {
  idle: "",
  calling: "Starting the call…",
  ringing: "Your phone will ring in a few seconds.",
  bad_phone: "Please enter your number with the country code, e.g. +91 98000 00000 or +1 415 555 0100.",
  finished: "This link has already been used. Reply to the email if you'd still like to talk.",
  opted_out: "Got it. You won't hear from us about this again.",
  error: "Something went wrong. Reply to the email and we'll sort it out.",
};

// How the API's answer to "Call me now" maps to what the user sees.
function stateForCallResponse(status: number | undefined): State {
  if (status === 200) return "ringing";
  if (status === 422) return "bad_phone";
  if (status === 409 || status === 429) return "finished";
  return "error";
}

function post(path: string, body?: unknown) {
  return fetch(`/api/invites/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

export default function InviteClient({ token, invite }: { token: string; invite: PublicInvite }) {
  const [state, setState] = useState<State>("idle");
  const [phone, setPhone] = useState("");
  const [consent, setConsent] = useState(false);
  const t = encodeURIComponent(token);

  // Runs only in a real browser, so link scanners don't count as "opened". The server dedupes repeats.
  useEffect(() => {
    post(`${t}/event`, { event: "opened" }).catch(() => {});
  }, [t]);

  async function callMe() {
    setState("calling");
    const res = await post(`${t}/call`, { phone_e164: phone.trim() || null, consent }).catch(() => null);
    setState(stateForCallResponse(res?.status));
  }

  async function optOut() {
    const res = await post(`${t}/optout`).catch(() => null);
    setState(res?.ok ? "opted_out" : "error");
  }

  if (state === "opted_out") return <p>{STATUS_TEXT.opted_out}</p>;

  return (
    <main>
      <h1>
        Hi {invite.first_name}, I&apos;m {invite.founder_name} from {invite.company_name}.
      </h1>
      <p>
        You recently {invite.trigger_short}. Would you give us about 3 minutes to tell us what we got wrong? You&apos;ll
        talk with our AI interviewer, and I read every answer myself.
      </p>
      <p>
        <strong>This is an AI, not a person.</strong> The conversation is recorded and transcribed. You can stop at any
        time.
      </p>

      {/* "Talk in browser" (Bolna Web Call SDK) is added in Step 6, behind NEXT_PUBLIC_WEB_CALL_ENABLED. */}

      <h2>We&apos;ll call you</h2>
      <p>
        <input
          type="tel"
          inputMode="tel"
          autoComplete="tel"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          placeholder={invite.phone_hint ?? "+91 98000 00000"}
          aria-label="Phone number with country code"
        />
        <br />
        <small>
          {invite.phone_hint ? "Leave empty to use the number we have." : "Include your country code, e.g. +91 or +1."}
        </small>
      </p>
      <p>
        <label>
          <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} /> Yes, call me now
          about my feedback
        </label>
      </p>
      <p>
        <button onClick={callMe} disabled={!consent || state === "calling" || state === "ringing" || state === "finished"}>
          Call me now
        </button>
      </p>

      {state !== "idle" && <p role="status">{STATUS_TEXT[state]}</p>}

      <hr />
      <p>
        <small>
          <button onClick={optOut}>Opt out</button> · Questions, or want your data deleted? Just reply to the email.
        </small>
      </p>
    </main>
  );
}
