"""Genera los SVG animados del README (divisor, cabeceras de seccion y marquesinas de iconos).
Uso: python3 tools/build_assets.py  (desde profile/). Necesita red para bajar los iconos de skillicons."""
import base64, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
W = 830
RED, EMBER, GRAY, PURPLE, LILAC = "#e11d48", "#ff4d6d", "#9ca3af", "#6b7280", "#d4d4dc"
PINK, ROSE, GOLD, VIOLET = RED, EMBER, GRAY, PURPLE  # alias de los nombres antiguos


def write(name, s):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(s)


def divider():
    petals = ""
    for i, (y, dur, delay, sc) in enumerate(((8, 9, 0, 1.0), (14, 12, -3, 0.8), (5, 10, -6, 0.9), (16, 14, -9, 0.7), (10, 11, -1.5, 1.1))):
        petals += f'''
  <g>
    <rect x="{-1.8*sc:.1f}" y="{-1.8*sc:.1f}" width="{3.6*sc:.1f}" height="{3.6*sc:.1f}" fill="{EMBER if i % 2 else LILAC}" opacity=".95">
      <animateTransform attributeName="transform" type="rotate" values="0;360" dur="{dur/2}s" repeatCount="indefinite" additive="sum"/>
    </rect>
    <animateMotion dur="{dur}s" begin="{delay}s" repeatCount="indefinite" path="M -10 {y} Q 200 {y-9} 415 {y+3} T {W+10} {y}"/>
  </g>'''
    write("divider.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="24" viewBox="0 0 {W} 24" fill="none">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{PURPLE}" stop-opacity="0"/>
      <stop offset=".25" stop-color="{PURPLE}"/>
      <stop offset=".5" stop-color="{RED}"/>
      <stop offset=".75" stop-color="{GRAY}"/>
      <stop offset="1" stop-color="{GRAY}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="-200" y1="0" x2="-20" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#fff" stop-opacity=".95"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
      <animate attributeName="x1" values="-200;{W}" dur="4s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="-20;{W+180}" dur="4s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect x="0" y="11" width="{W}" height="2" rx="1" fill="url(#g)"/>
  <rect x="0" y="10" width="{W}" height="4" rx="2" fill="url(#shine)"/>{petals}
</svg>
''')


def pixels(rows, cols, size, ox=0, oy=0):
    out = ""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in cols:
                out += f'<rect x="{ox + x*size}" y="{oy + y*size}" width="{size}" height="{size}" fill="{cols[ch]}"/>'
    return out


def rnd(seed):
    """Pseudoaleatorio determinista (LCG) para que los SVG salgan siempre iguales."""
    state = [seed * 2654435761 % 2**32]

    def r():
        state[0] = (state[0] * 1664525 + 1013904223) % 2**32
        return state[0] / 2**32
    return r


TORII = ["RRRRRRRRRRRRR", ".RRRRRRRRRRR.", "...D.....D...", "..RRRRRRRRR..", "...D.....D...", "...D.....D...", "...D.....D...", "...D.....D..."]
SHURIKEN = ["....R....", "...RRR...", "...RRR...", ".RRRRRRR.", "RRRR.RRRR", ".RRRRRRR.", "...RRR...", "...RRR...", "....R...."]
LANTERN = ["..WWW..", ".DDDDD.", ".RRRRR.", "RRRRRRR", "RDRDRDR", "RRRRRRR", ".RRRRR.", ".DDDDD.", "..WWW.."]
SEALS = {
    "about": ["...#...", "#..#..#", "#..#..#", "#..#..#", "#..#..#", "#######"],         # 山 colina (岡)
    "whatido": ["#######", "...#...", "...#...", "...#...", "...#...", "#######"],          # 工 trabajo
    "stack": ["...#...", "#######", "...#...", ".#.#.#.", "#..#..#", "...#..."],            # 木 arbol
    "stats": ["#####", "#...#", "#####", "#...#", "#...#", "#####"],                          # 日 sol/dia
    "contact": ["#######", "#.....#", "#.....#", "#.....#", "#.....#", "#######"],           # 口 boca
}


def icon_svg(kind):
    if kind == "torii":
        g = pixels(TORII, {"R": RED, "D": "#b3123a"}, 4, 0, 2)
        return f'<g>{g}<animate attributeName="opacity" values="1;.7;1" dur="2.6s" repeatCount="indefinite"/></g>'
    if kind == "shuriken":
        g = pixels(SHURIKEN, {"R": GRAY}, 4)
        return (f'<g transform="translate(18 18)"><g transform="translate(-18 -18)">{g}</g>'
                f'<animateTransform attributeName="transform" type="rotate" values="0 0 0;360 0 0" dur="2.4s" additive="sum" repeatCount="indefinite"/></g>')
    if kind == "katana":
        g = ""
        for i in range(11):
            col = "#b3123a" if i < 2 else PURPLE if i == 2 else "#e5e7eb"
            g += f'<rect x="{i*3}" y="{30-i*3}" width="6" height="6" fill="{col}"/>'
        return (f'<g>{g}<rect x="0" y="0" width="6" height="6" fill="#fff" opacity="0">'
                f'<animateTransform attributeName="transform" type="translate" values="12 18;30 0" dur="2.2s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;.5;1" dur="2.2s" repeatCount="indefinite"/></rect></g>')
    if kind == "sun":
        g = ""
        for y in range(9):
            for x in range(9):
                d2 = (x - 4) ** 2 + (y - 4) ** 2
                if d2 <= 17.5:
                    g += f'<rect x="{x*4}" y="{y*4}" width="4" height="4" fill="{RED if d2 > 5 else EMBER}"/>'
        return (f'<g transform="translate(18 18)"><g transform="translate(-18 -18)">{g}</g>'
                f'<animateTransform attributeName="transform" type="scale" values="1;1.14;1" dur="2.4s" additive="sum" repeatCount="indefinite"/></g>')
    if kind == "lantern":
        g = pixels(LANTERN, {"R": RED, "D": "#b3123a", "W": GRAY}, 4)
        return (f'<g><g>{g}</g>'
                f'<animateTransform attributeName="transform" type="rotate" values="-9 14 0;9 14 0;-9 14 0" dur="3s" repeatCount="indefinite"/></g>')
    if kind == "stack":
        rh = ["....#....", "..#####..", "#########", "..#####..", "....#...."]
        out = ""
        for k, col in enumerate((LILAC, PURPLE, RED)):
            g = pixels(rh, {"#": col}, 4)
            out += (f'<g transform="translate(0 {k*8})"><g>{g}<animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="2.4s" begin="{-(2-k)*0.35:.2f}s" repeatCount="indefinite"/></g></g>')
        return f'<g transform="translate(0 3)">{out}</g>'
    raise ValueError(kind)


def bg_effect(kind):
    r = rnd(7)
    if kind == "grid":
        lines = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="54"/>' for x in range(0, W, 12))
        return f'<g stroke="#ffffff" stroke-opacity=".04">{lines}</g>'
    if kind == "stripes":
        return ('<defs><pattern id="st" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                '<rect width="3" height="18" fill="#fff" fill-opacity=".05"/>'
                '<animateTransform attributeName="patternTransform" type="translate" additive="sum" values="0 0;18 0" dur="1.6s" repeatCount="indefinite"/></pattern></defs>'
                f'<rect width="{W}" height="54" fill="url(#st)"/>')
    if kind == "dots":
        out = ""
        for i in range(34):
            x, y, d = int(r() * W / 6) * 6, int(r() * 9) * 6, 2 + r() * 3
            c = PURPLE if i % 2 else GRAY
            out += f'<rect x="{x}" y="{y}" width="3" height="3" fill="{c}" opacity="0"><animate attributeName="opacity" values="0;.7;0" dur="{d:.1f}s" begin="{-r()*d:.1f}s" repeatCount="indefinite"/></rect>'
        return out
    if kind == "rain":
        out = ""
        for i in range(30):
            x, d = int(r() * W / 4) * 4, 1.2 + r() * 1.6
            out += (f'<rect x="{x}" y="-8" width="2" height="7" fill="{PURPLE if i % 3 else LILAC}" opacity=".55">'
                    f'<animateTransform attributeName="transform" type="translate" values="0 0;0 66" dur="{d:.1f}s" begin="{-r()*d:.1f}s" repeatCount="indefinite"/></rect>')
        return out
    if kind == "embers":
        out = ""
        for i in range(26):
            x, d = r() * W, 2.5 + r() * 3
            out += (f'<rect x="{x:.0f}" y="54" width="3" height="3" fill="{EMBER if i % 2 else RED}">'
                    f'<animateTransform attributeName="transform" type="translate" values="0 0;{(r()-.5)*30:.0f} -62" dur="{d:.1f}s" begin="{-r()*d:.1f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="opacity" values="0;.9;0" dur="{d:.1f}s" begin="{-r()*d:.1f}s" repeatCount="indefinite"/></rect>')
        return out
    raise ValueError(kind)


def title_effect(kind, text):
    font = "font-family=\"'Trebuchet MS','Segoe UI',Verdana,sans-serif\" font-size=\"25\" font-weight=\"800\" letter-spacing=\"4\""
    esc = text.replace("'", "&#39;")
    tw = len(text) * 20 + 60
    if kind == "slash":
        return (f'<linearGradient id="t" gradientUnits="userSpaceOnUse" x1="-120" y1="0" x2="0" y2="0">'
                f'<stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="{EMBER}"/><stop offset="1" stop-color="#fff"/>'
                f'<animate attributeName="x1" values="-120;{tw+60}" dur="5s" repeatCount="indefinite"/><animate attributeName="x2" values="0;{tw+180}" dur="5s" repeatCount="indefinite"/></linearGradient>',
                f'<text x="84" y="35" {font} fill="url(#t)">{esc}</text>'
                f'<polygon points="0,0 60,0 30,54 -30,54" fill="url(#sl)" opacity="0"><animateTransform attributeName="transform" type="translate" values="-80 0;{W+120} 0" dur="6s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;.9;.9;0" keyTimes="0;.1;.9;1" dur="6s" repeatCount="indefinite"/></polygon>')
    if kind == "glitch":
        def layer(col, dx, dy):
            return (f'<text x="84" y="35" {font} fill="{col}" opacity="0">{esc}'
                    f'<animate attributeName="opacity" values="0;0;.9;0;.9;0;0" keyTimes="0;.62;.64;.68;.7;.74;1" dur="4s" repeatCount="indefinite"/>'
                    f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;{dx} {dy};{-dx} 0;{dx} {-dy};0 0;0 0" keyTimes="0;.62;.64;.68;.7;.74;1" dur="4s" repeatCount="indefinite"/></text>')
        return ("", layer(RED, -5, 1) + layer(LILAC, 5, -1) + f'<text x="84" y="35" {font} fill="#fff">{esc}</text>')
    if kind == "typing":
        n = len(text)
        steps = list(range(n + 1)) + [n] * 6
        widths = ";".join(str(84 + i * 20) for i in steps)
        keyt = ";".join(f"{i/(len(steps)-1):.3f}" for i in range(len(steps)))
        mono = "font-family=\"'Courier New',Menlo,monospace\" font-size=\"26\" font-weight=\"700\""
        return (f'<clipPath id="tc"><rect x="0" y="0" width="84" height="54"><animate attributeName="width" values="{widths}" keyTimes="{keyt}" calcMode="discrete" dur="6s" repeatCount="indefinite"/></rect></clipPath>',
                f'<text x="84" y="35" {mono} textLength="{n*20}" lengthAdjust="spacing" fill="#fff" clip-path="url(#tc)">{esc}</text>'
                f'<rect x="84" y="14" width="12" height="26" fill="{RED}"><animate attributeName="x" values="{widths}" keyTimes="{keyt}" calcMode="discrete" dur="6s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="1;0;1" dur=".8s" repeatCount="indefinite"/></rect>')
    if kind == "scan":
        return ("", f'<text x="84" y="35" {font} fill="#fff">{esc}</text>'
                f'<rect x="0" y="0" width="{W}" height="2" fill="#fff" opacity=".22"><animateTransform attributeName="transform" type="translate" values="0 -4;0 56" dur="2.8s" repeatCount="indefinite"/></rect>'
                f'<text x="84" y="35" {font} fill="{LILAC}" opacity="0">{esc}<animate attributeName="opacity" values="0;0;.55;0;0" keyTimes="0;.45;.5;.55;1" dur="2.8s" repeatCount="indefinite"/></text>')
    if kind == "fade":
        spans = ""
        for i, ch in enumerate(text):
            ch = "&#160;" if ch == " " else "&#39;" if ch == "'" else ch
            a = .04 + i * .05
            spans += (f'<tspan opacity="0">{ch}<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{a:.2f};{a+.07:.2f};.9;1" dur="6s" repeatCount="indefinite"/></tspan>')
        return ("", f'<text x="84" y="35" {font} fill="#fff" xml:space="preserve">{spans}</text>')
    raise ValueError(kind)


SECTIONS = {
    "about": ("ABOUT ME", "torii", "grid", "slash"),
    "stack": ("TECH STACK", "stack", "dots", "typing"),
    "stats": ("GITHUB STATS", "sun", "rain", "scan"),
}


SEC_ICONS = {
    "about": f"""<path d="M3 4 H25 M6 8 H22 M9 8 V24 M19 8 V24 M5 14 H23" fill="none" stroke="{RED}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>""",
    "stack": f"""<path d="M14 3 L26 9 L14 15 L2 9 Z" fill="none" stroke="{LILAC}" stroke-width="2.2" stroke-linejoin="round"/>
      <path d="M2 14 L14 20 L26 14" fill="none" stroke="{LILAC}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity=".75"/>
      <path d="M2 19 L14 25 L26 19" fill="none" stroke="{RED}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>""",
    "stats": f"""<rect x="3" y="14" width="5" height="11" rx="1.5" fill="{LILAC}"/><rect x="11.5" y="7" width="5" height="18" rx="1.5" fill="{RED}"/><rect x="20" y="11" width="5" height="14" rx="1.5" fill="{LILAC}"/>""",
}
SEC_TITLES = {"about": "ABOUT ME", "stack": "TECH STACK", "stats": "GITHUB STATS"}


def section(name):
    text, ico = SEC_TITLES[name], SEC_ICONS[name]
    hh = 48
    write(f"h-{name}-v2.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{hh}" viewBox="0 0 {W} {hh}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d0d13"/><stop offset="1" stop-color="#1a181d"/></linearGradient>
    <clipPath id="cp"><rect width="{W}" height="{hh}" rx="10"/></clipPath>
    <linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{RED}"/><stop offset=".35" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></linearGradient>
    <linearGradient id="sh" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="120" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-140 0;{W+20} 0;{W+20} 0" keyTimes="0;.5;1" dur="7s" repeatCount="indefinite"/></linearGradient>
  </defs>
  <rect width="{W}" height="{hh}" rx="10" fill="url(#bg)"/>
  <g transform="translate(20 9)">{ico}<animateTransform attributeName="transform" type="translate" values="20 9;20 7;20 9" dur="3.2s" repeatCount="indefinite"/></g>
  <text x="62" y="30" font-family="'Trebuchet MS','Segoe UI',Verdana,sans-serif" font-size="21" font-weight="700" letter-spacing="5" fill="#f3f4f6">{text}</text>
  <g clip-path="url(#cp)"><rect x="0" y="{hh-3}" width="{W}" height="3" fill="url(#ln)"/>
  <rect x="0" y="{hh-3}" width="{W}" height="3" fill="url(#sh)" opacity=".6"/></g>
</svg>
""")


def divider_dots():
    out = ""
    for i in range(41):
        x = 5 + i * 20
        c = RED if i % 5 == 0 else PURPLE if i % 5 == 2 else GRAY
        out += (f'<rect x="{x}" y="9" width="6" height="6" fill="{c}" opacity=".15">'
                f'<animate attributeName="opacity" values=".15;1;.15" dur="2.4s" begin="{i*0.06:.2f}s" repeatCount="indefinite"/></rect>')
    write("divider-dots.svg", f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="24" viewBox="0 0 {W} 24">{out}</svg>\n')


def divider_pulse():
    pts, x = ["0,12"], 0
    while x < W - 110:
        pts += [f"{x+70},12", f"{x+76},12", f"{x+82},3", f"{x+90},21", f"{x+96},12"]
        x += 210
    pts.append(f"{W},12")
    path = " ".join(pts)
    write("divider-pulse.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="24" viewBox="0 0 {W} 24" fill="none">
  <polyline points="{path}" stroke="#3f3f46" stroke-width="1.5" stroke-linejoin="round"/>
  <polyline points="{path}" stroke="{RED}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round" pathLength="1000" stroke-dasharray="90 910">
    <animate attributeName="stroke-dashoffset" values="90;-1000" dur="3.2s" repeatCount="indefinite"/>
  </polyline>
  <polyline points="{path}" stroke="{PURPLE}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" pathLength="1000" stroke-dasharray="50 950" opacity=".9">
    <animate attributeName="stroke-dashoffset" values="560;-440" dur="3.2s" repeatCount="indefinite"/>
  </polyline>
</svg>
""")


def divider_blade():
    h = W // 2
    write("divider-blade.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="24" viewBox="0 0 {W} 24" fill="none">
  <defs>
    <linearGradient id="b" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GRAY}" stop-opacity="0"/><stop offset=".5" stop-color="#e5e7eb"/><stop offset="1" stop-color="{GRAY}" stop-opacity="0"/></linearGradient>
  </defs>
  <rect x="{h}" y="11" width="0" height="2" fill="url(#b)">
    <animate attributeName="x" values="{h};0;0;{h}" keyTimes="0;.3;.8;1" dur="4.5s" repeatCount="indefinite"/>
    <animate attributeName="width" values="0;{W};{W};0" keyTimes="0;.3;.8;1" dur="4.5s" repeatCount="indefinite"/>
  </rect>
  <g transform="translate({h} 12)">
    <polygon points="0,-9 4,0 0,9 -4,0" fill="{RED}"><animateTransform attributeName="transform" type="rotate" values="0;180;180;0" keyTimes="0;.3;.8;1" dur="4.5s" repeatCount="indefinite"/></polygon>
    <polygon points="0,-4 2,0 0,4 -2,0" fill="#fff"/>
  </g>
</svg>
""")


G, L = "#9ca3af", LILAC
ICONS = {
    "APPS": f"""<rect x="16" y="4" width="24" height="48" rx="6" fill="none" stroke="{G}" stroke-width="2.5"/>
      <line x1="24" y1="10" x2="32" y2="10" stroke="{G}" stroke-width="2.5" stroke-linecap="round"/>
      <rect x="21" y="18" width="6" height="6" rx="2" fill="{RED}"/><rect x="29" y="18" width="6" height="6" rx="2" fill="{L}"/>
      <rect x="21" y="27" width="6" height="6" rx="2" fill="{L}"/><rect x="29" y="27" width="6" height="6" rx="2" fill="{G}"/>
      <line x1="24" y1="46" x2="32" y2="46" stroke="{G}" stroke-width="2.5" stroke-linecap="round"/>""",
    "WEB": f"""<rect x="3" y="9" width="50" height="38" rx="6" fill="none" stroke="{G}" stroke-width="2.5"/>
      <line x1="3" y1="20" x2="53" y2="20" stroke="{G}" stroke-width="2.5"/>
      <circle cx="10" cy="14.5" r="1.8" fill="{RED}"/><circle cx="16" cy="14.5" r="1.8" fill="{L}"/><circle cx="22" cy="14.5" r="1.8" fill="{G}"/>
      <polyline points="21,28 14,34 21,40" fill="none" stroke="{L}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
      <polyline points="35,28 42,34 35,40" fill="none" stroke="{L}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="31" y1="27" x2="25" y2="41" stroke="{RED}" stroke-width="2.8" stroke-linecap="round"/>""",
    "AI": f"""<path d="M28 4 C29.5 18 34 22.5 48 24 C34 25.5 29.5 30 28 44 C26.5 30 22 25.5 8 24 C22 22.5 26.5 18 28 4Z" fill="none" stroke="{L}" stroke-width="2.5" stroke-linejoin="round"/>
      <path d="M44 34 C44.7 40 46.5 41.8 52 42.5 C46.5 43.2 44.7 45 44 51 C43.3 45 41.5 43.2 36 42.5 C41.5 41.8 43.3 40 44 34Z" fill="{RED}"/>
      <circle cx="12" cy="44" r="2.6" fill="{G}"/>""",
    "DESIGN": f"""<path d="M28 3 L43 27 C43 36 36 41 28 53 C20 41 13 36 13 27 Z" fill="none" stroke="{L}" stroke-width="2.6" stroke-linejoin="round"/>
      <line x1="28" y1="28" x2="28" y2="53" stroke="{L}" stroke-width="2.2" stroke-linecap="round"/>
      <circle cx="28" cy="25" r="4" fill="{RED}"/>
      <path d="M17 31 C22 33 25 33 28 28 C31 33 34 33 39 31" fill="none" stroke="{G}" stroke-width="1.8" stroke-linecap="round"/>""",
}
CARDS = [("APPS", "bob"), ("WEB", "tilt"), ("AI", "pulse"), ("DESIGN", "bob")]


def about_panel():
    ph = 228
    F = "font-family=\"'Trebuchet MS','Segoe UI',Verdana,sans-serif\""
    items = ""
    cw = (W - 80) / 4
    for i, (title, fx) in enumerate(CARDS):
        cx = 40 + i * cw
        d = i * 0.6
        g = ICONS[title]
        if fx == "tilt":
            anim = f'<animateTransform attributeName="transform" type="rotate" values="-4 28 28;4 28 28;-4 28 28" dur="3s" begin="{d}s" repeatCount="indefinite"/>'
        elif fx == "pulse":
            anim = f'<animateTransform attributeName="transform" type="scale" values="1;1.06;1" additive="sum" dur="1.8s" begin="{d}s" repeatCount="indefinite"/>'
        else:
            anim = f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="2.4s" begin="{d}s" repeatCount="indefinite"/>'
        items += f"""
  <g transform="translate({cx:.0f} 162)"><g transform="scale(.8)"><g>{g}{anim}</g></g></g>
  <text x="{cx + 52:.0f}" y="178" {F} font-size="12" fill="{RED}" letter-spacing="2">0{i+1}</text>
  <text x="{cx + 52:.0f}" y="198" {F} font-size="16" font-weight="700" letter-spacing="3" fill="#f3f4f6">{title}</text>"""
    hl = lambda t, c: f'<tspan fill="{c}" font-weight="700">{t}</tspan>'
    corner = lambda x, y, sx, sy: f'<path d="M{x} {y+sy*16} V{y} H{x+sx*16}" fill="none" stroke="{RED}" stroke-width="2"/>'
    write("about-panel-v3.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{ph}" viewBox="0 0 {W} {ph}">
  <defs>
    <radialGradient id="glow" cx=".92" cy=".2" r=".7"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".22"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
    <radialGradient id="glow2" cx=".05" cy="1" r=".6"><stop offset="0" stop-color="{RED}" stop-opacity=".18"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="{W}" height="{ph}" fill="#09090e"/>
  <rect width="{W}" height="{ph}" fill="url(#glow)"/>
  <rect width="{W}" height="{ph}" fill="url(#glow2)"/>
  <text x="{W-26}" y="190" text-anchor="end" font-family="'Songti SC','Hiragino Mincho ProN','Noto Serif CJK JP',serif" font-size="170" font-weight="700" fill="#fff" opacity=".045">&#21109;</text>
  {corner(10, 10, 1, 1)}{corner(W-10, 10, -1, 1)}{corner(10, ph-10, 1, -1)}{corner(W-10, ph-10, -1, -1)}
  <text x="40" y="34" {F} font-size="11" letter-spacing="5" fill="{LILAC}" opacity=".85">WHAT I DO</text>
  <text x="40" y="70" {F} font-size="22" fill="#e5e7eb" xml:space="preserve">I build {hl("apps", RED)}, {hl("websites", LILAC)} and {hl("AI-powered tools", RED)},</text>
  <text x="40" y="98" {F} font-size="22" fill="#e5e7eb" xml:space="preserve">and I also edit video, model in 3D and design.</text>
  <text x="40" y="126" {F} font-size="14" font-style="italic" fill="#8b8d98" xml:space="preserve">I like to combine both worlds: software that generates and processes creative content.</text>
  <line x1="40" y1="146" x2="{W-40}" y2="146" stroke="#fff" stroke-opacity=".12" stroke-dasharray="2 5"/>{items}
</svg>
""")


AI_TOOLS = [
    # (nombre, fuente del logo, tipo de logo propio)
    ("Claude", "si:claude", None), ("Gemini", "si:googlegemini", None), ("ChatGPT", "oa:openai", None),
    ("Whisper", None, "wave"), ("ElevenLabs", "si:elevenlabs", None), ("Higgsfield", None, "higgs"),
    ("Hugging Face", "si:huggingface", None), ("Ollama", "si:ollama", None), ("Cursor", "si:cursor", None),
    ("Copilot", "si:githubcopilot", None), ("Grok", "lb:grok", None), ("Mistral", "si:mistralai", None),
]
LOGO_URLS = {
    "si": "https://cdn.simpleicons.org/{n}",
    "oa": "https://cdn.jsdelivr.net/npm/simple-icons@14.0.0/icons/{n}.svg",   # OpenAI ya no esta en el CDN actual
    "lb": "https://cdn.jsdelivr.net/npm/@lobehub/icons-static-svg@latest/icons/{n}.svg",
}


def logo_path(src):
    """(d, fill-rule) del logo; se cachea en assets/icons/ para no depender de la red."""
    kind, n = src.split(":")
    cache = os.path.join(OUT, "icons", f"logo-{kind}-{n}.txt")
    if os.path.exists(cache):
        rule, d = open(cache).read().split("\n", 1)
        return d, rule
    svg = subprocess.run(["curl", "-sL", "-m", "20", LOGO_URLS[kind].format(n=n)], capture_output=True, text=True).stdout
    d = " ".join(re.findall(r' d="([^"]+)"', svg))
    rule = "evenodd" if "evenodd" in svg else "nonzero"
    with open(cache, "w") as fh:
        fh.write(rule + "\n" + d)
    return d, rule


def custom_logo(kind, i):
    if kind == "wave":
        hs = [(5, 10), (11, 18), (17, 7), (9, 15), (14, 20), (6, 12), (10, 5)]
        out = ""
        for k, (a, b) in enumerate(hs):
            x = 2.6 + k * 2.9
            out += (f'<rect x="{x:.1f}" y="{12-a/2}" width="1.8" height="{a}" rx=".9" fill="#fff">'
                    f'<animate attributeName="height" values="{a};{b};{a}" dur="1.3s" begin="{-k*0.17:.2f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="y" values="{12-a/2};{12-b/2};{12-a/2}" dur="1.3s" begin="{-k*0.17:.2f}s" repeatCount="indefinite"/></rect>')
        return out
    if kind == "higgs":
        data = base64.b64encode(open(os.path.join(OUT, "icons", "higgsfield.png"), "rb").read()).decode()
        return f'<image x="1" y="1" width="22" height="22" href="data:image/png;base64,{data}"/>'
    if kind == "bubble":
        dots = "".join(f'<circle cx="{8+4*k}" cy="10.5" r="1.3" fill="#fff"><animate attributeName="opacity" values=".25;1;.25" dur="1.2s" begin="{k*0.25}s" repeatCount="indefinite"/></circle>' for k in range(3))
        return ('<path d="M4 3.5h16a2 2 0 0 1 2 2v9.5a2 2 0 0 1-2 2h-7l-5 4v-4H4a2 2 0 0 1-2-2V5.5a2 2 0 0 1 2-2z" fill="none" stroke="#fff" stroke-width="1.7" stroke-linejoin="round"/>' + dots)
    raise ValueError(kind)


def ai_panel():
    cols, cw = 6, 138
    tile, top, rowh = 64, 40, 108
    h = top + 2 * rowh + 4
    accents = [RED, PURPLE, GRAY]
    cx = lambda c: c * cw + cw / 2
    cy = lambda r: top + r * rowh + tile / 2
    lines = ""
    for r in range(2):
        for c in range(cols - 1):
            lines += f'<line x1="{cx(c)+tile/2+4}" y1="{cy(r)}" x2="{cx(c+1)-tile/2-4}" y2="{cy(r)}"/>'
    for c in range(cols):
        lines += f'<line x1="{cx(c)}" y1="{cy(0)+tile/2+4}" x2="{cx(c)}" y2="{cy(1)-tile/2-4}"/>'
    tiles = ""
    for i, (name, src, kind) in enumerate(AI_TOOLS):
        r, c = divmod(i, cols)
        x, y = cx(c) - tile / 2, top + r * rowh
        if src:
            dd, rule = logo_path(src)
        inner = (f'<g transform="translate({tile/2-16} {tile/2-16}) scale(1.333)"><path fill="#fff" fill-rule="{rule}" d="{dd}"/></g>' if src
                 else f'<g transform="translate({tile/2-16} {tile/2-16}) scale(1.333)">{custom_logo(kind, i)}</g>')
        d = i * 0.35
        acc = accents[i % 3]
        tiles += f"""
  <g transform="translate({x:.1f} {y})">
    <g>
      <rect width="{tile}" height="{tile}" rx="14" fill="url(#tb)" stroke="#2f2f3d"/>
      <rect x="14" y="{tile-4}" width="{tile-28}" height="3" rx="1.5" fill="{acc}"/>
      <rect width="{tile}" height="{tile}" rx="14" fill="none" stroke="{acc}" stroke-width="1.5" opacity="0"><animate attributeName="opacity" values="0;.9;0" dur="3.6s" begin="{d}s" repeatCount="indefinite"/></rect>
      {inner}
      <animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="3.6s" begin="{d}s" repeatCount="indefinite"/>
    </g>
    <text x="{tile/2}" y="{tile+20}" text-anchor="middle" font-family="'Trebuchet MS','Segoe UI',Verdana,sans-serif" font-size="12" font-weight="700" letter-spacing="1" fill="#d4d4dc">{name}</text>
  </g>"""
    write("ai-panel.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
  <defs>
    <linearGradient id="tb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14141c"/><stop offset="1" stop-color="#1f1d24"/></linearGradient>
  </defs>
  <rect width="{W}" height="{h}" rx="10" fill="#0a0a0f"/>
  <rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="10" fill="none" stroke="#2f2f3d"/>
  <text x="20" y="25" font-family="'Courier New',Menlo,monospace" font-size="13" font-weight="700" letter-spacing="2" fill="{RED}">&gt; AI TOOLBOX<tspan fill="#9ca3af" opacity="1">_<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>
  <g stroke="#6b7280" stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="3 7" stroke-linecap="round">
    <animate attributeName="stroke-dashoffset" values="0;-20" dur="1.4s" repeatCount="indefinite"/>
    {lines}
  </g>{tiles}
</svg>
""")


def kanji_paths():
    """Contornos vectoriales de los kanji (cacheados en assets/icons/kanji.json); la primera vez usa Songti TC Light."""
    import json
    cache = os.path.join(OUT, "icons", "kanji.json")
    if os.path.exists(cache):
        return json.load(open(cache))
    from fontTools.ttLib import TTCollection
    from fontTools.pens.svgPathPen import SVGPathPen
    font = TTCollection("/System/Library/Fonts/Supplemental/Songti.ttc").fonts[5]
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    out = {}
    for ch in "機網智創":
        pen = SVGPathPen(gs)
        gs[cmap[ord(ch)]].draw(pen)
        out[ch] = pen.getCommands()
    json.dump(out, open(cache, "w"))
    return out


HERO = [("機", "APPS"), ("網", "WEB"), ("智", "AI"), ("創", "CREATIVE")]


def hero_strip():
    paths = kanji_paths()
    h, colw = 172, W / 4
    r = rnd(11)
    cols = ""
    for i, (ch, label) in enumerate(HERO):
        cx = colw * i + colw / 2
        d = i * 0.9
        size = 58
        k = size / 1000
        gx, gy = cx - size / 2, 92 - 6 + size * 0.0
        cols += f"""
  <g>
    <g transform="translate({cx:.1f} 78) rotate(-62)">
      <circle r="46" fill="none" stroke="url(#en)" stroke-width="3.2" stroke-linecap="round" pathLength="100" stroke-dasharray="0 100" opacity=".95">
        <animate attributeName="stroke-dasharray" values="0 100;86 100;86 100;86 100;0 100" keyTimes="0;.22;.8;.92;1" dur="8s" begin="{d}s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values=".95;.95;.95;0;0" keyTimes="0;.8;.9;.97;1" dur="8s" begin="{d}s" repeatCount="indefinite"/>
      </circle>
      <circle r="43" fill="none" stroke="url(#en)" stroke-width="1" stroke-linecap="round" pathLength="100" stroke-dasharray="0 100" opacity=".5">
        <animate attributeName="stroke-dasharray" values="0 100;80 100;80 100;0 100" keyTimes="0;.26;.9;1" dur="8s" begin="{d+0.2}s" repeatCount="indefinite"/>
      </circle>
    </g>
    <g transform="translate({gx:.1f} {gy+27:.1f}) scale({k} {-k})" fill="#f5f5f7" opacity="0">
      <path d="{paths[ch]}"/>
      <animate attributeName="opacity" values="0;0;1;1;1;0" keyTimes="0;.08;.28;.8;.92;1" dur="8s" begin="{d}s" repeatCount="indefinite"/>
    </g>
    <text x="{cx:.1f}" y="152" text-anchor="middle" font-family="'Trebuchet MS','Segoe UI',Verdana,sans-serif" font-size="12" font-weight="700" letter-spacing="6" fill="#d4d4dc">{label}</text>
    <circle cx="{cx:.1f}" cy="162" r="2" fill="{RED}"><animate attributeName="opacity" values=".25;1;.25" dur="2s" begin="{d}s" repeatCount="indefinite"/></circle>
  </g>"""
        if i:
            cols += f'\n  <line x1="{colw*i:.1f}" y1="30" x2="{colw*i:.1f}" y2="{h-30}" stroke="#ffffff" stroke-opacity=".1"/>'
    motes = ""
    for i in range(22):
        x, d = r() * W, 5 + r() * 5
        motes += (f'<circle cx="{x:.0f}" cy="{h}" r="{1+r()*1.4:.1f}" fill="{GRAY if i % 2 else LILAC}">'
                  f'<animateTransform attributeName="transform" type="translate" values="0 0;{(r()-.5)*40:.0f} {-h-10}" dur="{d:.1f}s" begin="{-r()*d:.1f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values="0;.5;0" dur="{d:.1f}s" begin="{-r()*d:.1f}s" repeatCount="indefinite"/></circle>')
    write("hero-strip.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
  <defs>
    <linearGradient id="hb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#09090d"/><stop offset=".6" stop-color="#12121a"/><stop offset="1" stop-color="#1d1b22"/></linearGradient>
    <linearGradient id="en" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
    <pattern id="sg" width="40" height="20" patternUnits="userSpaceOnUse">
      <g fill="none" stroke="#fff" stroke-opacity=".055">
        <circle cx="0" cy="20" r="18"/><circle cx="0" cy="20" r="12"/><circle cx="0" cy="20" r="6"/>
        <circle cx="40" cy="20" r="18"/><circle cx="40" cy="20" r="12"/><circle cx="40" cy="20" r="6"/>
        <circle cx="20" cy="10" r="18"/><circle cx="20" cy="10" r="12"/><circle cx="20" cy="10" r="6"/>
      </g>
    </pattern>
    <clipPath id="hc"><rect width="{W}" height="{h}" rx="10"/></clipPath>
  </defs>
  <g clip-path="url(#hc)">
    <rect width="{W}" height="{h}" fill="url(#hb)"/>
    <rect width="{W}" height="{h}" fill="url(#sg)"/>
    {motes}
    <circle cx="{W-34}" cy="30" r="7" fill="{RED}"><animate attributeName="r" values="7;8.5;7" dur="3s" repeatCount="indefinite"/></circle>
    <circle cx="34" cy="30" r="3" fill="{PURPLE}" opacity=".8"/>{cols}
  </g>
  <rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="10" fill="none" stroke="#2f2f3d"/>
</svg>
""")


def fetch_icon(slug):
    path = os.path.join(OUT, "icons", f"{slug}.svg")
    if os.path.exists(path):
        data = open(path, "rb").read()
    else:
        data = subprocess.run(["curl", "-s", "-m", "20", f"https://skillicons.dev/icons?i={slug}&theme=dark"], capture_output=True).stdout
    return base64.b64encode(data).decode()


def marquee(name, slugs, reverse=False, dur=40):
    size, gap = 48, 18
    step = size + gap
    n = len(slugs)
    loop = step * n
    imgs = ""
    for rep in range(W // loop + 3):
        for i, s in enumerate(slugs):
            x = rep * loop + i * step
            imgs += f'<image x="{x}" y="8" width="{size}" height="{size}" href="data:image/svg+xml;base64,{fetch_icon(s)}"/>'
    vals = (f"-{loop} 0;0 0" if reverse else f"0 0;-{loop} 0")
    write(f"m-{name}.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="64" viewBox="0 0 {W} 64">
  <defs>
    <linearGradient id="f" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".08" stop-color="#fff"/>
      <stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="m"><rect width="{W}" height="64" fill="url(#f)"/></mask>
  </defs>
  <g mask="url(#m)">
    <g>{imgs}
      <animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur}s" repeatCount="indefinite"/>
    </g>
  </g>
</svg>
''')


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    divider()
    for n in SECTIONS:
        section(n)
    about_panel()
    marquee("row1", ["py", "ts", "js", "swift", "html", "css", "bash", "nextjs", "astro", "react", "tailwind", "nodejs", "fastapi", "sqlite"], dur=44)
    marquee("row2", ["blender", "ps", "ai", "pr", "ae", "davinci", "docker", "n8n", "git", "github", "vercel", "vscode", "apple", "figma"], reverse=True, dur=40)
    print("ok")
