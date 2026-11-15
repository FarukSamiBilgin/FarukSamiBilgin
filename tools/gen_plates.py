"""Profile README plates in the style of https://faruksamibilgin.github.io.

Every small figure is computed from the equation of its chapter (or read from the
linked repository's results), not drawn by hand:
  01  L(theta) = a / 2 sin(theta/2), graphene a = 0.246 nm
  02  short-junction current-phase relation, tau = 0.95, against sin(phi)
  03  overdamped RSJ under drive (tools/shapiro.json, from tools/shapiro.js)
  04  Cooper-pair-box levels vs offset charge, E_J/E_C = 2 (charge basis)
  05  Ramsey fringe 1/2 + 1/2 exp(-t/T2) cos(wt)
  06  secret-key rate vs memory cutoff (repeater-cutoff-policies/results/results.json, e1)
  07  orbital T1 floor in twisted hBN (6-11 ps) against the 30 ns target
"""
import json, math, os, html
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets")
os.makedirs(OUT, exist_ok=True)

SANS = "'Archivo', 'Helvetica Neue', 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = SANS  # no monospace anywhere: numbers use the text face
DARK = dict(bg="#0a0a0a", fg="#f2f2f0", mu="#9b9b96", fa="#5f5f5b", li="#2a2a2a", ac="#da291c")
LIGHT = dict(bg="#f4f4f1", fg="#121212", mu="#5c5c57", fa="#93938d", li="#d6d6cf", ac="#da291c")
esc = lambda s: html.escape(s, quote=True)

def path(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

class Box:
    """Map data coordinates into a figure box (x0..x1, y0..y1 in pixels)."""
    def __init__(self, x, y, w, h, xr, yr, logx=False, logy=False):
        self.x, self.y, self.w, self.h, self.xr, self.yr, self.lx, self.ly = x, y, w, h, xr, yr, logx, logy
    def X(self, v):
        a, b = self.xr; f = (math.log10(v) - math.log10(a)) / (math.log10(b) - math.log10(a)) if self.lx else (v - a) / (b - a)
        return self.x + f * self.w
    def Y(self, v):
        a, b = self.yr; f = (math.log10(v) - math.log10(a)) / (math.log10(b) - math.log10(a)) if self.ly else (v - a) / (b - a)
        return self.y + self.h - f * self.h
    def axes(self, c):
        return (f'<line x1="{self.x}" y1="{self.y+self.h+.5}" x2="{self.x+self.w}" y2="{self.y+self.h+.5}" stroke="{c["fa"]}" stroke-width="1"/>'
                f'<line x1="{self.x+.5}" y1="{self.y}" x2="{self.x+.5}" y2="{self.y+self.h}" stroke="{c["fa"]}" stroke-width="1"/>')

def text(x, y, s, c, size=13, fam=MONO, anchor="start", weight=400, color=None):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color or c["mu"]}" text-anchor="{anchor}">{esc(s)}</text>')

# ------------------------------------------------------------------ figures
def fig1(c, B):
    b = Box(*B, (0.5, 6), (1, 40), logy=True)
    pts = [(b.X(t), b.Y(0.246 / (2 * math.sin(math.radians(t) / 2)))) for t in np.linspace(0.62, 6, 160)]
    xm, ym = b.X(1.08), b.Y(13.05)
    return (b.axes(c) + f'<path d="{path(pts)}" fill="none" stroke="{c["fg"]}" stroke-width="1.8"/>'
            f'<line x1="{xm:.1f}" y1="{b.y}" x2="{xm:.1f}" y2="{b.y+b.h}" stroke="{c["mu"]}" stroke-dasharray="2 4"/>'
            f'<circle cx="{xm:.1f}" cy="{ym:.1f}" r="5" fill="{c["ac"]}"/>'
            + text(xm + 12, ym - 8, "1.08°  →  13 nm", c, color=c["ac"])
            + text(b.x + b.w, b.y + b.h + 20, "twist angle θ", c, 12, SANS, "end")
            + text(b.x - 8, b.y + 10, "L", c, 12, SANS, "end"))

def fig2(c, B):
    b = Box(*B, (0, 2 * math.pi), (-1.15, 1.15))
    ph = np.linspace(0, 2 * math.pi, 400)
    tau = 0.95
    f = np.sin(ph) / np.sqrt(1 - tau * np.sin(ph / 2) ** 2); f /= f.max()
    s = [(b.X(p), b.Y(math.sin(p))) for p in ph]
    g = [(b.X(p), b.Y(v)) for p, v in zip(ph, f)]
    return (b.axes(c).replace(f'y1="{b.y+b.h+.5}" x2', f'y1="{b.Y(0)+.5}" x2').replace(f'y2="{b.y+b.h+.5}"', f'y2="{b.Y(0)+.5}"')
            + f'<path d="{path(s)}" fill="none" stroke="{c["mu"]}" stroke-width="1.2" stroke-dasharray="5 5"/>'
            f'<path d="{path(g)}" fill="none" stroke="{c["ac"]}" stroke-width="2.2"/>'
            + text(b.X(0.62 * math.pi) + 10, b.Y(1) + 4, "τ = 0.95", c, color=c["ac"])
            + text(b.X(1.55 * math.pi), b.Y(-0.62), "sin φ", c)
            + text(b.x + b.w, b.y + b.h + 20, "phase φ, 0 to 2π", c, 12, SANS, "end"))

def fig3(c, B):
    data = json.load(open(os.path.join(HERE, "shapiro.json")))
    b = Box(*B, (0, 5), (0, 2.4))
    pts = [(b.X(i), b.Y(min(v, 2.4))) for i, v in data]
    guides = "".join(f'<line x1="{b.x}" y1="{b.Y(n):.1f}" x2="{b.x+b.w}" y2="{b.Y(n):.1f}" stroke="{c["ac"]}" stroke-opacity="0.55" stroke-dasharray="4 5"/>' for n in (0.5, 1.5))
    return (b.axes(c) + guides + f'<path d="{path(pts)}" fill="none" stroke="{c["fg"]}" stroke-width="2"/>'
            + text(b.x + 8, b.Y(0.5) - 8, "n = ½", c, color=c["ac"])
            + text(b.x + b.w, b.y + b.h + 20, "bias current  I / Ic", c, 12, SANS, "end")
            + text(b.x - 8, b.y + 10, "V", c, 12, SANS, "end"))

def fig4(c, B):
    NC, ej = 20, 2.0
    ngs = np.linspace(-1, 1, 161); lv = []
    for ng in ngs:
        n = np.arange(-NC, NC + 1); H = np.diag(4.0 * (n - ng) ** 2) - ej / 2 * (np.eye(2 * NC + 1, k=1) + np.eye(2 * NC + 1, k=-1))
        lv.append(np.linalg.eigvalsh(H)[:3])
    lv = np.array(lv); i0 = np.argmin(abs(ngs - 0.5)); e0, e01 = lv[i0, 0], lv[i0, 1] - lv[i0, 0]
    y = (lv - e0) / e01
    b = Box(*B, (-1, 1), (-0.2, 3.2))
    cols = [c["fg"], c["ac"], c["mu"]]
    out = b.axes(c)
    for k in (2, 1, 0):
        pts = [(b.X(x), b.Y(min(v, 3.2))) for x, v in zip(ngs, y[:, k])]
        out += f'<path d="{path(pts)}" fill="none" stroke="{cols[k]}" stroke-width="{2.2 if k == 1 else 1.6}"/>'
    out += text(b.x + b.w + 6, b.Y(y[-1, 0]) + 4, "|0⟩", c, color=c["fg"]) + text(b.x + b.w + 6, b.Y(y[-1, 1]) + 4, "|1⟩", c, color=c["ac"])
    return out + text(b.x + b.w, b.y + b.h + 20, "offset charge  n_g", c, 12, SANS, "end") + text(b.x, b.y - 12, "E_J / E_C = 2", c)

def fig5(c, B):
    b = Box(*B, (0, 10), (0, 1))
    t = np.linspace(0, 10, 500); T2 = 3.2
    p = 0.5 + 0.5 * np.exp(-t / T2) * np.cos(2 * math.pi * 0.9 * t)
    env_u = [(b.X(x), b.Y(0.5 + 0.5 * math.exp(-x / T2))) for x in t]
    env_d = [(b.X(x), b.Y(0.5 - 0.5 * math.exp(-x / T2))) for x in t]
    return (b.axes(c) + f'<path d="{path(env_u)}" fill="none" stroke="{c["ac"]}" stroke-width="1.4" stroke-dasharray="4 4"/>'
            f'<path d="{path(env_d)}" fill="none" stroke="{c["ac"]}" stroke-width="1.4" stroke-dasharray="4 4"/>'
            f'<path d="{path([(b.X(x), b.Y(v)) for x, v in zip(t, p)])}" fill="none" stroke="{c["fg"]}" stroke-width="1.6"/>'
            + text(b.X(3.4), b.Y(0.86), "e^(−t/T₂)", c, color=c["ac"])
            + text(b.x + b.w, b.y + b.h + 20, "delay t", c, 12, SANS, "end"))

def fig6(c, B):
    rp = os.path.join(HERE, "..", "..", "repeater-cutoff-policies", "results", "results.json")
    rows = json.load(open(rp))["e1"]["rows"]
    pts = sorted((r["cutoff_over_tcoh"], r["secret_key_hz"]) for r in rows if r["cutoff_over_tcoh"] not in (None, float("inf")) and isinstance(r["cutoff_over_tcoh"], (int, float)) and math.isfinite(r["cutoff_over_tcoh"]))
    b = Box(*B, (min(p[0] for p in pts) * 0.8, max(p[0] for p in pts) * 1.25), (0, 2.3), logx=True)
    best = max(pts, key=lambda p: p[1])
    line = [(b.X(x), b.Y(y)) for x, y in pts]
    dots = "".join(f'<circle cx="{b.X(x):.1f}" cy="{b.Y(y):.1f}" r="2.6" fill="{c["fg"]}"/>' for x, y in pts)
    return (b.axes(c) + f'<path d="{path(line)}" fill="none" stroke="{c["fg"]}" stroke-width="1.6"/>' + dots
            + f'<circle cx="{b.X(best[0]):.1f}" cy="{b.Y(best[1]):.1f}" r="5.5" fill="{c["ac"]}"/>'
            + text(b.X(best[0]) + 12, b.Y(best[1]) - 6, f"{best[1]:.2f} Hz", c, color=c["ac"])
            + text(b.x + b.w, b.y + b.h - 10, "no cutoff: 0 Hz", c, 12, SANS, "end")
            + text(b.x + b.w, b.y + b.h + 20, "memory cutoff / T_coh", c, 12, SANS, "end")
            + text(b.x - 8, b.y + 10, "key", c, 12, SANS, "end"))

def fig7(c, B):
    b = Box(*B, (25, 72), (1e-12, 1e-6), logy=True)
    pts = [(32, 5.9e-12), (48, 11.3e-12), (64, 7.9e-12)]
    ty = b.Y(30e-9)
    out = b.axes(c) + f'<line x1="{b.x}" y1="{ty:.1f}" x2="{b.x+b.w}" y2="{ty:.1f}" stroke="{c["fg"]}" stroke-dasharray="5 5"/>'
    out += text(b.x + 8, ty - 8, "needed for a logical qubit: 30 ns", c, color=c["fg"])
    out += "".join(f'<circle cx="{b.X(x):.1f}" cy="{b.Y(y):.1f}" r="5" fill="{c["ac"]}"/>' for x, y in pts)
    out += text(b.X(48), b.Y(11.3e-12) - 14, "two-phonon floor: 6–11 ps", c, anchor="middle", color=c["ac"])
    gx = b.X(68)
    out += (f'<line x1="{gx:.1f}" y1="{ty+6:.1f}" x2="{gx:.1f}" y2="{b.Y(9e-12)-8:.1f}" stroke="{c["mu"]}" stroke-width="1"/>'
            + text(gx - 8, (ty + b.Y(9e-12)) / 2, "≈ 3000×", c, anchor="end"))
    return out + text(b.x + b.w, b.y + b.h + 20, "level spacing E₂₁ (meV)", c, 12, SANS, "end") + text(b.x - 8, b.y + 10, "T₁", c, 12, SANS, "end")

CH = [
    ("01", "Geometry", "Two lattices, one twist", "How a small rotation makes a large superlattice, and why 1.08° is special.", fig1),
    ("02", "Junction", "A junction is a nonlinear inductor", "The current–phase relation, and how transparency reshapes it.", fig2),
    ("03", "Drive", "Listening to a junction with microwaves", "Shapiro steps, and what a half step tells you about the junction.", fig3),
    ("04", "Levels", "A qubit is the bottom of a ladder", "Charging against Josephson energy, and why the transmon works.", fig4),
    ("05", "Coherence", "What a qubit forgets, and how fast", "Relaxation, dephasing, and how a coherence budget is built.", fig5),
    ("06", "Distance", "Sending entanglement far", "Repeater chains, memories, and the cutoff that makes key possible.", fig6),
    ("07", "Limits", "When the answer is no", "Six calculations that ruled something out, and the reasons.", fig7),
]

def plate(num, label, title, desc, fn, c):
    W, H = 1280, 236
    fig = fn(c, (930, 40, 286, 140))
    body = (f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>'
            f'<line x1="64" y1="0.5" x2="{W-64}" y2="0.5" stroke="{c["li"]}"/>'
            + text(64, 150, num, c, 116, SANS, weight=200, color=c["fg"]).replace("<text ", '<text letter-spacing="-4" ')
            + text(250, 78, label.upper(), c, 12, SANS, weight=400).replace("<text ", '<text letter-spacing="3.6" ')
            + text(250, 124, title, c, 33, SANS, weight=300, color=c["fg"]).replace("<text ", '<text letter-spacing="-0.4" ')
            + text(250, 160, desc, c, 18, SANS)
            + text(250, 200, "READ THE CHAPTER  →", c, 11, SANS, weight=500, color=c["ac"]).replace("<text ", '<text letter-spacing="3" ')
            + fig)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Chapter {num}: {esc(title)}">{body}</svg>'

for i, ch in enumerate(CH):
    c = LIGHT if i % 2 == 0 else DARK
    with open(os.path.join(OUT, f"ch{ch[0]}.svg"), "w", encoding="utf-8") as fh:
        fh.write(plate(*ch, c))

# ------------------------------------------------------------------ header
def lattice(pid, a, r, color, op, cx, cy, anim=None):
    h = a * math.sqrt(3)
    dots = "".join(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}"/>' for x, y in [(0, 0), (a, 0), (0, h), (a, h), (a / 2, h / 2)])
    el = ""
    if anim:
        vals, dur = anim
        el = (f'<animateTransform attributeName="patternTransform" type="rotate" values="{";".join(f"{v} {cx} {cy}" for v in vals)}" '
              f'dur="{dur}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>')
    return (f'<pattern id="{pid}" width="{a}" height="{h:.4f}" patternUnits="userSpaceOnUse" patternTransform="rotate(0 {cx} {cy})">'
            f'{el}<g fill="{color}" fill-opacity="{op}">{dots}</g></pattern>')

def header():
    c = DARK; W, H = 1280, 600; cx, cy = 960, 300
    body = f'''<defs>
<linearGradient id="v" x1="0" x2="1"><stop offset="0.36" stop-color="#fff" stop-opacity="0"/><stop offset="0.68" stop-color="#fff" stop-opacity="1"/></linearGradient>
<mask id="m"><rect width="{W}" height="{H}" fill="url(#v)"/></mask>
{lattice("a", 12, 1.5, "#e8e8e4", "0.5", cx, cy)}
{lattice("b", 12, 1.5, "#e8e8e4", "0.5", cx, cy, ([1.6, 4.2, 1.6], 30))}
</defs>
<rect width="{W}" height="{H}" fill="{c["bg"]}"/>
<g mask="url(#m)"><rect x="360" y="-300" width="1200" height="1200" fill="url(#a)"/><rect x="360" y="-300" width="1200" height="1200" fill="url(#b)"/></g>
''' + (text(64, 66, "FARUK SAMI BILGIN", c, 12, SANS, weight=500, color=c["fg"]).replace("<text ", '<text letter-spacing="3.6" ')
       + text(W - 64, 66, "NOTES ON QUANTUM DEVICES", c, 12, SANS, "end", 500, c["fg"]).replace("<text ", '<text letter-spacing="3.6" ')
       + f'<line x1="0" y1="96.5" x2="{W}" y2="96.5" stroke="{c["li"]}"/>'
       + text(64, 236, "Twisted lattices,", c, 72, SANS, weight=300, color=c["fg"]).replace("<text ", '<text letter-spacing="-1.6" ')
       + text(64, 312, "junctions and qubits", c, 72, SANS, weight=300, color=c["fg"]).replace("<text ", '<text letter-spacing="-1.6" ')
       + text(66, 372, "Seven short chapters on the physics behind my work. Each has a", c, 21, SANS)
       + text(66, 402, "figure you can change, and each ends with the full calculation", c, 21, SANS)
       + text(66, 432, "— code and data — in a public repository.", c, 21, SANS)
       + text(66, 500, "FARUKSAMIBILGIN.GITHUB.IO  →", c, 12, SANS, weight=500, color=c["ac"]).replace("<text ", '<text letter-spacing="3" ')
       + text(66, H - 40, "Header: two triangular lattices twisting between 1.6° and 4.2°; moiré period L = a / 2 sin(θ/2).", c, 13, SANS, color=c["fa"]))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Notes on quantum devices by Faruk Sami Bilgin: twisted lattices, junctions and qubits.">{body}</svg>'
    open(os.path.join(OUT, "notes-header.svg"), "w", encoding="utf-8").write(svg)

header()
print("written", sorted(os.listdir(OUT)))
