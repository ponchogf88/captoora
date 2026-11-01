import Zdog from "zdog";
import fx from "glfx";
import { VFX } from "@vfx-js/core";

const SHEEN = `
precision highp float;
uniform vec2 resolution;
uniform vec2 offset;
uniform float time;
uniform sampler2D src;
out vec4 outColor;

void main() {
  vec2 uv = (gl_FragCoord.xy - offset) / resolution;
  vec4 col = texture(src, uv);
  float breath = 0.45 + 0.55 * (0.5 + 0.5 * sin(time * 2.1));
  outColor = vec4(col.rgb, col.a * breath);
}
`;

const reducedQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

const state = {
  stack: ["zdog", "glfx", "@vfx-js/core"],
  zdog: false,
  glfx: false,
  vfx: false,
  reduced: reducedQuery.matches,
  paused: reducedQuery.matches,
  grade: "foto directa",
};
window.__CAPTOORA_MOTION__ = state;

const lente = document.querySelector("#lente");
const marco = document.querySelector("#marco");
const retrato = document.querySelector("#retrato");
const placa = document.querySelector("#placa");
const pausa = document.querySelector("#pausa");
const estado = document.querySelector("#estado");
const lectura = document.querySelector("#lectura");

let illo = null;
let iris = null;
let dragging = false;
let gradeCanvas = null;
let gradeTexture = null;
let vfx = null;
let raf = 0;
let lastGrade = 0;
let lastFrame = 0;
const muestras = [];
let ultimaViñeta = null;
const arranque = performance.now();

function decir(texto) {
  if (estado) estado.textContent = texto;
}

function pintarLectura(vignette) {
  if (!lectura) return;
  const zdogTxt = state.zdog ? (state.paused ? "quieto" : "girando") : "no arrancó";
  const glfxTxt = state.glfx ? state.grade : "foto directa";
  const vfxTxt = state.vfx ? (state.paused ? "en pausa" : "latido") : "HTML plano";
  const viñeta = typeof vignette === "number" ? vignette.toFixed(2) : "—";
  lectura.textContent = `Zdog: ${zdogTxt}. glfx.js: ${glfxTxt}, viñeta ${viñeta}. VFX-JS: ${vfxTxt}.`;
}

function crearLente() {
  illo = new Zdog.Illustration({
    element: lente,
    zoom: 1.05,
    dragRotate: true,
    resize: true,
    onDragStart() {
      dragging = true;
    },
    onDragEnd() {
      dragging = false;
    },
  });

  new Zdog.Cylinder({
    addTo: illo,
    diameter: 118,
    length: 26,
    stroke: false,
    color: "#e6c56a",
    backface: "#6a5424",
  });

  new Zdog.Ellipse({
    addTo: illo,
    diameter: 132,
    stroke: 7,
    color: "#f0d78c",
    translate: { z: 14 },
  });

  iris = new Zdog.Group({ addTo: illo, translate: { z: 16 } });
  const pasos = 6;
  for (let i = 0; i < pasos; i += 1) {
    const ancla = new Zdog.Group({
      addTo: iris,
      rotate: { z: (Math.PI * 2 * i) / pasos },
    });
    new Zdog.RoundedRect({
      addTo: ancla,
      width: 54,
      height: 16,
      cornerRadius: 8,
      stroke: 3,
      fill: true,
      color: "#1a140c",
      translate: { x: 28 },
    });
  }

  new Zdog.Ellipse({
    addTo: illo,
    diameter: 34,
    stroke: 14,
    fill: true,
    color: "#070604",
    translate: { z: 20 },
  });

  new Zdog.Ellipse({
    addTo: illo,
    diameter: 8,
    stroke: 3,
    fill: true,
    color: "#fff6d8",
    translate: { x: -8, y: -8, z: 24 },
  });

  illo.rotate.x = 0.35;
  illo.rotate.y = -0.45;
  illo.updateRenderGraph();
  state.zdog = true;
}

function prepararGrado(img) {
  const maxAncho = 800;
  const escala = Math.min(1, maxAncho / img.naturalWidth);
  const ancho = Math.max(2, Math.round(img.naturalWidth * escala));
  const alto = Math.max(2, Math.round(img.naturalHeight * escala));
  const fuente = document.createElement("canvas");
  fuente.width = ancho;
  fuente.height = alto;
  const ctx = fuente.getContext("2d", { alpha: false });
  ctx.drawImage(img, 0, 0, ancho, alto);

  gradeCanvas = fx.canvas();
  gradeTexture = gradeCanvas.texture(fuente);
  gradeCanvas.className = "grado";
  gradeCanvas.setAttribute(
    "aria-label",
    "El mismo retrato, con viñeta y luz movidas por glfx.js. Sigue el encuadre completo."
  );
  gradeCanvas.style.width = "100%";
  gradeCanvas.style.height = "auto";
  aplicarGrado(0.45);
  const pieDeFoto = marco.querySelector("figcaption");
  marco.insertBefore(gradeCanvas, pieDeFoto);
  retrato.classList.add("retrato-base");
  retrato.setAttribute("aria-hidden", "true");
  state.glfx = true;
  state.grade = "WebGL1, textura " + ancho + "×" + alto;
}

function aplicarGrado(cantidad) {
  if (!gradeCanvas) return;
  const brillo = (cantidad - 0.5) * 0.1;
  try {
    gradeCanvas
      .draw(gradeTexture)
      .brightnessContrast(brillo, 0.06)
      .sepia(0.05)
      .vignette(0.35 + cantidad * 0.28, 0.25 + cantidad * 0.55)
      .update();
  } catch (error) {
    console.error(error);
    soltarRevelado("filtro CSS: el revelado WebGL se cayó");
    decir("El revelado WebGL se cayó. La foto sigue en pantalla, con un ajuste CSS.");
  }
}

function gradoCss() {
  retrato.classList.add("grado-css");
  state.grade = "filtro CSS, sin WebGL";
}

function glfxPerdido() {
  if (!gradeCanvas || !gradeCanvas._ || !gradeCanvas._.gl) return false;
  return gradeCanvas._.gl.isContextLost();
}

function soltarRevelado(motivo) {
  if (gradeCanvas) {
    gradeCanvas.remove();
    gradeCanvas = null;
    gradeTexture = null;
  }
  retrato.classList.remove("retrato-base");
  retrato.removeAttribute("aria-hidden");
  retrato.classList.add("grado-css");
  state.glfx = false;
  state.grade = motivo;
}

function soltarBarrido() {
  if (vfx) {
    try {
      vfx.destroy();
    } catch (error) {
      console.error(error);
    }
  }
  vfx = null;
  state.vfx = false;
  placa.style.opacity = "";
}

async function prepararBarrido() {
  if (state.vfx) return;
  const area = window.innerWidth * window.innerHeight;
  const pixelRatio = area > 2000000 ? 0.75 : 1;
  const antes = glfxPerdido();
  if (!vfx) {
    vfx = VFX.init({
      pixelRatio,
      scrollPadding: false,
      zIndex: 2,
      autoplay: false,
    });
  }
  if (!vfx) {
    decir("Este navegador no abrió WebGL2. La placa se queda en HTML. El diafragma y el retrato siguen.");
    return;
  }
  try {
    await vfx.add(placa, { shader: SHEEN, overflow: 0 });
  } catch (error) {
    soltarBarrido();
    if (glfxPerdido()) soltarRevelado("filtro CSS: WebGL se soltó al montar el barrido");
    const rect = placa.getBoundingClientRect();
    decir(
      "VFX-JS no compiló el barrido (" +
        Math.round(rect.width) +
        "×" +
        Math.round(rect.height) +
        ", glfx perdido antes: " +
        antes +
        "). La placa queda en HTML."
    );
    console.error(error);
    return;
  }
  if (glfxPerdido()) {
    soltarBarrido();
    soltarRevelado("filtro CSS: el barrido se llevó el contexto de la foto");
    decir("El barrido y el revelado WebGL no cupieron juntos. Quedan el diafragma y la foto con ajuste CSS.");
    return;
  }
  state.vfx = true;
  if (!state.paused) vfx.play();
}

function cuadro(now) {
  raf = 0;
  if (state.paused) return;

  const dt = lastFrame ? now - lastFrame : 16;
  lastFrame = now;
  if (now - arranque > 4000 && state.vfx) {
    muestras.push(dt);
    if (muestras.length > 45) muestras.shift();
    if (muestras.length === 45) {
      let suma = 0;
      for (let i = 0; i < muestras.length; i += 1) suma += muestras[i];
      if (suma / muestras.length > 90) {
        muestras.length = 0;
        soltarBarrido();
        decir("Se apagó el barrido de VFX-JS: el cuadro se quedó por debajo de unos 11 fps. Zdog y glfx.js siguen.");
      }
    }
  }

  const t = now / 1000;
  if (illo && iris && !dragging) {
    iris.rotate.z = t * 0.35;
    illo.rotate.y = Math.sin(t * 0.45) * 0.7;
    illo.rotate.x = 0.28 + Math.cos(t * 0.35) * 0.12;
  }
  if (illo) illo.updateRenderGraph();

  if (gradeCanvas && now - lastGrade > 40) {
    lastGrade = now;
    ultimaViñeta = 0.5 + 0.5 * Math.sin(t * 0.9);
    aplicarGrado(ultimaViñeta);
  }
  pintarLectura(ultimaViñeta);
  raf = window.requestAnimationFrame(cuadro);
}

function arrancar() {
  if (state.paused || raf) return;
  lastFrame = 0;
  raf = window.requestAnimationFrame(cuadro);
}

function detener() {
  if (raf) window.cancelAnimationFrame(raf);
  raf = 0;
  if (vfx && state.vfx) vfx.stop();
}

function sincronizarPausa() {
  state.paused = pausa.getAttribute("aria-pressed") === "true";
  if (state.paused) {
    detener();
    pausa.textContent = "Reanudar movimiento";
    decir(
      state.reduced
        ? "Movimiento reducido. El diafragma queda quieto, el retrato en un solo revelado y la placa sin barrido."
        : "Movimiento en pausa. El diafragma queda donde está y el retrato conserva el último revelado."
    );
  } else {
    if (vfx && state.vfx) vfx.play();
    pausa.textContent = "Pausar movimiento";
    decir("Movimiento activo. Puedes arrastrar el diafragma.");
    arrancar();
  }
  pintarLectura(ultimaViñeta);
}

async function iniciar() {
  try {
    crearLente();
  } catch (error) {
    decir("Zdog no pudo dibujar el diafragma en este navegador.");
    console.error(error);
  }

  const listo = new Promise((resolve) => {
    if (retrato.complete && retrato.naturalWidth) resolve();
    else {
      retrato.addEventListener("load", () => resolve(), { once: true });
      retrato.addEventListener("error", () => resolve(), { once: true });
    }
  });
  await listo;

  if (retrato.naturalWidth) {
    try {
      prepararGrado(retrato);
    } catch (error) {
      gradoCss();
      decir("WebGL no estuvo disponible para el revelado. El retrato se muestra con un ajuste CSS.");
      console.error(error);
    }
  }

  if (!state.paused) {
    try {
      await prepararBarrido();
    } catch (error) {
      state.vfx = false;
      placa.style.opacity = "";
      decir("VFX-JS no pudo montar el barrido. La placa queda en HTML.");
      console.error(error);
    }
  }

  pausa.hidden = false;
  pausa.setAttribute("aria-pressed", state.paused ? "true" : "false");
  pausa.textContent = state.paused ? "Reanudar movimiento" : "Pausar movimiento";
  pausa.addEventListener("click", () => {
    const estabaEnPausa = pausa.getAttribute("aria-pressed") === "true";
    pausa.setAttribute("aria-pressed", estabaEnPausa ? "false" : "true");
    const vaAMoverse = pausa.getAttribute("aria-pressed") === "false";
    if (vaAMoverse && !state.vfx) {
      prepararBarrido()
        .then(() => sincronizarPausa())
        .catch((error) => {
          state.vfx = false;
          placa.style.opacity = "";
          console.error(error);
          sincronizarPausa();
        });
      return;
    }
    sincronizarPausa();
  });

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) detener();
    else if (!state.paused) {
      if (vfx && state.vfx) vfx.play();
      arrancar();
    }
  });

  reducedQuery.addEventListener("change", () => {
    state.reduced = reducedQuery.matches;
    pausa.setAttribute("aria-pressed", state.reduced ? "true" : "false");
    sincronizarPausa();
  });

  if (state.paused) {
    if (illo) illo.updateRenderGraph();
    if (!estado.textContent) {
      decir("Movimiento reducido. Pulsa reanudar si quieres ver el diafragma, el revelado y el barrido.");
    }
  } else {
    if (state.zdog && state.glfx && state.vfx) {
      decir("Movimiento activo. Puedes arrastrar el diafragma.");
    }
    arrancar();
  }
  pintarLectura(state.glfx ? 0.5 : null);
}

iniciar();
