"use client";

import { useEffect, useRef, useState, type FormEvent, type ReactNode } from "react";
import {
  Aperture, ArrowLeft, ArrowRight, ArrowUpRight, CalendarDays, Camera, Check, CheckCircle2,
  ChevronLeft, ChevronRight, ClipboardList, Copy, FileImage, FolderOpen, HeartHandshake, ImagePlus,
  LayoutDashboard, Link2, ListChecks, LockKeyhole, Megaphone, MessageCircle, Plus, Search, ShieldCheck,
  Sparkles, Star, TrendingUp, X,
} from "lucide-react";
import {
  defaultTemplates, emptyPiece, formats, isWebLink, objectives, permits, stages, validateEntry,
  type Entry, type Kind, type Values,
} from "./model";

const nav = [
  { label: "Operación", links: [
    { key: "home", label: "Vista general", icon: LayoutDashboard },
    { key: "selection", label: "Selección de archivos", icon: FolderOpen },
    { key: "approval", label: "Revisión y aprobación", icon: ShieldCheck },
    { key: "calendar", label: "Calendario", icon: CalendarDays },
  ] },
  { label: "Conversaciones", links: [
    { key: "mentions", label: "Menciones e historias", icon: Megaphone },
    { key: "thanks", label: "Agradecimientos", icon: HeartHandshake },
    { key: "highlights", label: "Experiencias", icon: Star },
    { key: "leads", label: "Consultas y reservas", icon: MessageCircle },
  ] },
  { label: "Recursos", links: [
    { key: "templates", label: "Plantillas", icon: ClipboardList },
    { key: "trends", label: "Tendencias", icon: TrendingUp },
  ] },
] as const;
type View = typeof nav[number]["links"][number]["key"];

const views: Record<View, [string, string, string]> = {
  home: ["Control de campaña", "Vista general", "Selección, permisos y seguimiento comercial de una sola sesión."],
  selection: ["Producción", "Selección de archivos", "Revisa tus originales y registra la selección personal antes de aprobar cualquier pieza."],
  approval: ["Producción", "Revisión y aprobación", "Confirma el material final, el permiso de cada participante y la cuenta de destino."],
  calendar: ["Producción", "Calendario editorial", "Control de programación manual. Horarios de Monterrey."],
  mentions: ["Conversaciones", "Menciones e historias", "Registra menciones, su vigencia y el seguimiento de cada historia."],
  thanks: ["Conversaciones", "Agradecimientos", "Prepara respuestas y registra los DM o comentarios después de enviarlos desde la cuenta correspondiente."],
  highlights: ["Conversaciones", "Experiencias", "Organiza las historias autorizadas para la destacada «Experiencias» de Instagram."],
  leads: ["Comercial", "Consultas y reservas", "Sigue cada conversación hasta la reserva y conserva el origen de la consulta."],
  templates: ["Recursos", "Plantillas de captions", "Usa una base editable para publicaciones, historias y respuestas."],
  trends: ["Recursos", "Registro de tendencias", "Guarda el enlace, el gancho y cómo se puede adaptar a CAPTOORA."],
};

type Field = { key: string; label: string; type?: string; options?: readonly string[]; hint?: string; required?: boolean };
const states = (options: string[]): Field => ({ key: "status", label: "Estado", options });
const accountField: Field = { key: "account", label: "Cuenta", hint: "Ej. Instagram · @captoora.studio" };
const tracker: Record<Exclude<Kind, "piece">, { name: string; action: string; empty: string; fields: Field[] }> = {
  mention: { name: "Mención", action: "Registrar mención", empty: "Sin menciones registradas", fields: [
    { key: "title", label: "Título", required: true }, { key: "participant", label: "Participante o @usuario" }, accountField,
    { key: "type", label: "Tipo", options: ["Historia", "Publicación", "Reel", "Comentario"] },
    { key: "url", label: "Enlace o evidencia", type: "url" }, { key: "date", label: "Vence (Monterrey)", type: "datetime-local" },
    { key: "pieceId", label: "Pieza relacionada", type: "piece" },
    states(["Por revisar", "Vigente", "Reposteada", "Vencida", "Archivada"]), { key: "notes", label: "Seguimiento", type: "textarea" },
  ] },
  thanks: { name: "Agradecimiento", action: "Nuevo agradecimiento", empty: "Sin agradecimientos registrados", fields: [
    { key: "title", label: "Título", required: true }, { key: "participant", label: "Destinatario o @usuario" }, accountField,
    { key: "type", label: "Canal", options: ["DM", "Comentario"] },
    { key: "mentionId", label: "Mención de origen", type: "mention" },
    { key: "date", label: "Fecha de envío (Monterrey)", type: "datetime-local" },
    states(["Pendiente", "Redactado", "Enviado", "Respondido"]),
    { key: "body", label: "Texto del agradecimiento", type: "textarea" }, { key: "url", label: "Enlace o referencia del envío", type: "url" },
  ] },
  highlight: { name: "Historia para Experiencias", action: "Añadir historia", empty: "Sin historias en la destacada", fields: [
    { key: "title", label: "Título de la historia", required: true }, accountField,
    { key: "pieceId", label: "Pieza autorizada", type: "piece" }, { key: "mentionId", label: "Mención de origen", type: "mention" },
    { key: "url", label: "Enlace a la historia o destacada", type: "url" },
    states(["Candidata", "Lista", "Añadida"]), { key: "notes", label: "Orden, portada o notas", type: "textarea" },
  ] },
  lead: { name: "Consulta o reserva", action: "Registrar consulta", empty: "Sin consultas ni reservas registradas", fields: [
    { key: "title", label: "Nombre o @usuario", required: true }, accountField,
    { key: "source", label: "Origen o código de atribución" }, { key: "pieceId", label: "Pieza de origen", type: "piece" },
    { key: "mentionId", label: "Mención de origen", type: "mention" }, { key: "service", label: "Servicio de interés" },
    states(["Nueva", "En seguimiento", "Cotizada", "Reservada", "Realizada", "Cerrada"]),
    { key: "date", label: "Próximo seguimiento", type: "datetime-local" }, { key: "bookingDate", label: "Fecha de la reserva", type: "datetime-local" },
    { key: "quoted", label: "Cotización (MXN)", type: "number" }, { key: "paid", label: "Cobro confirmado (MXN)", type: "number" },
    { key: "notes", label: "Próximo paso y notas", type: "textarea" },
  ] },
  template: { name: "Plantilla", action: "Nueva plantilla", empty: "Sin plantillas propias", fields: [
    { key: "title", label: "Nombre", required: true }, { key: "category", label: "Uso o formato" },
    { key: "body", label: "Texto reutilizable", type: "textarea", required: true },
  ] },
  trend: { name: "Tendencia", action: "Registrar tendencia", empty: "Sin tendencias registradas", fields: [
    { key: "title", label: "Nombre", required: true }, { key: "platform", label: "Plataforma", options: ["Instagram", "TikTok", "Facebook", "YouTube", "Otra"] },
    { key: "url", label: "URL de la fuente", type: "url", required: true }, { key: "date", label: "Fecha de hallazgo", type: "date" },
    { key: "hook", label: "Gancho observado", required: true }, { key: "objective", label: "Objetivo", options: objectives },
    states(["Por evaluar", "En prueba", "Usada", "Archivada"]), { key: "notes", label: "Adaptación para CAPTOORA", type: "textarea" },
  ] },
};

const viewKinds: Partial<Record<View, Exclude<Kind, "piece">>> = {
  mentions: "mention", thanks: "thanks", highlights: "highlight", leads: "lead", templates: "template", trends: "trend",
};

function useRecords() {
  const [entries, setEntries] = useState<Entry[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  async function load() {
    setLoading(true);
    setLoadError("");
    try {
      const res = await fetch("/api/records", { cache: "no-store" });
      if (!res.ok) throw Error(res.status === 401 ? "Abre el Site con tu sesión de ChatGPT para cargar tus registros." : "No se pudieron cargar los registros.");
      setEntries(await res.json());
    } catch (error) { setLoadError(error instanceof Error ? error.message : "Error al cargar los registros."); }
    finally { setLoading(false); }
  }
  useEffect(() => { void load(); }, []);
  async function save(entry: Entry) {
    const res = await fetch("/api/records", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(entry) });
    if (!res.ok) throw Error(((await res.json().catch(() => ({}))) as { error?: string }).error || "No se pudo guardar el registro.");
    const result = await res.json() as Entry;
    setEntries((old) => [result, ...old.filter(({ id }) => id !== result.id)]);
  }
  return { entries, loading, loadError, load, save };
}

function Blank({ title, detail, icon = <FileImage size={23} />, action }: { title: string; detail: string; icon?: ReactNode; action?: ReactNode }) {
  return <div className="blank"><span className="blank-icon">{icon}</span><strong>{title}</strong><p>{detail}</p>{action}</div>;
}

function Badge({ children, tone = "" }: { children: ReactNode; tone?: string }) {
  return <span className={`badge ${tone}`}>{children}</span>;
}

function statusTone(status: string) {
  if (["Aprobado", "Publicado", "Reservada", "Añadida", "Sí", "Seleccionada"].includes(status)) return "good";
  if (["Revisión de imagen/marca", "Programado", "Pendiente", "Vigente"].includes(status)) return "warm";
  if (["No", "Vencida"].includes(status)) return "bad";
  return "";
}

function newId() {
  const bytes = crypto.getRandomValues(new Uint8Array(16));
  bytes[6] = (bytes[6] & 15) | 64;
  bytes[8] = (bytes[8] & 63) | 128;
  return formatId(bytes);
}

function formatId(bytes: Uint8Array) {
  const hex = Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("");
  return [hex.slice(0, 8), hex.slice(8, 12), hex.slice(12, 16), hex.slice(16, 20), hex.slice(20, 32)].join("-");
}

const dayLabel = (value: string) => value ? value.slice(0, 10).split("-").reverse().join("/") + (value.length > 10 ? ` · ${value.slice(11, 16)}` : "") : "—";
const today = () => new Intl.DateTimeFormat("sv-SE", { timeZone: "America/Monterrey", dateStyle: "short" }).format(new Date());
const money = (value: number) => new Intl.NumberFormat("es-MX", { style: "currency", currency: "MXN", maximumFractionDigits: 2 }).format(value);

function Dashboard() {
  const [view, setView] = useState<View>("home");
  const [editor, setEditor] = useState<Entry | null>(null);
  const [picking, setPicking] = useState(false);
  const [message, setMessage] = useState("");
  const [filters, setFilters] = useState({ q: "", account: "", permit: "", status: "", objective: "" });
  const [leadMode, setLeadMode] = useState("Todas");
  const store = useRecords();
  const pieces = store.entries.filter((entry) => entry.kind === "piece");
  const accounts = [...new Set(store.entries.map(({ data }) => data.account).filter(Boolean))].sort();
  const matches = ({ data: d }: Entry) =>
    (!filters.account || d.account === filters.account) &&
    (!filters.permit || d.uso_publico_autorizado === filters.permit) &&
    (!filters.status || d.status === filters.status) &&
    (!filters.objective || d.objective === filters.objective) &&
    (!filters.q || Object.values(d).some((v) => v.toLocaleLowerCase("es-MX").includes(filters.q.trim().toLocaleLowerCase("es-MX"))));
  const visiblePieces = pieces.filter(matches);
  const templates = [...defaultTemplates, ...store.entries.filter(({ kind }) => kind === "template").map(({ data }) => ({ title: data.title, category: data.category, body: data.body }))];
  const kind = viewKinds[view];
  const meta = views[view];

  function navigate(next: View) {
    setView(next);
    setFilters({ q: "", account: "", permit: "", status: "", objective: "" });
    setLeadMode("Todas");
    window.scrollTo({ top: 0 });
  }
  function create(kind: Kind, preset: Values = {}) {
    const data = kind === "piece" ? { ...emptyPiece } : Object.fromEntries(tracker[kind].fields.map(({ key, options }) => [key, options?.[0] || ""]));
    if (kind === "trend") data.date = today();
    setEditor({ id: newId(), kind, data: { ...data, ...preset }, revision: 0 });
  }
  async function save(entry: Entry) {
    await store.save(entry);
    setEditor(null);
    setMessage("Registro guardado.");
  }
  async function copy(value: string) {
    try { await navigator.clipboard.writeText(value); setMessage("Texto copiado."); }
    catch { setMessage("Selecciona el texto de la plantilla y cópialo manualmente."); }
  }

  const toolbar = (stateOptions: readonly string[], forPieces: boolean, objectiveFilter = forPieces) => {
    const selects = [
      { key: "account", placeholder: "Todas las cuentas", options: accounts },
      ...(forPieces ? [{ key: "permit", placeholder: "Todos los permisos", options: permits }] : []),
      ...(stateOptions.length ? [{ key: "status", placeholder: "Todos los estados", options: stateOptions }] : []),
      ...(objectiveFilter ? [{ key: "objective", placeholder: "Todos los objetivos", options: objectives }] : []),
    ] as const;
    return <div className="filters">
      <label className="search"><Search size={16} /><input placeholder="Buscar registros…" aria-label="Buscar registros" value={filters.q} onChange={(e) => setFilters({ ...filters, q: e.target.value })} /></label>
      {selects.map(({ key, placeholder, options }) => <select aria-label={placeholder} key={key} value={filters[key as keyof typeof filters]} onChange={(e) => setFilters({ ...filters, [key]: e.target.value })}>
        <option value="">{placeholder}</option>{options.map((value) => <option key={value}>{value}</option>)}
      </select>)}
    </div>;
  };

  const queue = pieces.filter(({ data }) => data.status === "Programado");
  const count = (kind: Kind) => store.entries.filter((entry) => entry.kind === kind).length;

  return <div className="shell">
    <aside className="sidebar" aria-label="Navegación principal">
      <button className="wordmark" onClick={() => navigate("home")} aria-label="CAPTOORA, vista general"><span className="logo"><Aperture size={21} /></span><span>CAPTOORA<small>ESTUDIO FOTOGRÁFICO</small></span></button>
      <div className="workspace"><span className="workspace-icon"><Camera size={15} /></span><span><strong>Farmasi</strong><small>31 OCT 2026</small></span><span className="online" /></div>
      {nav.map((group) => <section className="nav-group" key={group.label}><h2>{group.label}</h2>{group.links.map(({ key, label, icon: Icon }) => <button key={key} aria-current={view === key ? "page" : undefined} className={view === key ? "active" : ""} onClick={() => navigate(key)}><Icon size={16} /><span>{label}</span>{view === key && <span className="nav-mark" />}</button>)}</section>)}
      <div className="side-footer"><LockKeyhole size={14} /> Espacio privado <span>MTY</span></div>
    </aside>
    <main>
      <header className="topbar"><div><span>CAPTOORA</span><ChevronRight size={13} /><strong>Farmasi</strong></div><span className="private"><span /> Operación manual</span></header>
      <div className="content">
        {store.loadError && <div className="notice error" role="alert">{store.loadError} <button className="button secondary" onClick={() => void store.load()}>Reintentar</button></div>}
        {view === "home" ? <>
          <section className="hero">
            <div className="hero-art" aria-hidden="true"><Aperture strokeWidth={0.55} /><span>F/31</span></div>
            <div className="hero-copy"><p className="eyebrow"><span /> MESA DE PRODUCCIÓN <i /> MONTERREY, MX</p><h1>Farmasi<span>.</span></h1><p className="hero-sub">Del retrato a la reserva.</p><p className="hero-meta"><CalendarDays size={15} /> 31 de octubre de 2026 <span>·</span> Campaña CAPTOORA</p>
            <button className="button primary" onClick={() => navigate("selection")}><FolderOpen size={16} /> Abrir selección <ArrowRight size={16} /></button></div>
          </section>
          <div className="stats">
            <Stat icon={<Camera size={18} />} label="Inventario ARW" value="2,738" detail="Originales del lote inicial" />
            <Stat icon={<FileImage size={18} />} label="Inventario JPG" value="2,738" detail="Selección personal pendiente" />
            <Stat icon={<ShieldCheck size={18} />} label="Piezas aprobadas" value={store.loading ? "…" : pieces.filter(({ data }) => data.status === "Aprobado").length} detail="Listas para programar" />
            <Stat icon={<CalendarDays size={18} />} label="Cola editorial" value={store.loading ? "…" : queue.length} detail={queue.length ? "Programadas manualmente" : "Sin piezas programadas"} />
          </div>
          <div className="home-grid">
            <section className="panel">
              <div className="panel-head"><div className="panel-symbol"><ListChecks size={19} /></div><div><h2>Pipeline editorial</h2><p>Del archivo seleccionado al enlace publicado</p></div><button className="icon-button panel-action" onClick={() => navigate("approval")} aria-label="Abrir revisión"><ArrowUpRight size={19} /></button></div>
              <div className="pipeline">{stages.map((status, index) => <button key={status} onClick={() => { navigate("approval"); setFilters((old) => ({ ...old, status })); }}><span className={`step s${index}`}>0{index + 1}</span><span>{status}</span><strong>{store.loading ? "…" : pieces.filter(({ data }) => data.status === status).length}</strong><ChevronRight size={14} /></button>)}</div>
            </section>
            <section className="panel">
              <div className="panel-head"><div className="panel-symbol"><Link2 size={18} /></div><div><h2>Canales y restricciones</h2><p>Configuración de partida</p></div></div>
              <div className="system-rows">
                <div><strong>Metricool</strong><Badge tone="good">Solo TikTok</Badge><p>@captoora.mty · cola inicial vacía</p></div>
                <div><strong>Instagram y Facebook</strong><Badge tone="warm">Por verificar</Badge><p>Fuera de la conexión de Metricool</p></div>
                <div><strong>Flujos n8n</strong><Badge>Inactivos</Badge><p>Pendientes IDs, credenciales y verificación de cuentas.</p></div>
              </div>
            </section>
          </div>
          <section className="panel quick"><div className="panel-head"><div className="panel-symbol"><MessageCircle size={18} /></div><div><h2>Conversaciones y ventas</h2><p>Seguimiento del contenido después de la sesión</p></div></div><div className="quick-links">
            {([[ "mentions", "Menciones", count("mention") ], [ "thanks", "Agradecimientos", count("thanks") ], [ "highlights", "Experiencias", count("highlight") ], [ "leads", "Consultas y reservas", count("lead") ]] as const).map(([key, title, number]) => <button key={key} onClick={() => navigate(key)}>{title}<strong>{number}</strong><ArrowUpRight size={15} /></button>)}
          </div></section>
        </> : <>
          <div className="page-head"><div><p className="eyebrow"><span />{meta[0]}</p><h1>{meta[1]}</h1><p>{meta[2]}</p></div>
            <div className="actions">{view === "selection" && <button className="button secondary" onClick={() => setPicking(true)}><FolderOpen size={16} /> Revisar archivos</button>}
              {["selection", "approval", "calendar"].includes(view) && <button className="button primary" onClick={() => create("piece")}><Plus size={17} /> Nueva pieza</button>}
              {kind && <button className="button primary" onClick={() => create(kind)}><Plus size={17} /> {tracker[kind].action}</button>}</div>
          </div>
          {view === "selection" && <div className="notice"><FolderOpen size={17} /><span><strong>Lote inicial: 2,738 ARW y 2,738 JPG.</strong> Abre tus archivos locales para elegir los que quieres registrar. Conserva los ARW como originales.</span></div>}
          {view === "approval" && <div className="notice"><ShieldCheck size={17} /><span>Para aprobar se requiere selección personal, constancia de permiso, archivo final y revisión de imagen, marca y cuenta.</span></div>}
          {view === "calendar" && <div className="notice"><CalendarDays size={17} /><span>La cola empezó vacía. Aquí registras fechas acordadas y enlaces reales después de publicar manualmente.</span></div>}
          {view === "highlights" && <div className="notice"><Star size={17} /><span>Para marcar una historia como lista o añadida, vincula una pieza aprobada con permiso de uso público.</span></div>}
          {["selection", "approval", "calendar"].includes(view) && toolbar(stages, true)}
          {view === "calendar" && <Calendar pieces={visiblePieces.filter(({ data }) => stages.indexOf(data.status as typeof stages[number]) >= 3)} edit={setEditor} />}
          {(view === "selection" || view === "approval") && <section className="panel"><div className="section-label"><h2>{view === "selection" ? "Material registrado" : "Piezas editoriales"}</h2><Badge>{visiblePieces.length} de {pieces.length}</Badge></div>
            {visiblePieces.length ? <PieceTable entries={visiblePieces} edit={setEditor} /> : <Blank title={store.loading ? "Cargando registros…" : pieces.length ? "Sin coincidencias" : "Aún no hay piezas registradas"} detail={pieces.length ? "Prueba con otros filtros." : "Añade una ficha por foto o pieza. El permiso empieza pendiente."} action={!pieces.length && !store.loading && <button className="button secondary" onClick={() => create("piece")}><Plus size={16} /> Nueva pieza</button>} />}
          </section>}
          {kind === "template" && <div className="template-grid">{templates.map((template, index) => <article className="panel template" key={index}><span className="panel-symbol"><ClipboardList size={18} /></span><small>{template.category || "Caption"}</small><h2>{template.title}</h2><p>{template.body}</p><div className="actions"><button className="button secondary" onClick={() => void copy(template.body)}><Copy size={15} /> Copiar</button><button className="button secondary" onClick={() => index < defaultTemplates.length ? create("template", template) : setEditor(store.entries.filter((entry) => entry.kind === "template")[index - defaultTemplates.length])}>{index < defaultTemplates.length ? "Personalizar" : "Editar"}</button></div></article>)}</div>}
          {kind && kind !== "template" && (() => {
            const all = store.entries.filter((entry) => entry.kind === kind);
            const items = all.filter(matches).filter(({ data }) => leadMode !== "Reservas" || ["Reservada", "Realizada"].includes(data.status));
            return <>
              {kind === "lead" && <div className="stats leads-stats"><Stat icon={<MessageCircle size={18} />} label="Consultas registradas" value={all.length} /><Stat icon={<CalendarDays size={18} />} label="Reservas y realizadas" value={all.filter(({ data }) => ["Reservada", "Realizada"].includes(data.status)).length} /><Stat icon={<CheckCircle2 size={18} />} label="Cobros confirmados" value={money(all.reduce((sum, { data }) => sum + (Number(data.paid) || 0), 0))} detail="MXN" /></div>}
              {toolbar(tracker[kind].fields.find(({ key }) => key === "status")?.options || [], false, kind === "trend")}
              <section className="panel">
                <div className="section-label">{kind === "lead" ? <div className="segmented">{["Todas", "Reservas"].map((value) => <button key={value} aria-pressed={leadMode === value} onClick={() => setLeadMode(value)}>{value}</button>)}</div> : <h2>{items.length} registros</h2>}{kind === "lead" && <Badge>{items.length}</Badge>}</div>
                {items.length ? <div className="records">{items.map((entry) => {
                  const d = entry.data;
                  const expired = kind === "mention" && d.date && d.date < new Intl.DateTimeFormat("sv-SE", { timeZone: "America/Monterrey", dateStyle: "short", timeStyle: "short" }).format(new Date()).replace(" ", "T") && ["Por revisar", "Vigente"].includes(d.status);
                  const related = store.entries.find(({ id }) => id === (d.pieceId || d.mentionId));
                  return <button className="record" key={entry.id} onClick={() => setEditor(entry)}><span><strong>{d.title}</strong><small>{[d.account || d.platform, d.participant || d.type || d.service, related?.data.title].filter(Boolean).join(" · ") || "Sin referencia adicional"}</small></span><span className="record-date">{dayLabel(d.bookingDate || d.date)}</span><Badge tone={expired ? "bad" : statusTone(d.status)}>{expired ? "Vigencia vencida" : d.status}</Badge><ChevronRight size={16} /></button>;
                })}</div> : <Blank title={store.loading ? "Cargando registros…" : all.length ? "Sin coincidencias" : tracker[kind].empty} detail={all.length ? "Ajusta los filtros para ver más registros." : "Los registros que agregues aparecerán aquí."} action={!all.length && !store.loading && <button className="button secondary" onClick={() => create(kind)}><Plus size={16} /> {tracker[kind].action}</button>} />}
              </section>
            </>;
          })()}
          <button className="back-link" onClick={() => navigate("home")}><ArrowLeft size={15} /> Volver a vista general</button>
        </>}
        <footer className="main-footer"><span>CAPTOORA / FARMASI</span><span>MONTERREY, NUEVO LEÓN · 2026</span></footer>
      </div>
    </main>
    {editor && <Editor key={editor.id} entry={editor} entries={store.entries} templates={templates} close={() => setEditor(null)} save={save} />}
    {picking && <FilePicker existing={pieces} close={() => setPicking(false)} save={store.save} onDone={(total) => { setPicking(false); setMessage(`${total} fichas registradas.`); }} />}
    {message && <div className="toast" role="status"><Check size={17} /> {message}<button className="icon-button" aria-label="Cerrar aviso" onClick={() => setMessage("")}><X size={15} /></button></div>}
  </div>;
}

function Stat({ icon, label, value, detail }: { icon: ReactNode; label: string; value: string | number; detail?: string }) {
  return <article className="stat"><div>{label}<span>{icon}</span></div><strong>{value}</strong>{detail && <p>{detail}</p>}</article>;
}

function PieceTable({ entries, edit }: { entries: Entry[]; edit: (entry: Entry) => void }) {
  return <div className="table-scroll"><table><thead><tr><th>Pieza / participante</th><th>Permiso</th><th>Formato / cuenta</th><th>Objetivo</th><th>Estado</th><th><span className="sr-only">Acciones</span></th></tr></thead><tbody>{entries.map((entry) => {
    const d = entry.data;
    return <tr key={entry.id}><td><button className="row-title" onClick={() => edit(entry)}>{d.title}</button><small>{d.participant || "Sin participante asignado"}</small></td><td><Badge tone={statusTone(d.uso_publico_autorizado)}>{d.uso_publico_autorizado}</Badge></td><td>{d.format}<small>{d.account || "Cuenta pendiente"}</small></td><td>{d.objective}</td><td><Badge tone={statusTone(d.status)}>{d.status}</Badge></td><td><button className="icon-button" aria-label={`Editar ${d.title}`} onClick={() => edit(entry)}><ArrowUpRight size={16} /></button></td></tr>;
  })}</tbody></table></div>;
}

function Calendar({ pieces, edit }: { pieces: Entry[]; edit: (entry: Entry) => void }) {
  const [month, setMonth] = useState(() => new Date(`${today().slice(0, 7)}-01T12:00:00`));
  const [selected, setSelected] = useState("");
  const year = month.getFullYear(), m = month.getMonth();
  const monthKey = `${year}-${String(m + 1).padStart(2, "0")}`;
  const pad = (month.getDay() + 6) % 7;
  const days = new Date(year, m + 1, 0).getDate();
  const shown = pieces.filter(({ data }) => data.date.startsWith(selected || monthKey)).sort((a, b) => a.data.date.localeCompare(b.data.date));
  const shift = (offset: number) => { setMonth(new Date(year, m + offset, 1, 12)); setSelected(""); };
  return <div className="calendar-layout"><section className="panel calendar">
    <div className="section-label"><h2>{new Intl.DateTimeFormat("es-MX", { year: "numeric", month: "long" }).format(month)}</h2><div className="actions"><button className="icon-button" aria-label="Mes anterior" onClick={() => shift(-1)}><ChevronLeft size={18} /></button><button className="icon-button" aria-label="Mes siguiente" onClick={() => shift(1)}><ChevronRight size={18} /></button></div></div>
    <div className="calendar-grid">
      {["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"].map((day) => <span className="weekday" key={day}>{day}</span>)}
      {Array.from({ length: pad }, (_, index) => <span key={`pad-${index}`} />)}
      {Array.from({ length: days }, (_, index) => {
        const date = `${monthKey}-${String(index + 1).padStart(2, "0")}`;
        const count = pieces.filter(({ data }) => data.date.startsWith(date)).length;
        return <button key={date} aria-label={`${date}, ${count} piezas`} aria-pressed={selected === date} className={date === today() ? "today" : ""} onClick={() => setSelected(selected === date ? "" : date)}>{index + 1}{count > 0 && <span>{count}</span>}</button>;
      })}
    </div>
  </section><section className="panel calendar-agenda"><div className="section-label"><h2>{selected ? dayLabel(selected) : "Agenda del mes"}</h2><Badge>{shown.length}</Badge></div>
    {shown.length ? <div className="records">{shown.map((entry) => <button className="record" key={entry.id} onClick={() => edit(entry)}><span><strong>{entry.data.title}</strong><small>{dayLabel(entry.data.date)} · {entry.data.account}</small></span><Badge tone={statusTone(entry.data.status)}>{entry.data.status}</Badge></button>)}</div> : <Blank icon={<CalendarDays size={23} />} title="Sin publicaciones en la agenda" detail="Las piezas programadas y publicadas aparecen aquí por fecha." />}
  </section></div>;
}

export default Dashboard;

function Modal({ title, subtitle, close, children }: { title: string; subtitle: string; close: () => void; children: ReactNode }) {
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => { dialog.current?.showModal(); }, []);
  return <dialog ref={dialog} aria-labelledby="dialog-title" onCancel={(event) => { event.preventDefault(); close(); }}>
    <div className="modal-head"><div><p className="eyebrow"><span />{subtitle}</p><h2 id="dialog-title">{title}</h2></div><button className="icon-button" aria-label="Cerrar" onClick={close}><X size={21} /></button></div>{children}
  </dialog>;
}

const pieceFields: Field[] = [
  { key: "title", label: "Nombre de la pieza", required: true },
  { key: "participant", label: "Participantes", hint: "Incluye a todas las personas visibles" },
  { key: "uso_publico_autorizado", label: "Permiso de uso público", options: permits },
  { key: "evidence", label: "Constancia del permiso", hint: "Folio, enlace o referencia fechada" },
  { key: "selection", label: "Selección personal", options: ["Por revisar", "Seleccionada", "Descartada"] },
  { key: "format", label: "Formato", options: formats },
  { key: "source", label: "Fuente", hint: "Ej. sesión Farmasi, Aftershoot o mención de IG" },
  { key: "original", label: "Ruta o nombre del original ARW/JPG" },
  { ...accountField, label: "Cuenta de destino" },
  { key: "objective", label: "Objetivo", options: objectives },
  { key: "cta", label: "Llamado a la acción (CTA)", hint: "Ej. enviar «SESIÓN» por DM" },
  { key: "finalUrl", label: "Enlace al archivo final", type: "url", hint: "Alternativa al archivo privado adjunto" },
];

function Editor({ entry, entries, templates, close, save }: {
  entry: Entry; entries: Entry[]; templates: typeof defaultTemplates; close: () => void; save: (entry: Entry) => Promise<void>;
}) {
  const [data, setData] = useState(entry.data);
  const [file, setFile] = useState<File | null>(null);
  const uploaded = useRef<{ file: File; key: string } | null>(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const piece = entry.kind === "piece";
  const stage = piece ? stages.indexOf(entry.data.status as typeof stages[number]) : -1;
  const title = piece ? (entry.revision ? "Ficha editorial" : "Nueva pieza") : tracker[entry.kind as Exclude<Kind, "piece">].name;
  const set = (key: string, value: string) => setData((current) => ({ ...current, [key]: value }));

  function field({ key, label, type, options, hint, required }: Field) {
    const props = { value: data[key] || "", required, disabled: saving, onChange: (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => set(key, event.target.value) };
    const linked = type === "piece" || type === "mention";
    return <label className={type === "textarea" ? "wide" : ""} key={key}>{label}{required && <span className="required"> *</span>}
      {options ? <select {...props}>{options.map((option) => <option key={option}>{option}</option>)}</select>
        : linked ? <select {...props}><option value="">Sin vínculo</option>{entries.filter((item) => item.kind === type).map((item) => <option key={item.id} value={item.id}>{item.data.title}</option>)}</select>
        : type === "textarea" ? <textarea {...props} rows={3} placeholder={hint} />
        : <input {...props} type={type || "text"} placeholder={hint} {...(type === "number" ? { min: 0, step: ".01" } : {})} />}
    </label>;
  }

  async function commit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (saving) return;
    const submitter = (event.nativeEvent as SubmitEvent).submitter as HTMLButtonElement | null;
    const next: Values = { ...data, ...(submitter?.value ? { status: submitter.value } : {}) };
    if (piece && stage >= 2 && next.status === stages[1]) {
      next.imageCheck = next.brandCheck = next.accountCheck = "";
    }
    const mediaKey = file ? (uploaded.current?.file === file ? uploaded.current.key : newId()) : next.mediaKey;
    if (file) next.mediaKey = mediaKey;
    const problem = validateEntry(entry.kind, next, entry.revision ? entry.data : undefined);
    if (problem) { setError(problem); return; }
    setError("");
    setSaving(true);
    try {
      if (file && uploaded.current?.key !== mediaKey) {
        const res = await fetch(`/api/media/${mediaKey}`, { method: "PUT", headers: { "Content-Type": file.type }, body: file });
        if (!res.ok) throw Error("No se pudo adjuntar el archivo. Usa JPG, PNG, WebP, MP4 o WebM de hasta 25 MB, o registra un enlace.");
        uploaded.current = { file, key: mediaKey };
      }
      await save({ ...entry, data: next });
    } catch (error) { setError(error instanceof Error ? error.message : "No se pudo guardar."); }
    finally { setSaving(false); }
  }

  const nextAction = ["Enviar a revisión", "Aprobar", "Registrar programación", "Registrar publicación"][stage];
  const captionTools = (key: string) => <label className="wide template-tool"><span><Sparkles size={15} /> Aplicar plantilla</span><select value="" disabled={saving} onChange={(event) => { if (event.target.value !== "") set(key, templates[Number(event.target.value)].body); }}><option value="">Elegir plantilla de texto…</option>{templates.map(({ title }, i) => <option key={i} value={i}>{title}</option>)}</select></label>;

  return <Modal title={title} subtitle={piece ? "Producción · Farmasi" : "Registro · Farmasi"} close={() => { if (!saving) close(); }}>
    <form onSubmit={commit}>
      <div className="modal-body">
        {piece ? <>
          <div className="editor-status"><Badge tone={statusTone(entry.data.status)}>{entry.data.status}</Badge><code>uso_publico_autorizado</code></div>
          <div className="field-grid">{pieceFields.map(field)}
            <label className="wide upload-field"><span><ImagePlus size={16} /> Archivo final privado</span><input type="file" accept="image/jpeg,image/png,image/webp,video/mp4,video/webm" disabled={saving} onChange={(event) => setFile(event.target.files?.[0] || null)} /><small>Hasta 25 MB. Para archivos más grandes usa el enlace.</small></label>
            {entry.data.mediaKey && <a className="wide inline-link" href={`/api/media/${entry.data.mediaKey}`} target="_blank" rel="noreferrer">Abrir archivo adjunto <ArrowUpRight size={14} /></a>}
            {!entry.data.mediaKey && isWebLink(data.finalUrl) && <a className="wide inline-link" href={data.finalUrl} target="_blank" rel="noreferrer">Abrir enlace final <ArrowUpRight size={14} /></a>}
            {captionTools("caption")}
            {field({ key: "caption", label: "Caption / copy", type: "textarea" })}
          </div>
          <div className="review-box"><h3><ShieldCheck size={17} /> Revisión manual</h3>
            {[["imageCheck", "Imagen y personas revisadas"], ["brandCheck", "Marca, texto y créditos revisados"], ["accountCheck", "Cuenta de destino verificada"]].map(([key, label]) =>
              <label key={key} className="check"><input type="checkbox" disabled={saving} checked={data[key] === "Sí"} onChange={(event) => set(key, event.target.checked ? "Sí" : "")} /> {label}</label>)}
          </div>
          <div className="field-grid">
            {field({ key: "date", label: "Fecha editorial (Monterrey)", type: "datetime-local" })}
            {field({ key: "postUrl", label: "URL de la publicación real", type: "url" })}
            {isWebLink(data.postUrl) && <a className="wide inline-link" href={data.postUrl} target="_blank" rel="noreferrer">Abrir publicación <ArrowUpRight size={14} /></a>}
            {field({ key: "notes", label: "Notas de producción", type: "textarea" })}
          </div>
        </> : <div className="field-grid">
          {entry.kind === "thanks" && captionTools("body")}
          {tracker[entry.kind as Exclude<Kind, "piece">].fields.map(field)}
          {isWebLink(data.url) && <a className="wide inline-link" href={data.url} target="_blank" rel="noreferrer">Abrir enlace <ArrowUpRight size={14} /></a>}
        </div>}
        {error && <p className="notice error" role="alert">{error}</p>}
      </div>
      <div className="modal-foot">
        {piece && stage >= 2 && <button className="button secondary" disabled={saving} value={stages[1]} type="submit">Reabrir revisión</button>}
        <button className={nextAction ? "button secondary" : "button primary"} disabled={saving} type="submit">{saving ? "Guardando…" : "Guardar"}</button>
        {nextAction && entry.revision > 0 && <button className="button primary" disabled={saving} value={stages[stage + 1]} type="submit">{nextAction} <ArrowRight size={16} /></button>}
      </div>
    </form>
  </Modal>;
}

function FileTile({ file, checked, disabled, toggle }: { file: File; checked: boolean; disabled: boolean; toggle: () => void }) {
  const [preview, setPreview] = useState("");
  useEffect(() => {
    if (!/\.(jpg|jpeg|png|webp)$/i.test(file.name)) return;
    const url = URL.createObjectURL(file);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);
  return <label className="file-tile">{preview ? <img src={preview} alt="" /> : <span className="raw-icon"><FileImage size={27} /></span>}<span><input type="checkbox" checked={checked} disabled={disabled} onChange={toggle} /> {file.name}</span></label>;
}

const fileRef = (file: File) => `${file.name} · ${file.size} bytes · ${file.lastModified}`;

function FilePicker({ existing, close, save, onDone }: {
  existing: Entry[]; close: () => void; save: (entry: Entry) => Promise<void>; onDone: (total: number) => void;
}) {
  const [files, setFiles] = useState<File[]>([]);
  const [picked, setPicked] = useState(new Set<string>());
  const [processed, setProcessed] = useState(0);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [page, setPage] = useState(0);
  const [filter, setFilter] = useState("");
  const known = new Set(existing.map(({ data }) => data.localRef));
  const candidates = files.filter((file) => file.name.toLowerCase().includes(filter.trim().toLowerCase()));
  const pageSize = 24;
  async function register() {
    setSaving(true);
    setError("");
    let completed = processed;
    try {
      for (const file of files.filter((file) => picked.has(fileRef(file)) && !known.has(fileRef(file)))) {
        const key = fileRef(file);
        const data = { ...emptyPiece, title: file.name, original: file.name, source: "Selección local · Farmasi 31 OCT", selection: "Seleccionada", localRef: key };
        const id = crypto.subtle
          ? formatId(new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(key))))
          : newId();
        await save({ id, kind: "piece", data, revision: 0 });
        completed++;
        setProcessed(completed);
        setPicked((old) => { const next = new Set(old); next.delete(key); return next; });
      }
      onDone(completed);
    } catch (error) { setError(error instanceof Error ? error.message : "No se pudieron registrar todos los archivos."); }
    finally { setSaving(false); }
  }
  return <Modal title="Revisar archivos locales" subtitle="Selección personal" close={() => { if (!saving) close(); }}>
    <div className="modal-body">
      <p className="muted">Puedes abrir JPG y ARW. Las vistas previas se muestran en este dispositivo. El registro conserva las referencias de los archivos que elijas.</p>
      <input className="file-input" type="file" multiple accept=".arw,.jpg,.jpeg,.png,.webp" disabled={saving} onChange={(event) => {
        setFiles([...new Map(Array.from(event.target.files || []).map((file) => [fileRef(file), file])).values()]); setPicked(new Set()); setPage(0); setFilter(""); setError("");
      }} />
      {!!files.length && <><label className="search"><Search size={16} /><input placeholder="Filtrar por nombre…" aria-label="Filtrar archivos" value={filter} onChange={(event) => { setFilter(event.target.value); setPage(0); }} /></label>
        <div className="file-grid">{candidates.slice(page * pageSize, (page + 1) * pageSize).map((file) => {
          const key = fileRef(file);
          return <FileTile key={key} file={file} checked={picked.has(key) || known.has(key)} disabled={saving || known.has(key)} toggle={() => setPicked((old) => { const next = new Set(old); if (next.has(key)) next.delete(key); else next.add(key); return next; })} />;
        })}</div>
        <div className="file-pagination"><span>{candidates.length} archivos · {picked.size} elegidos</span><button className="icon-button" aria-label="Página anterior" disabled={!page} onClick={() => setPage(page - 1)}><ChevronLeft size={18} /></button><button className="icon-button" aria-label="Página siguiente" disabled={(page + 1) * pageSize >= candidates.length} onClick={() => setPage(page + 1)}><ChevronRight size={18} /></button></div>
      </>}
      {error && <p className="notice error" role="alert">{error}</p>}
    </div>
    <div className="modal-foot"><button className="button secondary" disabled={saving} onClick={close}>Cerrar</button><button className="button primary" disabled={saving || !picked.size} onClick={() => void register()}>{saving ? `Guardando… (${processed})` : `Registrar selección (${picked.size})`}</button></div>
  </Modal>;
}
