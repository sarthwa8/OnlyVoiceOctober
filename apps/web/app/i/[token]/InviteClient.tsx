"use client";

import { useEffect, useState } from "react";
import { callMe, logEvent, optOut, type CallResult, type PublicInvite } from "@/lib/api";
import { useWebCall, type WebCallState } from "@/lib/useWebCall";

export type { PublicInvite };

const WEB_CALL_ENABLED = process.env.NEXT_PUBLIC_WEB_CALL_ENABLED === "true";

type State = "idle" | "calling" | "opted_out" | WebCallState | CallResult;

const STATUS_TEXT: Record<State, string> = {
  idle: "",
  connecting: "Connecting…",
  live: "You're live. Talk whenever you're ready.",
  ended: "Thank you!",
  mic_denied: "We couldn't use your microphone. No problem, we'll call you instead. Enter your number below.",
  busy: "Lots of people right now. Tap \"Call me now\" below instead.",
  calling: "Starting the call…",
  ringing: "Your phone will ring in a few seconds.",
  bad_phone: "Please enter your number with the country code, e.g. +91 98000 00000 or +1 415 555 0100.",
  finished: "This link has already been used. Reply to the email if you'd still like to talk.",
  opted_out: "Got it. You won't hear from us about this again.",
  error: "Something went wrong. Reply to the email and we'll sort it out.",
};

export default function InviteClient({ token, invite }: { token: string; invite: PublicInvite }) {
  const [state, setState] = useState<State>("idle");
  const [phone, setPhone] = useState("");
  const [consent, setConsent] = useState(false);
  const webCall = useWebCall(token, WEB_CALL_ENABLED, setState);

  // Runs only in a real browser, so link scanners don't count as "opened". The server dedupes repeats.
  useEffect(() => logEvent(token, "opened"), [token]);

  async function onCallMe() {
    setState("calling");
    setState(await callMe(token, phone, consent));
  }

  async function onOptOut() {
    setState((await optOut(token)) ? "opted_out" : "error");
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

      {WEB_CALL_ENABLED && state !== "mic_denied" && (
        <p>
          {state === "live" || state === "connecting" ? (
            <button onClick={webCall.stop}>End call</button>
          ) : (
            <button onClick={webCall.start} disabled={state === "ended" || state === "ringing"}>
              Talk in browser
            </button>
          )}
        </p>
      )}

      <h2>{WEB_CALL_ENABLED ? "Or we'll call you" : "We'll call you"}</h2>
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
        <button onClick={onCallMe} disabled={!consent || state === "calling" || state === "ringing" || state === "finished"}>
          Call me now
        </button>
      </p>

      {state !== "idle" && (
        <p role="status">
          {state === "ended" && invite.incentive ? `Thank you! ${invite.incentive} is on its way.` : STATUS_TEXT[state]}
        </p>
      )}

      <hr />
      <p>
        <small>
          <button onClick={onOptOut}>Opt out</button> · Questions, or want your data deleted? Just reply to the email.
        </small>
      </p>
    </main>
  );
}
