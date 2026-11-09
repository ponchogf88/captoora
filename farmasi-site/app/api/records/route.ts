import { env } from "cloudflare:workers";
import { and, desc, eq } from "drizzle-orm";
import { getDb } from "@/db";
import { records } from "@/db/schema";
import { getChatGPTUser } from "@/app/chatgpt-auth";
import { kinds, validateEntry, type Entry, type Values } from "@/app/model";

export const dynamic = "force-dynamic";
const fail = (error: string, status: number) => Response.json({ error }, { status });

export async function GET() {
  const user = await getChatGPTUser();
  if (!user) return fail("Inicia sesión para ver tus registros.", 401);
  const rows = await getDb().select().from(records).where(eq(records.owner, user.userId)).orderBy(desc(records.updated));
  return Response.json(rows.map(({ id, kind, data, revision }) => ({ id, kind, data: JSON.parse(data), revision })));
}

export async function POST(request: Request) {
  const user = await getChatGPTUser();
  if (!user) return fail("Inicia sesión para guardar.", 401);
  const input = await request.json().catch(() => null) as Entry | null;
  if (!input || !/^[a-f0-9-]{36}$/.test(input.id) || !kinds.includes(input.kind) ||
      !Number.isInteger(input.revision) || input.revision < 0 || !input.data || Array.isArray(input.data) ||
      typeof input.data !== "object" || Object.keys(input.data).length > 40 ||
      Object.values(input.data).some((value) => typeof value !== "string" || value.length > 12000)) {
    return fail("Revisa los datos del registro.", 400);
  }
  const { id, kind, data, revision } = input;
  const owner = user.userId;
  const db = getDb();
  const scope = and(eq(records.owner, owner), eq(records.id, id));
  const current = await db.select().from(records).where(scope).get();
  if (current && current.kind === "piece" && kind === "piece" && revision === 0 && data.localRef) {
    const prior = JSON.parse(current.data) as Values;
    if (prior.localRef === data.localRef) return Response.json({ id, kind, data: prior, revision: current.revision });
  }
  const conflict = () => fail("El registro cambió en otra pestaña. Vuelve a cargar el tablero.", 409);
  if ((current?.revision ?? 0) !== revision || (current && current.kind !== kind)) return conflict();
  const error = validateEntry(kind, data, current ? JSON.parse(current.data) as Values : undefined);
  if (error) return fail(error, 400);
  if (kind === "piece" && data.mediaKey && (!/^[a-f0-9-]{36}$/.test(data.mediaKey) ||
      !await env.BUCKET?.head(`finales/${owner}/${data.mediaKey}`))) {
    return fail("El archivo final privado no está disponible. Vuelve a adjuntarlo.", 400);
  }
  if (kind === "highlight" && ["Lista", "Añadida"].includes(data.status)) {
    const linked = await db.select().from(records)
      .where(and(eq(records.owner, owner), eq(records.id, data.pieceId || ""), eq(records.kind, "piece"))).get();
    const piece = linked && JSON.parse(linked.data) as Values;
    if (!piece || piece.uso_publico_autorizado !== "Sí" || !["Aprobado", "Programado", "Publicado"].includes(piece.status)) {
      return fail("Vincula una pieza aprobada con permiso de uso público para la destacada.", 400);
    }
  }
  const row = { owner, id, kind, data: JSON.stringify(data), updated: new Date().toISOString(), revision: revision + 1 };
  const written = current
    ? await db.update(records).set(row).where(and(scope, eq(records.revision, revision))).returning({ id: records.id })
    : await db.insert(records).values(row).onConflictDoNothing().returning({ id: records.id });
  if (!written.length) return conflict();
  return Response.json({ id, kind, data, revision: row.revision });
}
