import Link from "next/link";
import { notFound } from "next/navigation";
import { AdminApiError, adminGet, REASON_LABELS, type CallView, type InviteDetail } from "@/lib/admin.server";

const PRICE: Record<string, string> = {
  price_is_the_issue: "Price itself is the issue",
  value_not_price: "Value, not price",
  not_mentioned: "Not mentioned",
};

function time(at: string | null): string {
  return at ? at.replace("T", " ").slice(0, 19) : "";
}

function Call({ call }: { call: CallView }) {
  const i = call.insight;
  return (
    <section className="box">
      <h3>
        {call.channel ?? "call"} · {call.status ?? "unknown"} <code className="muted">{call.execution_id}</code>
      </h3>
      <p className="muted">
        {time(call.started_at)}
        {call.duration_s ? ` · ${(call.duration_s / 60).toFixed(1)} min` : ""}
        {call.user_talk_ratio != null ? ` · user talked ${Math.round(call.user_talk_ratio * 100)}% of the words` : ""}
      </p>

      {call.recording_url ? (
        <audio controls preload="none" src={call.recording_url} style={{ width: "100%" }} />
      ) : (
        call.turns.length > 0 && <p className="muted">No recording link in the webhook.</p>
      )}

      {i && (
        <div className="box">
          <p>
            <strong>{REASON_LABELS[i.primary_reason.code] ?? i.primary_reason.code}:</strong> {i.primary_reason.detail}
          </p>
          {[...i.primary_reason.evidence, ...i.best_quotes].map((q) => (
            <blockquote key={q.quote}>“{q.quote}”</blockquote>
          ))}
          {i.secondary_reasons.length > 0 && (
            <p>
              Also: {i.secondary_reasons.map((r) => `${REASON_LABELS[r.code] ?? r.code} (${r.detail})`).join("; ")}
            </p>
          )}
          <p>
            Switched to: {i.switched_to ?? "—"} · Missing: {i.feature_gaps.length ? i.feature_gaps.join(", ") : "—"} · Price:{" "}
            {PRICE[i.price_sensitivity]}
          </p>
          <p>
            Savable: <strong>{i.savable_score.toFixed(1)}</strong>
            {i.savable_condition ? ` — if ${i.savable_condition}` : ""}
          </p>
          <p>
            <em>{i.summary}</em>
          </p>
          {call.quotes_dropped ? (
            <p className="muted">{call.quotes_dropped} quote(s) dropped because they weren&apos;t word for word in the transcript.</p>
          ) : null}
        </div>
      )}

      {call.errors.map((e, n) => (
        <div key={n} className="box error">
          <strong>{e.step ?? "error"}</strong> failed at {time(e.at)}: <code>{e.error}</code>
        </div>
      ))}

      {call.turns.length > 0 && (
        <details open={!i}>
          <summary>Transcript ({call.turns.length} turns)</summary>
          {call.turns.map((t, n) => (
            <p key={n} style={{ margin: "4px 0" }}>
              <strong>{t.speaker === "user" ? "User" : "AI"}:</strong> {t.text}
            </p>
          ))}
        </details>
      )}
    </section>
  );
}

export default async function InviteResultsPage({ params }: { params: Promise<{ token: string }> }) {
  const { token } = await params;
  let d: InviteDetail;
  try {
    d = await adminGet<InviteDetail>(`/calls/${encodeURIComponent(token)}`);
  } catch (e) {
    if (e instanceof AdminApiError && e.status === 404) notFound();
    throw e;
  }

  return (
    <main>
      <p>
        <Link href="/results">← All results</Link>
      </p>
      <h1>{d.name}</h1>
      <p>
        {d.company} · {d.plan} plan · {d.tenure_days ?? "?"} days · MRR {d.mrr ?? "?"} · {d.trigger} · status{" "}
        <strong>{d.status}</strong>
      </p>
      <p className="muted">
        {d.email}
        {d.phone_e164 ? ` · ${d.phone_e164}` : ""} · email variant {d.email_variant ?? "—"} · incentive {d.incentive ? "yes" : "no"}
      </p>

      <h2>Timeline</h2>
      {d.events.length === 0 ? (
        <p className="muted">Invited, nothing since.</p>
      ) : (
        <ul>
          {d.events.map((e, n) => (
            <li key={n}>
              <code>{time(e.at)}</code> {e.event}
              {Object.keys(e.meta).length > 0 && <span className="muted"> {JSON.stringify(e.meta)}</span>}
            </li>
          ))}
        </ul>
      )}
      {d.start_errors.map((e, n) => (
        <div key={n} className="box error">
          Couldn&apos;t start a call ({e.where}) at {time(e.at)}: <code>{e.error}</code>
        </div>
      ))}

      <h2>Calls</h2>
      {d.calls.length === 0 ? <p className="muted">No calls yet.</p> : d.calls.map((c) => <Call key={c.execution_id} call={c} />)}
    </main>
  );
}
