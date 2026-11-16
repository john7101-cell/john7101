import React from "react";
import { AbsoluteFill, Audio, OffthreadVideo, interpolate, staticFile, useCurrentFrame, Easing, delayRender, continueRender } from "remotion";

const FUENTES: [string, string, string, string][] = [
  ["Serif", "cormorant-garamond-latin-500-normal", "500", "normal"], ["Serif", "cormorant-garamond-latin-600-normal", "600", "normal"],
  ["Serif", "cormorant-garamond-latin-500-italic", "500", "italic"], ["Serif", "cormorant-garamond-latin-600-italic", "600", "italic"],
  ["Sans", "montserrat-latin-400-normal", "400", "normal"], ["Sans", "montserrat-latin-500-normal", "500", "normal"], ["Sans", "montserrat-latin-600-normal", "600", "normal"],
];
const espera = delayRender("fuentes");
Promise.all(FUENTES.map(([fam, file, weight, style]) => {
  const f = new FontFace(fam, `url(${staticFile(`fonts/${file}.woff2`)})`, { weight, style });
  return f.load().then((ff) => { (document.fonts as any).add(ff); });
})).then(() => continueRender(espera));

export const DUR = 93.1;
const ROSA = "#F6BCCB";
const fontCss = `
@font-face{font-family:Serif;src:url(${staticFile("fonts/cormorant-garamond-latin-500-normal.woff2")});font-weight:500}
@font-face{font-family:Serif;src:url(${staticFile("fonts/cormorant-garamond-latin-600-normal.woff2")});font-weight:600}
@font-face{font-family:Serif;src:url(${staticFile("fonts/cormorant-garamond-latin-500-italic.woff2")});font-weight:500;font-style:italic}
@font-face{font-family:Serif;src:url(${staticFile("fonts/cormorant-garamond-latin-600-italic.woff2")});font-weight:600;font-style:italic}
@font-face{font-family:Sans;src:url(${staticFile("fonts/montserrat-latin-400-normal.woff2")});font-weight:400}
@font-face{font-family:Sans;src:url(${staticFile("fonts/montserrat-latin-500-normal.woff2")});font-weight:500}
@font-face{font-family:Sans;src:url(${staticFile("fonts/montserrat-latin-600-normal.woff2")});font-weight:600}`;

// *texto* -> palabra clave en serif itálica rosa; "/" -> salto de línea
const Rich: React.FC<{ t: string; keySize: number }> = ({ t, keySize }) => (
  <>
    {t.split("/").map((line, li) => (
      <div key={li}>
        {line.trim().split(/(\*[^*]+\*)/).map((p, i) =>
          p.startsWith("*") ? (
            <span key={i} style={{ fontFamily: "Serif", fontStyle: "italic", fontWeight: 600, color: ROSA, fontSize: keySize, letterSpacing: 0 }}>
              {p.slice(1, -1)}
            </span>
          ) : (
            <span key={i}>{p}</span>
          )
        )}
      </div>
    ))}
  </>
);

const useFade = (s: number, e: number, inD = 0.35, outD = 0.3) => {
  const t = useCurrentFrame() / 30;
  const o = interpolate(t, [s, s + inD, e - outD, e], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const y = interpolate(t, [s, s + inD + 0.2], [14, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const blur = interpolate(t, [s, s + inD], [6, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return { o, y, blur, on: t >= s && t <= e };
};

type Cue = [number, number, string];
const SUBS: Cue[] = [
  [2.15, 3.9, "¿Trabajas, produces,"], [3.9, 5.2, "tomas *decisiones*,"], [5.2, 6.6, "eres *independiente*"],
  [6.6, 9.1, "y no necesitas que nadie / te *resuelva la vida?*"],
  [11.55, 14.9, "¿por qué terminas necesitando tanto / *que alguien te elija?*"],
  [15.0, 16.45, "Te ilusionas *rápido*,"], [16.45, 18.25, "te *entregas* incluso antes"], [18.25, 20.3, "de conocer profundamente / a esa persona."],
  [20.4, 22.35, "Justificas sus *ausencias*,"], [22.35, 24.0, "esperas sus *mensajes*,"], [24.0, 25.5, "analizas *cada palabra*,"],
  [25.5, 27.95, "perdonas cosas / *que te duelen*"], [27.95, 30.2, "y aunque sabes que / algo no está bien…"],
  [31.7, 33.4, "Y comienzas a preguntarte:"], [33.4, 36.25, "¿por qué siempre termino en / *relaciones que me lastiman?*"],
  [36.35, 38.8, "¿Por qué me cuesta tanto / *poner límites?*"], [38.85, 41.05, "¿Por qué termino *dando tanto*,"],
  [41.05, 42.25, "esperando tan poco"], [42.25, 44.9, "y olvidándome de lo que / *yo también necesito?*"],
  [47.8, 51.45, "Tal vez necesitas *comprender* / qué está pasando en tus *vínculos*"],
  [53.75, 56.1, "a reconocer tus / *necesidades afectivas*,"], [56.1, 58.7, "comprender tus patrones de / *dependencia emocional*,"],
  [58.7, 60.4, "*fortalecer tu identidad*"], [60.4, 62.25, "y aprender a construir relaciones"], [62.25, 64.6, "donde amar / *no signifique abandonarte*"],
  [75.1, 77.15, "Porque no se trata de / *dejar de amar*,"], [77.15, 79.45, "ni de convertirte en una mujer / *fría o distante*"],
  [79.5, 81.9, "Se trata de aprender a / *amar sin perderte*,"], [81.9, 83.6, "de reconocer *lo que mereces*"],
  [83.6, 85.3, "y de no volver a *abandonarte*"], [85.3, 87.0, "por miedo a que alguien se vaya."],
];

const Sub: React.FC<{ c: Cue }> = ({ c }) => {
  const f = useFade(c[0], c[1], 0.22, 0.18);
  if (!f.on) return null;
  return (
    <div style={{ position: "absolute", left: 70, right: 70, top: 1330, textAlign: "center", opacity: f.o, transform: `translateY(${f.y}px)`,
      fontFamily: "Sans", fontWeight: 500, fontSize: 54, lineHeight: 1.28, color: "#fff", letterSpacing: 0.3,
      textShadow: "0 2px 18px rgba(0,0,0,.75), 0 0 2px rgba(0,0,0,.6)" }}>
      <Rich t={c[2]} keySize={68} />
    </div>
  );
};

type Title = { s: number; e: number; t: string; label?: string; top?: number; size?: number };
const TITLES: Title[] = [
  { s: 0.05, e: 2.15, t: "¿Eres una mujer que / *puede con todo?*" },
  { s: 9.3, e: 11.5, t: "Pero… cuando / *te enamoras*" },
  { s: 30.25, e: 31.7, t: "*te cuesta soltar*", size: 120 },
  { s: 45.15, e: 47.75, t: "Tal vez no necesitas / ser *más fuerte*" },
  { s: 64.75, e: 67.75, t: "tienes una / *cita contigo*", label: "5 DE DICIEMBRE" },
  { s: 87.1, e: 89.2, t: "Esta vez, / *vuelve a ti.*", size: 112 },
];
const Halo: React.FC<{ o: number; top: number }> = ({ o, top }) => (
  <div style={{ position: "absolute", left: -200, right: -200, top: top - 260, height: 760, opacity: o * 0.85,
    background: "radial-gradient(ellipse at center, rgba(14,5,10,.72) 0%, rgba(14,5,10,.35) 45%, rgba(14,5,10,0) 70%)" }} />
);
const TitleView: React.FC<{ x: Title }> = ({ x }) => {
  const f = useFade(x.s, x.e, 0.5, 0.35);
  if (!f.on) return null;
  return (
    <>
    <Halo o={f.o} top={(x.top ?? 470) + 60} />
    <div style={{ position: "absolute", left: 60, right: 60, top: x.top ?? 470, textAlign: "center", opacity: f.o, transform: `translateY(${f.y}px)`, filter: `blur(${f.blur}px)` }}>
      {x.label && <div style={{ fontFamily: "Sans", fontWeight: 600, fontSize: 30, letterSpacing: 10, color: ROSA, marginBottom: 22, textShadow: "0 2px 12px rgba(0,0,0,.6)" }}>{x.label}</div>}
      <div style={{ fontFamily: "Serif", fontWeight: 500, fontSize: x.size ?? 96, lineHeight: 1.02, color: "#fff", textShadow: "0 4px 30px rgba(0,0,0,.65)" }}>
        <Rich t={x.t} keySize={(x.size ?? 96) * 1.12} />
      </div>
    </div>
    </>
  );
};

const Brand: React.FC = () => {
  const f = useFade(52.1, 56.0, 0.8, 0.5);
  const t = useCurrentFrame() / 30;
  if (!f.on) return null;
  const ls = interpolate(t, [52.1, 56], [26, 16], { extrapolateRight: "clamp" });
  const line = interpolate(t, [52.4, 53.4], [0, 260], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  return (
    <>
    <Halo o={f.o} top={540} />
    <div style={{ position: "absolute", left: 0, right: 0, top: 480, textAlign: "center", opacity: f.o, filter: `blur(${f.blur}px)`, color: "#fff", textShadow: "0 4px 30px rgba(0,0,0,.6)" }}>
      <div style={{ fontFamily: "Serif", fontWeight: 500, fontSize: 118, letterSpacing: ls, paddingLeft: ls }}>VOLVER A MÍ</div>
      <div style={{ height: 2, width: line, background: ROSA, margin: "18px auto 22px" }} />
      <div style={{ fontFamily: "Serif", fontStyle: "italic", fontSize: 54, color: ROSA }}>un encuentro para volver a ti</div>
    </div>
    </>
  );
};

const Info: React.FC = () => {
  const a = useFade(67.85, 75.0, 0.5, 0.35);
  const b = useFade(69.0, 75.0, 0.5, 0.35);
  const c = useFade(70.8, 75.0, 0.5, 0.35);
  const d = useFade(72.8, 75.0, 0.4, 0.35);
  if (!a.on) return null;
  const sh = "0 3px 20px rgba(0,0,0,.7)";
  return (
    <>
      <div style={{ position: "absolute", left: 0, right: 0, top: 300, textAlign: "center", color: "#fff", textShadow: sh }}>
        <div style={{ opacity: a.o, transform: `translateY(${a.y}px)`, fontFamily: "Sans", fontWeight: 600, fontSize: 30, letterSpacing: 10, color: ROSA }}>VEN A</div>
        <div style={{ opacity: a.o, transform: `translateY(${a.y}px)`, fontFamily: "Serif", fontSize: 104, letterSpacing: 12, marginTop: 8 }}>VOLVER A MÍ</div>
        <div style={{ opacity: c.o, transform: `translateY(${c.y}px)`, fontFamily: "Sans", fontWeight: 500, fontSize: 40, letterSpacing: 3, marginTop: 18 }}>5 DE DICIEMBRE · 1:00 – 4:00 P. M.</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1310, textAlign: "center", color: "#fff", textShadow: sh }}>
        <div style={{ opacity: b.o, transform: `translateY(${b.y}px)`, fontFamily: "Serif", fontStyle: "italic", fontSize: 72 }}>The Ranch Hotel Boutique</div>
        <div style={{ opacity: b.o, transform: `translateY(${b.y}px)`, fontFamily: "Sans", fontWeight: 500, fontSize: 34, letterSpacing: 8, marginTop: 6, color: ROSA }}>SANTA ELENA</div>
        <div style={{ opacity: d.o, transform: `translateY(${d.y}px)`, display: "inline-block", marginTop: 46, padding: "16px 44px", border: `2px solid ${ROSA}`, borderRadius: 60,
          fontFamily: "Sans", fontWeight: 500, fontSize: 38, letterSpacing: 2, background: "rgba(20,8,14,.35)" }}>Inversión <b style={{ fontWeight: 600 }}>$130.000</b></div>
      </div>
    </>
  );
};

const EndCard: React.FC = () => {
  const t = useCurrentFrame() / 30;
  const g = interpolate(t, [88.6, 89.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const items = [
    { s: 89.2, el: <div style={{ fontFamily: "Serif", fontSize: 100, letterSpacing: 12, paddingLeft: 12 }}>VOLVER A MÍ</div> },
    { s: 89.6, el: <div style={{ fontFamily: "Serif", fontStyle: "italic", fontSize: 44, color: ROSA, marginTop: 2 }}>comprende tus vínculos, fortalece tu identidad</div> },
    { s: 90.1, el: <div style={{ fontFamily: "Sans", fontWeight: 500, fontSize: 34, letterSpacing: 2, marginTop: 34, lineHeight: 1.6 }}>5 de diciembre · 1:00 – 4:00 p. m.<br />The Ranch Hotel Boutique · Santa Elena<br />Inversión $130.000</div> },
    { s: 90.6, el: <div style={{ display: "inline-block", marginTop: 38, padding: "18px 50px", borderRadius: 60, background: ROSA, color: "#2A0F1E", fontFamily: "Sans", fontWeight: 600, fontSize: 36, letterSpacing: 3 }}>CUPOS LIMITADOS · RESERVA TU LUGAR</div> },
  ];
  if (t < 88.6) return null;
  return (
    <>
      <AbsoluteFill style={{ background: "linear-gradient(to bottom, rgba(18,6,12,0) 35%, rgba(18,6,12,.78) 62%, rgba(18,6,12,.9) 100%)", opacity: g }} />
      <div style={{ position: "absolute", left: 40, right: 40, top: 1080, textAlign: "center", color: "#fff", textShadow: "0 3px 18px rgba(0,0,0,.5)" }}>
        {items.map((it, i) => {
          const o = interpolate(t, [it.s, it.s + 0.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const y = interpolate(t, [it.s, it.s + 0.7], [16, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
          return <div key={i} style={{ opacity: o, transform: `translateY(${y}px)` }}>{it.el}</div>;
        })}
      </div>
    </>
  );
};

export const Edit: React.FC = () => {
  const t = useCurrentFrame() / 30;
  const fadeIn = interpolate(t, [0, 0.4], [1, 0], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      
      <OffthreadVideo src={staticFile("base.mp4")} volume={0.55} />
      {/* degradados suaves para que el texto se lea sin cajas */}
      <AbsoluteFill style={{ background: "linear-gradient(to bottom, rgba(0,0,0,.28) 0%, rgba(0,0,0,0) 18%, rgba(0,0,0,0) 60%, rgba(0,0,0,.42) 82%, rgba(0,0,0,.2) 100%)" }} />
      <Audio src={staticFile("voz.mp3")} volume={1} />
      {SUBS.map((c, i) => <Sub key={i} c={c} />)}
      {TITLES.map((x, i) => <TitleView key={i} x={x} />)}
      <Brand />
      <Info />
      <EndCard />
      <AbsoluteFill style={{ background: "#000", opacity: fadeIn }} />
    </AbsoluteFill>
  );
};
