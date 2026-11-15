"""Generate the profile header (dark + light): a live moire of two triangular lattices.

The only graphic on the profile. The second lattice rotates slowly between 1.5 and 4.0 degrees;
the fringe period follows L = a / (2 sin(theta/2)). Values in the caption line are real results
from the linked repositories.
"""
import math, os, html

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

SANS = "-apple-system, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SFMono-Regular', 'Cascadia Mono', Consolas, Menlo, monospace"

THEMES = {
    "dark":  dict(bg="#0b0e13", border="#1d232c", text="#e9edf2", muted="#8b95a3", faint="#566170",
                  dots="#c9d3df", dotop="0.42", accent="#d9a441"),
    "light": dict(bg="#fbfbfc", border="#e3e7ec", text="#11161d", muted="#5a6573", faint="#97a1ad",
                  dots="#1e2a38", dotop="0.32", accent="#9a6a12"),
}

RESULTS = [
    ("Twisted hBN, registry-resolved DFT", "V<tspan dy='4' font-size='12'>0</tspan><tspan dy='-4'> = 40 meV</tspan>"),
    ("Orbital qubit in twisted hBN", "T<tspan dy='4' font-size='12'>1</tspan><tspan dy='-4'> ≈ 6–11 ps</tspan>"),
    ("Magic-angle graphene junction", "half-step width 0.200 I<tspan dy='4' font-size='12'>c</tspan>"),
    ("Repeater chain, 400 km", "1.94 Hz with optimal cutoff"),
]

def esc(s):
    return html.escape(s, quote=True)

def lattice(pid, a, r, color, op, cx, cy, anim=None):
    h = a * math.sqrt(3)
    dots = "".join(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}"/>' for x, y in
                   [(0, 0), (a, 0), (0, h), (a, h), (a / 2, h / 2)])
    a_el = ""
    if anim:
        vals, dur = anim
        a_el = (f'<animateTransform attributeName="patternTransform" type="rotate" '
                f'values="{";".join(f"{v} {cx} {cy}" for v in vals)}" dur="{dur}s" repeatCount="indefinite" '
                f'calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>')
    return (f'<pattern id="{pid}" width="{a}" height="{h:.4f}" patternUnits="userSpaceOnUse" '
            f'patternTransform="rotate(0 {cx} {cy})">{a_el}<g fill="{color}" fill-opacity="{op}">{dots}</g></pattern>')

def hero(theme):
    t = THEMES[theme]; W, H = 1280, 400
    cx, cy = 960, 200
    n = len(RESULTS); per = 4.5; dur = n * per; f = 0.03
    cycle = ""
    for i, (label, value) in enumerate(RESULTS):
        s, e = i / n, (i + 1) / n
        kt = f"0;{s:.4f};{s+f:.4f};{e-f:.4f};{e:.4f};1"
        cycle += (f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
                  f'<text x="0" y="0" font-family="{SANS}" font-size="14" fill="{t["muted"]}">{esc(label)}</text>'
                  f'<text x="0" y="26" font-family="{MONO}" font-size="19" fill="{t["accent"]}">{value}</text></g>')
    body = f'''
<defs>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0.40" stop-color="#fff" stop-opacity="0"/><stop offset="0.66" stop-color="#fff" stop-opacity="1"/></linearGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <clipPath id="c"><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12"/></clipPath>
  {lattice("la", 12, 1.55, t["dots"], t["dotop"], cx, cy)}
  {lattice("lb", 12, 1.55, t["dots"], t["dotop"], cx, cy, anim=([1.5, 4.0, 1.5], 30))}
</defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  <g mask="url(#m)">
    <rect x="380" y="-240" width="1140" height="880" fill="url(#la)"/>
    <rect x="380" y="-240" width="1140" height="880" fill="url(#lb)"/>
  </g>
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{t["border"]}"/>
<text x="64" y="132" font-family="{SANS}" font-size="52" font-weight="600" fill="{t["text"]}" letter-spacing="-0.8">Faruk Sami Bilgin</text>
<text x="66" y="174" font-family="{SANS}" font-size="19" fill="{t["muted"]}">Independent researcher in quantum devices</text>
<text x="66" y="202" font-family="{SANS}" font-size="19" fill="{t["muted"]}">Josephson and moiré qubits, graphene quantum dots, quantum networks</text>
<line x1="66" x2="126" y1="262" y2="262" stroke="{t["border"]}" stroke-width="1"/>
<g transform="translate(66,296)">{cycle}</g>
<text x="{W-36}" y="{H-30}" text-anchor="end" font-family="{SANS}" font-size="12" fill="{t["faint"]}">Two triangular lattices, twist 1.5°–4.0° · moiré period L = a / 2 sin(θ/2)</text>
'''
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Faruk Sami Bilgin, independent researcher in quantum devices">{body}</svg>')
    with open(os.path.join(OUT, f"header-{theme}.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)

for th in THEMES:
    hero(th)
print("ok")
