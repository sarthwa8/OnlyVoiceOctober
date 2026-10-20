import type { Metadata } from "next";

export const metadata: Metadata = { title: "ChurnCall results", robots: { index: false, follow: false } };

// Admin-only pages (Basic Auth in middleware.ts). Wider than the invite page so tables fit.
export default function ResultsLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <div style={{ maxWidth: 1100, margin: "0 auto" }}>
      <style>{`
        .scroll { overflow-x: auto; margin: 8px 0 24px; }
        table { border-collapse: collapse; width: 100%; font-size: 14px; }
        th, td { border: 1px solid #ddd; padding: 6px 8px; text-align: left; vertical-align: top; }
        th { background: #f6f6f6; }
        td.num, th.num { text-align: right; }
        code { font-size: 12px; }
        blockquote { margin: 4px 0; padding-left: 10px; border-left: 3px solid #ccc; color: #333; }
        .muted { color: #777; }
        .box { border: 1px solid #ddd; padding: 12px; margin: 12px 0; border-radius: 6px; }
        .error { border-color: #e0a0a0; background: #fff6f6; }
      `}</style>
      {children}
    </div>
  );
}
