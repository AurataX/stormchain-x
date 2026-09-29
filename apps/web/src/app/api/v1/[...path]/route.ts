// Same-origin proxy: the operator token stays server-side (local demo, loopback only).
const API = process.env.API_URL ?? "http://127.0.0.1:8000";

async function forward(request: Request, context: { params: Promise<{ path: string[] }> }) {
  const { path } = await context.params;
  if (path.some((part) => part === ".." || part === ".")) {
    return Response.json({ detail: "Invalid path" }, { status: 400 });
  }
  const headers = new Headers({ "content-type": "application/json" });
  const write = request.method === "POST";
  if (write && process.env.OPERATOR_TOKEN) {
    headers.set("authorization", `Bearer ${process.env.OPERATOR_TOKEN}`);
  }
  try {
    const upstream = await fetch(`${API}/api/v1/${path.join("/")}${new URL(request.url).search}`, {
      method: request.method,
      headers,
      body: write ? await request.text() : undefined,
      cache: "no-store",
    });
    return new Response(upstream.body, {
      status: upstream.status,
      headers: { "content-type": upstream.headers.get("content-type") ?? "application/json" },
    });
  } catch {
    return Response.json({ detail: "API unreachable" }, { status: 502 });
  }
}

export { forward as GET, forward as POST };
