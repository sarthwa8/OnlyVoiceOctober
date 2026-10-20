import type { NextConfig } from "next";

// The browser only ever talks to this app. Only the routes the invite page and Bolna need are
// forwarded to FastAPI: one public origin (no CORS), the Bolna key never leaves the API, and the
// rest of FastAPI (docs, admin) isn't reachable from the internet.
const nextConfig: NextConfig = {
  // Let the dev server serve its scripts to the ngrok URL (Next blocks unknown dev origins).
  allowedDevOrigins: ["*.ngrok-free.dev", "*.ngrok-free.app"],
  async rewrites() {
    const api = process.env.API_URL ?? "http://localhost:8000";
    return [
      { source: "/api/invites/:path*", destination: `${api}/invites/:path*` },
      { source: "/api/bolna/webhook", destination: `${api}/bolna/webhook` },
    ];
  },
};

export default nextConfig;
