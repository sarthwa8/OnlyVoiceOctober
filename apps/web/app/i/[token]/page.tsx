import InviteClient, { type PublicInvite } from "./InviteClient";

// Server component: reads the invite straight from FastAPI. Nothing is logged here, because email
// link scanners fetch this page too. "opened" is logged by InviteClient once it runs in a real browser.
export default async function InvitePage({ params }: { params: Promise<{ token: string }> }) {
  const { token } = await params;
  const res = await fetch(`${process.env.API_URL}/invites/${encodeURIComponent(token)}`, { cache: "no-store" });
  if (res.status === 404) return <p>This link isn&apos;t valid.</p>;
  if (!res.ok) return <p>Something went wrong. Please reply to the email and we&apos;ll sort it out.</p>;

  const invite: PublicInvite = await res.json();
  if (invite.status === "completed") return <p>Thanks, you&apos;ve already shared your feedback.</p>;
  if (invite.status === "opted_out") return <p>Got it. You won&apos;t hear from us about this again.</p>;
  return <InviteClient token={token} invite={invite} />;
}
