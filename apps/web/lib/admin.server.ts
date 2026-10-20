// Server-only: fetches the private admin API (FastAPI /admin/*) with the admin key.
// Import this ONLY from server components; ADMIN_KEY has no NEXT_PUBLIC_ prefix, so it never reaches the browser,
// and /admin/* is not in the Next.js /api rewrite.

export type Quote = { quote: string };
export type Reason = { code: string; detail: string; evidence: Quote[] };
export type CallInsight = {
  completed: boolean;
  primary_reason: Reason;
  secondary_reasons: Reason[];
  switched_to: string | null;
  feature_gaps: string[];
  price_sensitivity: "price_is_the_issue" | "value_not_price" | "not_mentioned";
  savable_score: number;
  savable_condition: string | null;
  best_quotes: Quote[];
  summary: string;
};
export type Turn = { speaker: string; text: string };
export type CallView = {
  execution_id: string;
  channel: string | null;
  status: string | null;
  started_at: string | null;
  duration_s: number | null;
  recording_url: string | null;
  user_talk_ratio: number | null;
  turns: Turn[];
  insight: CallInsight | null;
  quotes_dropped: number | null;
  errors: Record<string, string>[];
};
export type InviteRow = {
  token: string;
  name: string;
  company: string;
  email_variant: string | null;
  incentive: boolean;
  mrr: number | null;
  status: string;
  channel: string | null;
  primary_reason: string | null;
  savable_score: number | null;
  duration_s: number | null;
  last_event_at: string | null;
};
export type InviteEvent = { token: string; event: string; at: string; meta: Record<string, unknown> };
export type InviteDetail = InviteRow & {
  email: string;
  phone_e164: string | null;
  trigger: string;
  plan: string;
  tenure_days: number | null;
  events: InviteEvent[];
  calls: CallView[];
  start_errors: Record<string, string>[];
};
export type ReasonGroup = { code: string; count: number; mrr: number; savable: number; quotes: string[]; tokens: string[] };
export type FunnelCounts = {
  invited: number;
  opened: number;
  started: number;
  completed: number;
  opted_out: number;
  started_by_channel: Record<string, number>;
  completed_by_channel: Record<string, number>;
};
export type Funnel = {
  overall: FunnelCounts;
  by_company: Record<string, FunnelCounts>;
  by_incentive: Record<string, FunnelCounts>;
  by_email_variant: Record<string, FunnelCounts>;
};

export class AdminApiError extends Error {
  constructor(public status: number, path: string) {
    super(`admin API ${path} returned ${status}`);
  }
}

export async function adminGet<T>(path: string): Promise<T> {
  const res = await fetch(`${process.env.API_URL}/admin${path}`, {
    headers: { "X-Admin-Key": process.env.ADMIN_KEY ?? "" },
    cache: "no-store",
  });
  if (!res.ok) throw new AdminApiError(res.status, path);
  return res.json() as Promise<T>;
}

export const REASON_LABELS: Record<string, string> = {
  onboarding_friction: "Couldn't get set up",
  missing_feature: "Missing a feature",
  price_value_mismatch: "Not worth the price",
  switched_to_competitor: "Switched to a competitor",
  reliability_bugs: "Bugs / outages",
  support_experience: "Bad support experience",
  no_longer_needed: "No longer needed",
  budget_cut: "Budget cut",
  other: "Other",
};
