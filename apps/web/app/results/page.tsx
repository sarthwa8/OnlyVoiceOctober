import Link from "next/link";
import {
  adminGet,
  REASON_LABELS,
  type CallView,
  type Funnel,
  type FunnelCounts,
  type InviteRow,
  type ReasonGroup,
} from "@/lib/admin.server";

const STATUSES = ["invited", "opened", "started", "completed", "opted_out"];

function pct(part: number, whole: number): string {
  return whole ? `${Math.round((100 * part) / whole)}%` : "–";
}

function FunnelRow({ label, c }: { label: string; c: FunnelCounts }) {
  return (
    <tr>
      <td>{label}</td>
      <td className="num">{c.invited}</td>
      <td className="num">{c.opened}</td>
      <td className="num">{c.started}</td>
      <td className="num">{c.completed}</td>
      <td className="num">{c.opted_out}</td>
      <td className="num">
        <strong>{pct(c.completed, c.invited)}</strong>
      </td>
      <td className="num">{pct(c.completed, c.opened)}</td>
    </tr>
  );
}

function query(params: Record<string, string | undefined>): string {
  const q = new URLSearchParams(Object.entries(params).filter((e): e is [string, string] => !!e[1]));
  return q.size ? `?${q}` : "";
}

export default async function ResultsPage({ searchParams }: { searchParams: Promise<{ company?: string; status?: string }> }) {
  const { company, status } = await searchParams;
  const [funnel, reasons, calls] = await Promise.all([
    adminGet<Funnel>("/funnel"),
    adminGet<ReasonGroup[]>(`/reasons${query({ company })}`),
    adminGet<{ invites: InviteRow[]; unlinked: CallView[] }>(`/calls${query({ company, status })}`),
  ]);
  const channels = Object.keys({ ...funnel.overall.started_by_channel, ...funnel.overall.completed_by_channel });

  return (
    <main>
      <h1>ChurnCall results</h1>

      <h2>Funnel</h2>
      <p className="muted">Unique people at each stage. Completion = completed interviews ÷ people invited (and ÷ people who opened the link).</p>
      <div className="scroll">
        <table>
        <thead>
          <tr>
            <th></th>
            <th className="num">Invited</th>
            <th className="num">Opened</th>
            <th className="num">Started</th>
            <th className="num">Completed</th>
            <th className="num">Opted out</th>
            <th className="num">Completion (of invited)</th>
            <th className="num">(of opened)</th>
          </tr>
        </thead>
        <tbody>
          <FunnelRow label="Overall" c={funnel.overall} />
          {Object.entries(funnel.by_company).map(([slug, c]) => (
            <FunnelRow key={`co-${slug}`} label={`Company: ${slug}`} c={c} />
          ))}
          {Object.entries(funnel.by_incentive).map(([k, c]) => (
            <FunnelRow key={`in-${k}`} label={`Incentive: ${k}`} c={c} />
          ))}
          {Object.entries(funnel.by_email_variant).map(([k, c]) => (
            <FunnelRow key={`ev-${k}`} label={`Email: ${k}`} c={c} />
          ))}
        </tbody>
      </table>
        </div>
      {channels.length > 0 && (
        <p>
          By channel:{" "}
          {channels
            .map((ch) => `${ch}: ${funnel.overall.completed_by_channel[ch] ?? 0} completed of ${funnel.overall.started_by_channel[ch] ?? 0} started`)
            .join(" · ")}
        </p>
      )}

      <h2>Why they left{company ? ` (${company})` : ""}</h2>
      {reasons.length === 0 ? (
        <p className="muted">No analysed interviews yet.</p>
      ) : (
        <div className="scroll">
        <table>
          <thead>
            <tr>
              <th>Reason</th>
              <th className="num">People</th>
              <th className="num">MRR</th>
              <th className="num">Savable</th>
              <th>In their words</th>
            </tr>
          </thead>
          <tbody>
            {reasons.map((g) => (
              <tr key={g.code}>
                <td>{REASON_LABELS[g.code] ?? g.code}</td>
                <td className="num">{g.count}</td>
                <td className="num">${g.mrr.toFixed(0)}</td>
                <td className="num">{g.savable}</td>
                <td>
                  {g.quotes.map((q) => (
                    <blockquote key={q}>“{q}”</blockquote>
                  ))}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
      )}

      <h2>People</h2>
      <p>
        Filter: <Link href="/results">all</Link>
        {Object.keys(funnel.by_company).map((slug) => (
          <span key={slug}>
            {" · "}
            <Link href={`/results${query({ company: slug, status })}`}>{slug}</Link>
          </span>
        ))}
        {" | "}
        {STATUSES.map((s, i) => (
          <span key={s}>
            {i > 0 && " · "}
            <Link href={`/results${query({ company, status: s })}`}>{s}</Link>
          </span>
        ))}
      </p>
      <div className="scroll">
        <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Company</th>
            <th>Status</th>
            <th>Channel</th>
            <th>Reason</th>
            <th className="num">Savable</th>
            <th className="num">Minutes</th>
            <th className="num">MRR</th>
            <th>Last activity</th>
          </tr>
        </thead>
        <tbody>
          {calls.invites.map((r) => (
            <tr key={r.token}>
              <td>
                <Link href={`/results/${encodeURIComponent(r.token)}`}>{r.name}</Link>
              </td>
              <td>{r.company}</td>
              <td>{r.status}</td>
              <td>{r.channel ?? ""}</td>
              <td>{r.primary_reason ? REASON_LABELS[r.primary_reason] ?? r.primary_reason : ""}</td>
              <td className="num">{r.savable_score?.toFixed(1) ?? ""}</td>
              <td className="num">{r.duration_s ? (r.duration_s / 60).toFixed(1) : ""}</td>
              <td className="num">{r.mrr ?? ""}</td>
              <td className="muted">{r.last_event_at?.replace("T", " ").slice(0, 16)}</td>
            </tr>
          ))}
        </tbody>
      </table>
        </div>

      {calls.unlinked.length > 0 && (
        <>
          <h2>Calls not linked to an invite</h2>
          <p className="muted">For example, test calls placed from Bolna&apos;s dashboard.</p>
          <ul>
            {calls.unlinked.map((c) => (
              <li key={c.execution_id}>
                <code>{c.execution_id}</code> · {c.status} · {c.duration_s ? `${(c.duration_s / 60).toFixed(1)} min` : "no duration"}
              </li>
            ))}
          </ul>
        </>
      )}
    </main>
  );
}
