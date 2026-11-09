export const stages = ["Borrador", "Revisión de imagen/marca", "Aprobado", "Programado", "Publicado"] as const;
export const permits = ["Pendiente", "Sí", "No"] as const;
export const objectives = ["Alcance", "Conversación", "Consultas", "Reservas"] as const;
export const formats = ["Foto", "Carrusel", "Reel", "Historia", "Video", "Otro"] as const;
export const kinds = ["piece", "mention", "thanks", "highlight", "lead", "template", "trend"] as const;
export type Kind = (typeof kinds)[number];
export type Entry = { id: string; kind: Kind; data: Record<string, string>; revision: number };
export type Values = Entry["data"];

export const emptyPiece: Values = {
  title: "", participant: "", uso_publico_autorizado: "Pendiente", evidence: "", format: "Foto", cta: "",
  source: "", original: "", finalUrl: "", mediaKey: "", account: "", objective: "Alcance", status: "Borrador",
  selection: "Por revisar", imageCheck: "", brandCheck: "", accountCheck: "", caption: "",
  date: "", postUrl: "", notes: "",
};

export const defaultTemplates = [
  { title: "Gracias por ser parte", category: "Agradecimiento · DM / comentario", body: "¡Gracias, [nombre], por compartir la experiencia Farmasi con CAPTOORA! Nos encantó retratarte en el estudio. ✨" },
  { title: "Retratos de emprendedoras", category: "Carrusel · Consultas", body: "Así se vivió Farmasi en CAPTOORA. [Detalle real de la sesión]. ¿Quieres actualizar tus retratos de marca? Escríbenos «RETRATO» para conocer opciones." },
  { title: "Así se vivió en el estudio", category: "Reel · Reservas", body: "Del montaje al último retrato, así vivimos Farmasi en Monterrey. Envíanos «SESIÓN» por DM para consultar disponibilidad." },
];

export function isWebLink(value: string) {
  try { return ["http:", "https:"].includes(new URL(value).protocol); }
  catch { return false; }
}

const reviewFields = ["title", "participant", "uso_publico_autorizado", "evidence", "format", "cta", "source",
  "original", "finalUrl", "mediaKey", "account", "objective", "selection", "imageCheck", "brandCheck", "accountCheck", "caption"];

export function validateEntry(kind: Kind, data: Values, prior?: Values): string | undefined {
  if (!data.title?.trim()) return "Escribe un título.";
  if (kind === "template" && !data.body?.trim()) return "Escribe el texto de la plantilla.";
  if (kind === "trend" && (!isWebLink(data.url) || !data.hook?.trim())) return "Registra un enlace válido y el gancho de la tendencia.";
  if (kind === "lead" && data.status === "Reservada" && !data.bookingDate) return "Registra la fecha y hora de la reserva.";
  if (kind !== "piece") return;
  const next = stages.indexOf(data.status as typeof stages[number]);
  const before = prior ? stages.indexOf(prior.status as typeof stages[number]) : 0;
  if (next < 0 || next > before + 1 || (next < before && next !== 1)) return "Sigue el orden del pipeline.";
  if (!permits.some((value) => value === data.uso_publico_autorizado)) return "Indica el estado del permiso.";
  if (data.finalUrl && !isWebLink(data.finalUrl)) return "El enlace al archivo final debe comenzar con https:// o http://.";
  if (next < 2) return;
  if (before >= 2 && prior && reviewFields.some((field) => data[field] !== prior[field])) {
    return "Devuelve la pieza a revisión antes de cambiar el material aprobado.";
  }
  if (data.selection !== "Seleccionada") return "Marca la selección personal como completada.";
  if (data.uso_publico_autorizado !== "Sí" || !data.evidence?.trim() || !data.participant?.trim()) {
    return "Registra las personas que aparecen y la constancia de permiso de todas ellas.";
  }
  if (!data.mediaKey && !data.finalUrl) return "Adjunta el archivo final o registra su enlace.";
  if (!["source", "account", "format", "cta", "objective"].every((field) => data[field]?.trim())) {
    return "Completa la fuente, cuenta de destino, formato, CTA y objetivo.";
  }
  if (data.imageCheck !== "Sí" || data.brandCheck !== "Sí" || data.accountCheck !== "Sí") {
    return "Confirma la revisión de imagen, marca y cuenta de destino.";
  }
  if (next >= 3 && !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(data.date || "")) return "Registra fecha y hora de programación manual.";
  if (next === 4 && !isWebLink(data.postUrl)) return "Registra la URL real de la publicación.";
}
