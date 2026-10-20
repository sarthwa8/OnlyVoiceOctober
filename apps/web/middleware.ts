import { NextResponse, type NextRequest } from "next/server";

// The results pages show real users' names, emails and transcripts: Basic Auth with the admin key as the
// password (any username). Fails closed: without ADMIN_KEY configured, nobody gets in.
export const config = { matcher: ["/results", "/results/:path*"] };

export function middleware(req: NextRequest) {
  const expected = process.env.ADMIN_KEY;
  const [scheme, encoded] = (req.headers.get("authorization") ?? "").split(" ");
  let password = "";
  if (scheme === "Basic" && encoded) {
    try {
      password = atob(encoded).split(":").slice(1).join(":");
    } catch {
      password = "";
    }
  }
  if (expected && password === expected) return NextResponse.next();
  return new NextResponse("Authentication required", {
    status: 401,
    headers: { "WWW-Authenticate": 'Basic realm="ChurnCall results", charset="UTF-8"' },
  });
}
