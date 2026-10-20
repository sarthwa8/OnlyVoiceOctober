// The invite page: a narrow, phone-friendly column.
export default function InviteLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <div style={{ maxWidth: 560, margin: "0 auto" }}>{children}</div>;
}
