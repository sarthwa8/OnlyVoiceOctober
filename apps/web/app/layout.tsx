import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "ChurnCall",
  description: "Tell us what we got wrong",
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: 0, padding: 16, lineHeight: 1.5 }}>{children}</body>
    </html>
  );
}
