import React from "react";
import { AbsoluteFill, Audio, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, Easing, delayRender, continueRender, random } from "remotion";

export const DUR = 39.5;
const FPS = 30;
const ROSA = "#F6BCCB";
const VINO = "#5A1E34";
const CREMA = "#FFF6EF";

const FUENTES: [string, string, string, string][] = [
  ["Serif", "cormorant-garamond-latin-500-normal", "500", "normal"], ["Serif", "cormorant-garamond-latin-600-normal", "600", "normal"],
  ["Serif", "cormorant-garamond-latin-500-italic", "500", "italic"], ["Serif", "cormorant-garamond-latin-600-italic", "600", "italic"],
  ["Sans", "montserrat-latin-400-normal", "400", "normal"], ["Sans", "montserrat-latin-500-normal", "500", "normal"], ["Sans", "montserrat-latin-600-normal", "600", "normal"],
];
const espera = delayRender("fuentes");
Promise.all(FUENTES.map(([fam, file, weight, style]) =>
  new FontFace(fam, `url(${staticFile(`fonts/${file}.woff2`)})`, { weight, style }).load().then((f) => (document.fonts as any).add(f))
)).then(() => continueRender(espera));

const useT = () => useCurrentFrame() / FPS;
const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
const sp = (frame: number, startS: number, damping = 14, stiffness = 120) =>
  spring({ frame: frame - Math.round(startS * FPS), fps: FPS, config: { damping, stiffness, mass: 0.9 } });

// Extrusión 3D falsa del texto: capas de sombra hacia abajo-derecha
const extrude = (n: number, color: string) =>
  Array.from({ length: n }, (_, i) => `${(i + 1) * 0.6}px ${(i + 1) * 1.1}px 0 ${color}`).join(",") + ", 0 18px 40px rgba(0,0,0,.55)";

// ---------- Título 3D: cada palabra gira desde atrás (rotateX) con profundidad ----------
type Word = { w: string; k?: boolean };
const parse = (t: string): Word[][] =>
  t.split("/").map((line) => {
    const out: Word[] = [];
    line.trim().split(/(\*[^*]+\*)/).filter(Boolean).forEach((p) => {
      const k = p.startsWith("*");
      p.replace(/\*/g, "").trim().split(/\s+/).filter(Boolean).forEach((w) => out.push({ w, k }));
    });
    return out;
  });

const Title3D: React.FC<{ s: number; e: number; t: string; label?: string; top?: number; size?: number }> = ({ s, e, t, label, top = 170, size = 84 }) => {
  const f = useCurrentFrame();
  const now = f / FPS;
  if (now < s - 0.05 || now > e + 0.05) return null;
  const out = interpolate(now, [e - 0.35, e], [0, 1], clamp);
  const lines = parse(t);
  let idx = 0;
  const lab = sp(f, s, 18, 140);
  return (
    <div style={{ position: "absolute", left: 50, right: 50, top, textAlign: "center", perspective: 1100, perspectiveOrigin: "50% 40%" }}>
      <div style={{ transformStyle: "preserve-3d", transform: `rotateX(${out * 70}deg) translateZ(${-out * 200}px)`, opacity: 1 - out }}>
        {label && (
          <div style={{ display: "inline-block", fontFamily: "Sans", fontWeight: 600, fontSize: 28, letterSpacing: 9, color: VINO, background: ROSA,
            padding: "10px 26px", borderRadius: 40, marginBottom: 20, transform: `translateY(${(1 - lab) * -30}px) scale(${0.6 + 0.4 * lab})`, opacity: lab }}>{label}</div>
        )}
        {lines.map((ln, li) => (
          <div key={li} style={{ transformStyle: "preserve-3d", lineHeight: 1.04 }}>
            {ln.map((wd) => {
              const d = s + 0.12 + idx++ * 0.07;
              const p = sp(f, d, 13, 110);
              const sz = wd.k ? size * 1.15 : size;
              return (
                <span key={idx} style={{ display: "inline-block", margin: "0 0.17em", transformOrigin: "50% 100%",
                  transform: `rotateX(${(1 - p) * -95}deg) translateZ(${(1 - p) * -260}px)`, opacity: interpolate(p, [0, 0.35], [0, 1], clamp),
                  fontFamily: "Serif", fontStyle: wd.k ? "italic" : "normal", fontWeight: wd.k ? 600 : 500, fontSize: sz,
                  color: wd.k ? ROSA : CREMA, textShadow: extrude(wd.k ? 8 : 6, wd.k ? "#8E3A57" : "rgba(60,25,35,.85)") }}>{wd.w}</span>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
};

// ---------- Subtítulos del diálogo ----------
type Cue = [number, number, string];
const SUBS: Cue[] = [
  [0.0, 1.95, "¿Se acaba el año?"], [2.0, 4.6, "¿Cuántas veces dijiste / *«esta es la última vez»*?"], [5.05, 7.8, "Muchas… y siempre / *vuelvo a buscarlo*."],
  [8.45, 10.3, "Eres *fuerte*, *independiente*,"], [10.3, 11.45, "logras todo…"], [11.45, 13.45, "pero en el amor sigues / *en el mismo círculo*."],
  [13.5, 15.95, "Lo sé… y estoy cansada de / *conformarme con menos*."],
  [16.0, 18.7, "No termines el año / *repitiendo la misma historia*."], [18.9, 21.45, "Ven conmigo a *Volver a mí*, / en Talita Kum."],
  [21.5, 23.95, "Cuatro psicólogas, / aquí en *Laureles*."],
  [24.0, 25.05, "¿Y cuánto vale?"], [25.05, 26.15, "*$120.000*."], [26.15, 27.6, "Con pronto pago, *$90.000*."],
  [27.6, 30.15, "Incluye material, refrigerio / y *un obsequio*."], [30.2, 31.9, "Esta vez, *vuelvo a mí*."],
];
const Rich: React.FC<{ t: string; key2: number }> = ({ t, key2 }) => (
  <>{t.split("/").map((line, li) => (
    <div key={li}>{line.trim().split(/(\*[^*]+\*)/).map((p, i) => p.startsWith("*")
      ? <span key={i} style={{ fontFamily: "Serif", fontStyle: "italic", fontWeight: 600, color: ROSA, fontSize: key2 }}>{p.slice(1, -1)}</span>
      : <span key={i}>{p}</span>)}</div>))}</>
);
const Sub: React.FC<{ c: Cue; top: number }> = ({ c, top }) => {
  const now = useT();
  if (now < c[0] || now > c[1]) return null;
  const o = interpolate(now, [c[0], c[0] + 0.18, c[1] - 0.12, c[1]], [0, 1, 1, 0], clamp);
  const y = interpolate(now, [c[0], c[0] + 0.3], [12, 0], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <div style={{ position: "absolute", left: 60, right: 60, top, textAlign: "center", opacity: o, transform: `translateY(${y}px)`,
      fontFamily: "Sans", fontWeight: 500, fontSize: 50, lineHeight: 1.25, color: "#fff", textShadow: "0 2px 16px rgba(0,0,0,.8), 0 0 2px rgba(0,0,0,.7)" }}>
      <Rich t={c[2]} key2={64} />
    </div>
  );
};

// ---------- Anillo 3D ("el mismo círculo") ----------
const Ring3D: React.FC<{ s: number; e: number }> = ({ s, e }) => {
  const f = useCurrentFrame(); const now = f / FPS;
  if (now < s || now > e) return null;
  const p = sp(f, s, 16, 90);
  const o = interpolate(now, [e - 0.4, e], [1, 0], clamp) * p;
  const rot = (now - s) * 140;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 70, height: 420, perspective: 900, display: "flex", justifyContent: "center", opacity: o }}>
      <div style={{ width: 760, height: 420, transformStyle: "preserve-3d", transform: `rotateX(72deg) rotateZ(${rot}deg) scale(${0.4 + 0.6 * p})` }}>
        {Array.from({ length: 10 }, (_, i) => (
          <div key={i} style={{ position: "absolute", inset: 0, borderRadius: "50%", border: `3px solid rgba(246,188,203,${0.9 - i * 0.07})`,
            transform: `translateZ(${i * 3}px)`, boxShadow: i === 0 ? "0 0 40px rgba(246,188,203,.6)" : undefined }} />
        ))}
        <div style={{ position: "absolute", left: "50%", top: -8, width: 16, height: 16, marginLeft: -8, borderRadius: 8, background: ROSA, boxShadow: `0 0 24px ${ROSA}` }} />
      </div>
    </div>
  );
};

// ---------- Partículas 3D (bokeh a distintas profundidades) ----------
const Bokeh: React.FC<{ s: number; e: number; n?: number }> = ({ s, e, n = 26 }) => {
  const now = useT();
  if (now < s || now > e) return null;
  const o = interpolate(now, [s, s + 0.8, e - 0.5, e], [0, 1, 1, 0], clamp);
  return (
    <AbsoluteFill style={{ perspective: 800, opacity: o, pointerEvents: "none" }}>
      {Array.from({ length: n }, (_, i) => {
        const x = random(`x${i}`) * 1080, y0 = random(`y${i}`) * 1920, z = -600 + random(`z${i}`) * 700;
        const r = 10 + random(`r${i}`) * 34, sp2 = 30 + random(`v${i}`) * 70;
        const y = ((y0 - (now - s) * sp2) % 1920 + 1920) % 1920;
        return <div key={i} style={{ position: "absolute", left: x, top: y, width: r, height: r, borderRadius: "50%",
          transform: `translateZ(${z}px)`, background: `radial-gradient(circle, rgba(255,214,224,.85) 0%, rgba(246,188,203,.25) 55%, rgba(246,188,203,0) 70%)`,
          filter: `blur(${Math.max(0, -z / 160)}px)` }} />;
      })}
    </AbsoluteFill>
  );
};

// ---------- Marca 3D: VOLVER A MÍ + Talita Kum ----------
const Brand3D: React.FC = () => {
  const f = useCurrentFrame(); const now = f / FPS;
  const s = 19.55, e = 23.95;
  if (now < s || now > e) return null;
  const out = interpolate(now, [e - 0.35, e], [0, 1], clamp);
  const letters = "VOLVER A MÍ".split("");
  const sub = sp(f, s + 0.8, 16, 120), chip = sp(f, 22.1, 14, 130);
  const tilt = Math.sin((now - s) * 1.2) * 6;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 1040, perspective: 1000, textAlign: "center", opacity: 1 - out }}>
      <div style={{ display: "inline-block", padding: "34px 50px 38px", borderRadius: 36, background: "rgba(40,14,24,.55)", border: "1.5px solid rgba(246,188,203,.55)",
        backdropFilter: "blur(14px)", transformStyle: "preserve-3d", transform: `rotateY(${tilt}deg) rotateX(${(1 - sp(f, s, 15, 100)) * 70}deg)`,
        boxShadow: "0 30px 60px rgba(0,0,0,.45)" }}>
        <div style={{ fontFamily: "Sans", fontWeight: 600, fontSize: 26, letterSpacing: 10, color: ROSA, opacity: sub }}>TALLER</div>
        <div style={{ transformStyle: "preserve-3d", whiteSpace: "nowrap" }}>
          {letters.map((ch, i) => {
            const p = sp(f, s + 0.05 + i * 0.05, 12, 120);
            return <span key={i} style={{ display: "inline-block", width: ch === " " ? 34 : undefined, fontFamily: "Serif", fontWeight: 600, fontSize: 104, letterSpacing: 4,
              color: CREMA, transform: `rotateY(${(1 - p) * 110}deg) translateZ(${(1 - p) * 180}px)`, opacity: interpolate(p, [0, 0.3], [0, 1], clamp),
              textShadow: extrude(7, "#7A2E49") }}>{ch}</span>;
          })}
        </div>
        <div style={{ fontFamily: "Serif", fontStyle: "italic", fontSize: 54, color: ROSA, marginTop: 2, opacity: sub, transform: `translateY(${(1 - sub) * 16}px)` }}>en Talita Kum</div>
        <div style={{ display: "inline-block", marginTop: 18, padding: "10px 28px", borderRadius: 40, background: ROSA, color: VINO, fontFamily: "Sans", fontWeight: 600, fontSize: 28,
          transform: `scale(${chip}) translateZ(${(1 - chip) * 100}px)`, opacity: chip }}>4 psicólogas · Laureles, Medellín</div>
      </div>
    </div>
  );
};

// ---------- Tarjeta de precio 3D ----------
const Price3D: React.FC = () => {
  const f = useCurrentFrame(); const now = f / FPS;
  const s = 25.0, e = 30.15;
  if (now < s || now > e) return null;
  const inn = sp(f, s, 14, 110), out = interpolate(now, [e - 0.35, e], [0, 1], clamp);
  const dis = sp(f, 26.25, 18, 140), nuevo = sp(f, 26.85, 11, 150);
  const items = [["Material de trabajo", 27.7], ["Refrigerio", 28.6], ["Obsequio", 29.35]] as const;
  const flt = Math.sin((now - s) * 1.6) * 5;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 960, perspective: 1100, textAlign: "center", opacity: 1 - out }}>
      <div style={{ display: "inline-block", width: 760, padding: "30px 40px", borderRadius: 34, background: "linear-gradient(145deg, rgba(255,246,239,.96), rgba(250,224,232,.94))",
        transformStyle: "preserve-3d", transform: `rotateY(${(1 - inn) * -80 + flt}deg) rotateX(${4 - flt * 0.4}deg) translateZ(${(1 - inn) * -300}px)`,
        boxShadow: "0 40px 80px rgba(30,8,16,.5), inset 0 0 0 2px rgba(255,255,255,.6)", color: VINO }}>
        <div style={{ fontFamily: "Sans", fontWeight: 600, fontSize: 24, letterSpacing: 8, opacity: .75 }}>INVERSIÓN</div>
        <div style={{ position: "relative", display: "inline-block", fontFamily: "Serif", fontWeight: 600, fontSize: 82, opacity: 1 - dis * 0.55,
          transform: `scale(${1 - dis * 0.3})` }}>
          $120.000
          <div style={{ position: "absolute", left: -6, right: -6, top: "52%", height: 6, borderRadius: 3, background: "#C2475F", transformOrigin: "left", transform: `scaleX(${dis})` }} />
        </div>
        <div style={{ transform: `translateZ(${(1 - nuevo) * 220}px) scale(${0.5 + 0.5 * nuevo})`, opacity: nuevo, marginTop: -6 }}>
          <span style={{ fontFamily: "Serif", fontWeight: 600, fontSize: 118, color: "#B23A5B", textShadow: extrude(6, "rgba(178,58,91,.35)") }}>$90.000</span>
          <div style={{ fontFamily: "Sans", fontWeight: 600, fontSize: 28, letterSpacing: 4 }}>PRONTO PAGO</div>
        </div>
        <div style={{ display: "flex", justifyContent: "center", gap: 14, marginTop: 22 }}>
          {items.map(([txt, at], i) => {
            const p = sp(f, at, 12, 140);
            return <div key={i} style={{ padding: "10px 18px", borderRadius: 30, background: VINO, color: CREMA, fontFamily: "Sans", fontWeight: 500, fontSize: 24,
              transform: `rotateX(${(1 - p) * -90}deg)`, opacity: p, whiteSpace: "nowrap" }}>✓ {txt}</div>;
          })}
        </div>
      </div>
    </div>
  );
};

// ---------- Cierre: invitación 3D ----------
const EndCard: React.FC = () => {
  const f = useCurrentFrame(); const now = f / FPS;
  const s = 31.95;
  if (now < s - 0.6) return null;
  const bg = interpolate(now, [s - 0.6, s + 0.4], [0, 1], clamp);
  const inn = sp(f, s, 13, 80);
  const flt = Math.sin((now - s) * 1.1);
  const sweep = interpolate(now, [s + 1.0, s + 2.2], [-120, 220], clamp);
  const row = (at: number) => { const p = sp(f, at, 15, 130); return { opacity: p, transform: `translateZ(${(1 - p) * 120}px) translateY(${(1 - p) * 20}px)` }; };
  const btn = sp(f, s + 2.3, 10, 160);
  const pulse = 1 + Math.max(0, Math.sin((now - s - 2.8) * 4)) * 0.04 * (now > s + 2.8 ? 1 : 0);
  return (
    <>
      <AbsoluteFill style={{ backdropFilter: `blur(${bg * 18}px)`, background: `rgba(36,10,20,${bg * 0.55})` }} />
      <AbsoluteFill style={{ perspective: 1300, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ position: "relative", width: 860, padding: "60px 56px 56px", borderRadius: 44, overflow: "hidden", textAlign: "center", color: VINO,
          background: "linear-gradient(160deg, #FFF8F2 0%, #FBE3EA 60%, #F5CFDA 100%)", transformStyle: "preserve-3d",
          transform: `rotateY(${(1 - inn) * 95 + flt * 7}deg) rotateX(${flt * 3 + 3}deg) translateZ(${(1 - inn) * -400}px)`,
          boxShadow: "0 60px 120px rgba(20,4,10,.6), inset 0 0 0 2px rgba(255,255,255,.7)" }}>
          <div style={{ position: "absolute", top: -200, bottom: -200, width: 140, left: `${sweep}%`, transform: "rotate(18deg)",
            background: "linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.65), rgba(255,255,255,0))" }} />
          <div style={row(s + 0.45)}><span style={{ fontFamily: "Sans", fontWeight: 600, fontSize: 26, letterSpacing: 9, opacity: .8 }}>TALLER · CIERRE DE AÑO</span></div>
          <div style={{ ...row(s + 0.6), fontFamily: "Serif", fontWeight: 600, fontSize: 112, lineHeight: 1, marginTop: 14, color: "#7A2E49", textShadow: extrude(6, "rgba(122,46,73,.25)") }}>VOLVER A MÍ</div>
          <div style={{ ...row(s + 0.85), fontFamily: "Serif", fontStyle: "italic", fontSize: 48, color: "#B23A5B", marginTop: 8 }}>No termines el año repitiendo la misma historia</div>
          <div style={{ ...row(s + 1.1), height: 2, background: "rgba(122,46,73,.25)", margin: "30px 40px" }} />
          <div style={{ ...row(s + 1.2), fontFamily: "Serif", fontWeight: 600, fontSize: 62 }}>Talita Kum</div>
          <div style={{ ...row(s + 1.35), fontFamily: "Sans", fontWeight: 500, fontSize: 30, marginTop: 6, lineHeight: 1.45 }}>Espacio terapéutico · 4 psicólogas<br />Laureles, Medellín</div>
          <div style={{ ...row(s + 1.6), display: "flex", justifyContent: "center", gap: 18, marginTop: 30 }}>
            <div style={{ padding: "14px 24px", borderRadius: 22, background: "rgba(122,46,73,.08)", fontFamily: "Sans", fontWeight: 600, fontSize: 32 }}>10:00 a. m. – 12:00 m.</div>
          </div>
          <div style={{ ...row(s + 1.8), marginTop: 26, fontFamily: "Sans", fontWeight: 500, fontSize: 32 }}>
            <span style={{ textDecoration: "line-through", opacity: .6 }}>$120.000</span>
            <span style={{ fontFamily: "Serif", fontWeight: 600, fontSize: 70, color: "#B23A5B", margin: "0 14px" }}>$90.000</span>
            <span style={{ fontWeight: 600 }}>pronto pago</span>
          </div>
          <div style={{ ...row(s + 2.0), fontFamily: "Sans", fontWeight: 500, fontSize: 27, marginTop: 8, opacity: .85 }}>Incluye material de trabajo, refrigerio y obsequio</div>
          <div style={{ display: "inline-block", marginTop: 36, padding: "22px 60px", borderRadius: 60, background: "linear-gradient(135deg, #B23A5B, #7A2E49)", color: "#fff",
            fontFamily: "Sans", fontWeight: 600, fontSize: 36, letterSpacing: 3, boxShadow: "0 14px 30px rgba(122,46,73,.45)",
            transform: `translateZ(${(1 - btn) * 200}px) scale(${btn * pulse})`, opacity: btn }}>RESERVA TU CUPO</div>
        </div>
      </AbsoluteFill>
    </>
  );
};

const SFX: [number, string, number][] = [
  [0.1, "whoosh", 0.25], [8.05, "whoosh", 0.22], [12.4, "cristal", 0.18], [16.05, "whoosh", 0.22], [19.55, "swoosh", 0.3], [22.1, "pop", 0.2],
  [25.0, "swoosh", 0.28], [26.85, "ding", 0.25], [27.7, "pop", 0.15], [28.6, "pop", 0.15], [29.35, "pop", 0.15], [31.95, "whoosh", 0.3], [34.3, "ding", 0.22],
];

export const Promo: React.FC = () => {
  const now = useT();
  const fadeIn = interpolate(now, [0, 0.3], [1, 0], clamp);
  const fadeOut = interpolate(now, [DUR - 0.5, DUR], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <OffthreadVideo src={staticFile("base.mp4")} volume={1} />
      <AbsoluteFill style={{ background: "linear-gradient(to bottom, rgba(20,6,12,.55) 0%, rgba(20,6,12,0) 26%, rgba(20,6,12,0) 52%, rgba(20,6,12,.55) 78%, rgba(20,6,12,.7) 100%)" }} />
      {SFX.map(([t, n, v], i) => <Sequence key={i} from={Math.round(t * FPS)}><Audio src={staticFile(`sfx/${n}.wav`)} volume={v} /></Sequence>)}
      <Bokeh s={19.4} e={24.0} n={18} />
      <Bokeh s={31.6} e={DUR} n={30} />
      <Title3D s={0.1} e={7.85} label="CERRANDO EL AÑO" t="¿Cuántas veces / dijiste *«la última vez»?*" />
      <Ring3D s={12.45} e={15.9} />
      <Title3D s={8.05} e={15.9} t="Fuerte en todo… / *el mismo círculo*" size={80} />
      <Title3D s={16.05} e={19.4} t="No termines el año / *repitiendo la historia*" size={80} />
      <Title3D s={30.15} e={31.95} t="Esta vez, / *vuelvo a mí*" size={92} />
      <Brand3D />
      <Price3D />
      {SUBS.map((c, i) => <Sub key={i} c={c} top={(c[0] >= 19.5 && c[0] < 24) || (c[0] >= 25 && c[0] < 30.2) ? 1500 : 1470} />)}
      <EndCard />
      <AbsoluteFill style={{ background: "#000", opacity: Math.max(fadeIn, fadeOut) }} />
    </AbsoluteFill>
  );
};
