import type { NextConfig } from "next";

// The browser only ever talks to this app. /api/* is forwarded to FastAPI, so there is
// one public origin (no CORS) and the Bolna key never leaves the API.
const nextConfig: NextConfig = {
  // Let the dev server serve its scripts to the ngrok URL (Next blocks unknown dev origins).
  allowedDevOrigins: ["*.ngrok-free.dev", "*.ngrok-free.app"],
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${process.env.API_URL ?? "http://localhost:8000"}/:path*` }];
  },
};

export default nextConfig;
