import { env } from "cloudflare:workers";
import { getChatGPTUser } from "@/app/chatgpt-auth";

const types = ["image/jpeg", "image/png", "image/webp", "video/mp4", "video/webm"];
const maxBytes = 25 * 1024 * 1024;
type Context = { params: Promise<{ key: string }> };

async function location(context: Context) {
  const user = await getChatGPTUser();
  const { key } = await context.params;
  return user && /^[a-f0-9-]{36}$/.test(key) ? `finales/${user.userId}/${key}` : null;
}

export async function PUT(request: Request, context: Context) {
  const key = await location(context);
  if (!key) return new Response(null, { status: 403 });
  const type = request.headers.get("content-type") || "";
  const length = Number(request.headers.get("content-length"));
  if (!types.includes(type) || length > maxBytes) return new Response(null, { status: 415 });
  const bytes = await request.arrayBuffer();
  if (!bytes.byteLength || bytes.byteLength > maxBytes) return new Response(null, { status: 413 });
  if (!env.BUCKET) return new Response(null, { status: 503 });
  const stored = await env.BUCKET.put(key, bytes, { httpMetadata: { contentType: type }, onlyIf: { etagDoesNotMatch: "*" } });
  return new Response(null, { status: stored ? 201 : 409 });
}

export async function GET(_request: Request, context: Context) {
  const key = await location(context);
  if (!key) return new Response(null, { status: 403 });
  const object = await env.BUCKET?.get(key);
  if (!object) return new Response(null, { status: 404 });
  const headers = new Headers({ "Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff" });
  object.writeHttpMetadata(headers);
  return new Response(object.body, { headers });
}
