"""Design components: SVG charts, tables, CSS. Extracted from the approved design. Do not hard-code data here."""
import math

NAVY = "#14264f"; RED = "#d0021b"
PL = []   # filled in place by pages.build_pages()
BRAND = {"name": "TEAM", "sub": "TEAM REPORT", "logo": ""}

def icon(kind, c="#fff", s=22):
    p = {
        "trophy": '<path d="M7 4h10v5a5 5 0 0 1-10 0z M7 6H3v2a4 4 0 0 0 4 4 M17 6h4v2a4 4 0 0 1-4 4 M12 14v4 M8 21h8 M9 18h6"/>',
        "person": '<circle cx="12" cy="5" r="2.5"/><path d="M8 21v-9l-2-2 M16 21v-9l2-2 M8 12h8 M9 21v-4 M15 21v-4"/>',
        "weight": '<path d="M6 21h12l2-11H4z M9 10a3 3 0 1 1 6 0"/>',
        "clock": '<circle cx="12" cy="13" r="8"/><path d="M12 13V8 M9 3h6 M12 3v2 M19 6l-1 1"/>',
        "run": '<circle cx="15" cy="4" r="2"/><path d="M8 21l4-6-3-3 3-4 4 3 3 1 M7 10l3-2 M12 15l4 6"/>',
        "bars": '<path d="M4 20V12M10 20V6M16 20V9M22 20V3" stroke-width="3.5"/>',
        "check": '<circle cx="12" cy="12" r="9"/><path d="M7.5 12.5l3 3 6-6.5"/>',
        "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 1v5M12 18v5M1 12h5M18 12h5"/>',
        "ball": '<ellipse cx="12" cy="12" rx="10" ry="6" transform="rotate(-35 12 12)"/><path d="M8 14l8-4M10 9l4 6"/>',
        "warn": '<path d="M12 3L2 21h20z M12 10v5 M12 18v.5"/>',
        "star": '<path d="M12 2l3 7 7 .7-5.3 4.8 1.6 7.2L12 18l-6.3 3.7 1.6-7.2L2 9.7 9 9z"/>',
        "trend": '<path d="M3 17l6-6 4 4 8-9 M15 6h6v6"/>',
        "note": '<path d="M4 20h16 M5 16l10-10 3 3-10 10H5z"/>',
        "bulb": '<path d="M9 18h6 M10 21h4 M12 2a6 6 0 0 0-3 11c1 1 1 2 1 3h4c0-1 0-2 1-3a6 6 0 0 0-3-11z"/>',
        "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
        "dumb": '<path d="M2 9v6M5 6v12M19 6v12M22 9v6M5 12h14"/>',
        "bal": '<circle cx="12" cy="12" r="9"/><path d="M12 3v18M3 12h18"/>',
    }[kind]
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" '
            f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')

def darken(c, f=0.78):
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))

def bar_chart(w, h, vals, ymax, ticks, fmt, vcol=False):
    L, R, T, B = 46, 14, 26, 46
    pw, ph = w - L - R, h - T - B
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    for t in ticks:
        y = T + ph - ph * t / ymax
        s += f'<line x1="{L}" x2="{w-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="#e3e6ec"/>'
        s += f'<text x="{L-8}" y="{y+4:.1f}" font-size="13" text-anchor="end" fill="#333">{t}</text>'
    s += f'<line x1="{L}" x2="{L}" y1="{T}" y2="{T+ph}" stroke="#555"/>'
    gw = pw / 5
    for i, v in enumerate(vals):
        bw = gw * 0.62; x = L + gw * i + (gw - bw) / 2
        bh = ph * v / ymax; y = T + ph - bh
        c = PL[i]["c"]
        s += (f'<defs><linearGradient id="g{w}{h}{i}{ymax}" x1="0" y1="0" x2="0" y2="1">'
              f'<stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="{darken(c)}"/></linearGradient></defs>')
        s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(bh,3):.1f}" rx="3" fill="url(#g{w}{h}{i}{ymax})"/>'
        lc = darken(c, .85) if vcol else "#14264f"
        s += (f'<text x="{x+bw/2:.1f}" y="{y-6:.1f}" font-size="14" font-weight="700" '
              f'text-anchor="middle" fill="{lc}">{fmt(v)}</text>')
        s += (f'<text x="{x+bw/2:.1f}" y="{T+ph+19}" font-size="{12.5 if w>420 else 10.5}" text-anchor="middle" fill="#222" font-weight="500">{PL[i]["n1"]}</text>'
              f'<text x="{x+bw/2:.1f}" y="{T+ph+34}" font-size="{12.5 if w>420 else 10.5}" text-anchor="middle" fill="#222" font-weight="500">{PL[i]["n2"]}</text>')
    return s + '</svg>'


def logo(sz=104):
    if BRAND.get("logo"):
        return f'<img src="{BRAND["logo"]}" style="width:{sz}px;height:{sz}px;object-fit:contain">'
    pts = []
    for i in range(24):
        a = i * math.pi * 2 / 24 - math.pi / 2
        r = 48 if i % 2 == 0 else 36
        pts.append(f"{50 + r * math.cos(a):.1f},{50 + r * math.sin(a):.1f}")
    ini = BRAND.get("initials", "T")
    return (f'<svg width="{sz}" height="{sz}" viewBox="0 0 100 100"><polygon points="{" ".join(pts)}" fill="#d0021b"/>'
            f'<circle cx="50" cy="50" r="30" fill="#14264f"/><text x="50" y="{50 + (9 if len(ini) < 3 else 7)}" font-size="{26 if len(ini) < 3 else 20}" font-weight="900" '
            f'font-style="italic" text-anchor="middle" fill="#fff" font-family="Inter">{ini}</text></svg>')

def header(title, sub, scale=1.0):
    ts = "font-size:17px" if len(title) > 24 and scale == 1.0 and False else ""
    return f'''<div class="hdr"><div class="brand">{logo(104)}<div class="vsep"></div>
<div><div class="bt" style="font-size:{min(50, int(400 / (0.66 * max(len(BRAND["name"]), 1))))}px">{BRAND["name"]}</div><div class="bs">{BRAND["sub"]}</div></div></div>
<div class="rt"><div class="badge"><span>{title}</span></div><div class="subline"><i></i><b>{sub}</b><i></i></div></div></div>'''

def panel(title, ic, body, cls="", style=""):
    return (f'<div class="panel {cls}" style="{style}"><div class="ph"><span class="phi">{icon(ic, "#fff", 24)}</span>'
            f'<span>{title}</span></div><div class="pb">{body}</div></div>')

def footer_bar(left, page=None):
    pg = f'<div class="pg">Page {page} / 7</div>' if page else ''
    return f'<div class="fbar"><div class="fl"></div><div class="fc">{left}</div>{pg}<div class="fr"></div></div>'

def note_box(ic="note"):
    return (f'<div class="note"><div class="nt">{icon(ic, NAVY, 22)}<b>Note :</b></div>'
            f'<div class="nl"></div><div class="nl"></div><div class="nl"></div></div>')

def silhouette():
    return '''<svg viewBox="0 0 100 100" width="100%" height="100%" preserveAspectRatio="xMidYMax slice">
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dbe9f6"/><stop offset="1" stop-color="#f2f6fa"/></linearGradient></defs>
<rect width="100" height="100" fill="url(#sky)"/>
<circle cx="50" cy="40" r="17" fill="#c4ccd8"/>
<path d="M14 100 Q16 66 50 62 Q84 66 86 100Z" fill="#c4ccd8"/>
<text x="50" y="92" font-size="7" text-anchor="middle" fill="#7d8797" font-family="Inter" font-weight="600">PLAYER PHOTO</text></svg>'''

CSS = f'''
@page p1 {{ size:1024px 1536px; margin:0 }}
@page p2 {{ size:777px 1024px; margin:0 }}
* {{ box-sizing:border-box; margin:0; padding:0 }}
body {{ font-family:'Inter',sans-serif; color:#14264f; -webkit-print-color-adjust:exact; print-color-adjust:exact }}
.page {{ position:relative; overflow:hidden; background:#fbfcfe; break-after:page }}
.big {{ page:p1; width:1024px; height:1536px; padding:16px 22px }}
.wrap {{ page:p1; width:1024px; height:1536px; overflow:hidden; break-after:page; background:#fbfcfe; position:relative }}
.small {{ width:777px; height:1165px; padding:12px 16px; position:relative; transform:scale(1.31789); transform-origin:0 0; overflow:hidden }}
.hdr {{ display:flex; justify-content:space-between; align-items:flex-start; padding-bottom:14px; border-bottom:2px solid {RED}; position:relative }}
.brand {{ display:flex; align-items:center; gap:14px }}
.vsep {{ width:3px; height:92px; background:{NAVY} }}
.bt {{ font-size:50px; font-weight:900; letter-spacing:1px; line-height:1; color:{NAVY} }}
.bs {{ font-size:25px; font-weight:700; color:#6c7380; letter-spacing:.5px; margin-top:6px }}
.rt {{ width:430px; margin-top:2px }}
.badge {{ background:{NAVY}; color:#fff; transform:skewX(-12deg); border-radius:14px 0 0 0; padding:15px 22px; text-align:center; border-top-right-radius:14px; box-shadow:5px 0 0 {NAVY} }}
.badge span {{ display:inline-block; transform:skewX(12deg); font-style:italic; font-weight:800; font-size:24.5px;white-space:nowrap; letter-spacing:.5px }}
.subline {{ display:flex; align-items:center; gap:14px; margin-top:12px }}
.subline i {{ flex:1; height:2px; background:{RED} }}
.subline b {{ letter-spacing:7px; font-size:20px; font-weight:700 }}
.small .bt {{ font-size:38px }} .small .bs {{ font-size:19px }} .small .vsep {{ height:62px }}
.small .rt {{ width:305px }} .small .badge {{ padding:11px 14px }} .small .badge span {{ font-size:22px }}
.small .badge span.sm {{ font-size:16.5px }} .small .subline b {{ font-size:17px; letter-spacing:3px }}
.small .hdr svg:first-child {{ width:72px; height:72px }} .small .hdr {{ padding-bottom:8px }}
.panel {{ border:1.5px solid #c6cfe0; border-radius:10px; background:#fff; overflow:hidden; box-shadow:0 1px 3px rgba(20,38,79,.1) }}
.ph {{ background:{NAVY}; color:#fff; font-weight:700; font-size:21px; padding:9px 14px; display:flex; align-items:center; gap:12px; border-bottom-right-radius:26px; width:100% }}
.pb {{ padding:6px 8px 4px }}
.small .ph {{ font-size:16px; padding:6px 12px }}
.cards {{ display:flex; gap:6px; margin-top:14px }}
.card {{ flex:1; border-radius:18px; overflow:hidden; color:#fff; text-align:center; box-shadow:0 2px 4px rgba(0,0,0,.18) }}
.card .nm {{ font-style:italic; font-weight:800; font-size:21px; line-height:1.05; padding:11px 4px 8px }}
.card .ph1 {{ margin:0 6px; height:128px; background:#e9f0f7; border-radius:12px; overflow:hidden }}
.card .tag {{ font-weight:800; font-size:21px; padding:8px 0 7px }}
.stats {{ margin-top:12px; border:1px solid #cfd6e4; border-radius:6px; overflow:hidden }}
.srow {{ display:grid; grid-template-columns:158px repeat(5,1fr); height:37.5px; align-items:center; text-align:center; font-weight:600; font-size:19.5px }}
.srow .lab {{ background:{NAVY}; color:#fff; height:100%; display:flex; align-items:center; gap:10px; padding-left:14px; font-size:16.5px; font-weight:600; text-align:left; border-top:1px solid #2a3c69 }}
.srow div.c {{ height:100%; display:flex; align-items:center; justify-content:center; border-left:2px solid; }}
.row2 {{ display:flex; gap:14px; margin-top:12px }}
.tbl {{ margin-top:18px; border:1px solid #cfd6e4; border-radius:10px; overflow:hidden; background:#fff }}
.tbl table {{ width:100%; border-collapse:collapse }}
.tbl th {{ background:{NAVY}; color:#fff; font-size:16px; font-weight:600; padding:9px 4px; border-left:1px solid #34476f; line-height:1.15 }}
.tbl th svg {{ display:block; margin:0 auto 4px }}
.tbl td {{ text-align:center; font-size:19px; font-weight:600; padding:9px 4px; border-bottom:1px solid #e1e6f0 }}
.tbl tr:nth-child(even) td {{ background:#f2f6fc }}
.tbl td.nm {{ text-align:left; font-weight:700; padding-left:16px }}
.strip {{ width:7px; padding:0 !important }}
.note {{ border:2px solid {NAVY}; border-radius:14px; margin-top:22px; background:#fff; height:170px; position:relative; padding:46px 24px 0 }}
.note .nt {{ position:absolute; left:-2px; top:-2px; background:{NAVY}; color:#fff; border-top-left-radius:12px; padding:9px 46px 9px 14px; font-size:27px; display:flex; gap:12px; align-items:center; clip-path:polygon(0 0,100% 0,88% 100%,0 100%) }}
.note .nt svg {{ stroke:#fff }}
.nl {{ border-bottom:1px solid #d6dae2; height:29px }}
.small .note {{ height:92px; padding:7px 20px 0; margin-top:4px; border-radius:12px; border-color:#c6cfe0; background:#f1f3f8 }}
.small .note .nt {{ position:static; background:none; color:{NAVY}; clip-path:none; padding:0 0 6px; font-size:19px }}
.small .note .nt svg {{ stroke:{NAVY} }}
.small .note .nl {{ height:21px; border-bottom:1px dotted #8a93a6 }}
.small .note .nl:nth-of-type(3) {{ display:none }}
.fbar {{ position:absolute; left:0; right:0; bottom:0; height:44px; background:{NAVY}; color:#fff; display:flex; align-items:center; justify-content:center }}
.fbar .fc {{ font-weight:600; letter-spacing:4px; font-size:17px }}
.fbar .fl {{ position:absolute; left:0; top:0; bottom:0; width:70px; background:repeating-linear-gradient(115deg,{RED} 0 7px,#fff 7px 12px,{NAVY} 12px 24px) }}
.fbar .fr {{ position:absolute; right:0; top:0; bottom:0; width:70px; background:repeating-linear-gradient(65deg,{RED} 0 7px,#fff 7px 12px,{NAVY} 12px 24px) }}
.fbar .pg {{ position:absolute; right:84px; top:4px; bottom:4px; background:{RED}; color:#fff; font-weight:800; font-size:14px; padding:0 20px; display:flex; align-items:center; border-radius:4px; transform:skewX(-14deg) }}
.sbar {{ position:absolute; left:0; right:0; bottom:0; height:60px; background:linear-gradient(90deg,{NAVY} 0 70%,{RED} 70% 71.3%,#fff 71.3% 72.4%,{NAVY} 72.4%); display:flex; align-items:center; justify-content:center; color:#fff; font-size:19px; letter-spacing:6px; font-weight:600 }}
.cmp {{ margin-top:10px }}
.cmp .panel {{ margin-bottom:9px }}
.ctab {{ width:100%; border-collapse:collapse }}
.ctab th {{ color:#fff; font-size:16px; font-weight:700; padding:8px 2px; line-height:1.1; border-left:2px solid #fff }}
.ctab th.st {{ background:{NAVY}; font-size:19px; border-left:none }}
.ctab td {{ text-align:center; font-size:17px; font-weight:700; padding:8px 2px; border-bottom:1px solid #e1e6f0; border-left:1px solid #e6eaf1 }}
.ctab td.m {{ text-align:left; font-weight:600; padding-left:12px; width:196px }}
.ctab td.m span {{ display:inline-flex; align-items:center; gap:10px }}
.ctab tr:nth-child(even) td {{ background:#f7f9fc }}
.top4 {{ display:grid; grid-template-columns:repeat(4,1fr); gap:8px; padding:10px 8px 8px }}
.tp {{ border-radius:9px; text-align:center; border:2px solid; overflow:hidden }}
.tp .t {{ color:#fff; font-weight:700; font-size:15px; padding:6px 2px }}
.tp .v {{ font-size:34px; font-weight:800; padding:2px 0 0 }}
.tp .w {{ font-size:13px; font-weight:600; padding:0 4px 7px; color:#222 }}
.kpis {{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:12px }}
.kpi {{ border-radius:12px; padding:9px 8px 8px; text-align:center; color:#fff; background:{NAVY} }}
.kpi b {{ display:block; font-size:26px; font-weight:800 }} .kpi span {{ font-size:13px; letter-spacing:1px; opacity:.85 }}
.metric {{ display:flex; align-items:center; gap:16px; padding:10px 18px }}
.metric .mi {{ width:70px }} .metric .mb {{ flex:1 }}
.metric .mt {{ display:flex; justify-content:space-between; align-items:flex-end }}
.metric .mt b {{ font-size:32px; font-weight:800 }}
.metric .mt div {{ font-size:20px; font-weight:700 }} .metric .mt small {{ display:block; font-size:14px; font-weight:500 }}
.meter {{ height:13px; border-radius:7px; background:#dfe1e6; margin-top:10px }} .meter i {{ display:block; height:100%; border-radius:7px }}
.ins {{ background:#e9ebf2; border-radius:0 40px 40px 0; padding:12px 26px; margin-top:12px; width:735px; display:flex; gap:16px }}
.ins h3 {{ font-size:27px; font-weight:800 }} .ins li {{ list-style:none; font-size:17px; margin-top:7px; padding-left:22px; position:relative }}
.ins li:before {{ content:''; position:absolute; left:3px; top:7px; width:9px; height:9px; border-radius:50%; background:{RED} }}
.legend div {{ display:flex; align-items:center; gap:10px; font-size:15px; margin:8px 0 }} .legend i {{ width:16px; height:16px; border-radius:50% }}
'''

# ---- extra pages: Defense / Receiving / Rushing (exec'd from make_report.py) ----
NEWCSS = """
.hero{position:relative;border-radius:18px;overflow:hidden;color:#fff;height:184px;margin-top:16px;box-shadow:0 2px 6px rgba(0,0,0,.22)}
.hero .yl{position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.08) 0 3px,transparent 3px 64px)}
.hero .hnum{position:absolute;right:230px;top:-34px;font-size:230px;font-weight:900;font-style:italic;color:rgba(255,255,255,.10);line-height:1}
.hero .hl{position:absolute;left:28px;top:20px}
.hero .kick{font-size:13.5px;letter-spacing:3px;font-weight:700;opacity:.85}
.hero .hname{font-size:42px;font-weight:900;font-style:italic;line-height:1.05;margin-top:6px}
.hero .hpos{font-size:19px;font-weight:700;opacity:.92;margin-top:4px}
.hero .hbig{position:absolute;right:34px;top:18px;text-align:right}
.hero .hbig b{display:block;font-size:92px;font-weight:900;line-height:.95}
.hero .hbig span{font-size:14px;letter-spacing:2px;font-weight:700;opacity:.92}
.hero .chips{position:absolute;left:28px;bottom:16px;display:flex;gap:10px}
.hero .chip{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.38);border-radius:999px;padding:5px 15px;font-size:14.5px;font-weight:600}
.hero .chip b{font-size:19px;margin-right:6px;font-weight:800}
.big .kpi{padding:12px 8px 10px}.big .kpi b{font-size:34px}.big .kpi span{font-size:13.5px}
.insb{background:#e9ebf2;border-radius:16px;padding:16px 22px;height:100%;display:flex;gap:14px}
.insb h3{font-size:24px;font-weight:800}
.insb li{list-style:none;font-size:15.5px;margin-top:7px;padding-left:20px;position:relative;line-height:1.3}
.insb li:before{content:'';position:absolute;left:2px;top:6px;width:9px;height:9px;border-radius:50%;background:#d0021b}
.note2{border:2px solid #14264f;border-radius:14px;background:#fff;height:100%;padding:12px 20px}
.note2 .nt2{display:flex;align-items:center;gap:10px;font-size:22px;font-weight:800;color:#14264f}
.note2 .nl{border-bottom:1px solid #d6dae2;height:28px}
.db{position:relative;height:26px;background:#eef1f7;border-radius:6px;overflow:hidden;text-align:left}
.db i{position:absolute;left:0;top:0;bottom:0;opacity:.30}
.db span{position:relative;padding-left:10px;line-height:26px;font-weight:700;font-size:17px}
.legend b{font-weight:800;min-width:54px;display:inline-block}
.cap{font-size:12.5px;color:#5b6477;padding:2px 10px 8px;line-height:1.35}
""".replace("@NAVY", NAVY)

GOLD = "#f2b705"
FLD = dict(flags="#8d97aa", ints="#14264f", sacks="#d9091f", pbu="#f2a900", td="#3a9a2c")
nm = lambda p: p["n1"] + " " + p["n2"]

def star_gold(sz=16):
    return (f'<svg width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="{GOLD}" stroke="#c98f00" stroke-width="1" '
            f'style="vertical-align:-2px;margin-left:6px"><path d="M12 2l3 7 7 .7-5.3 4.8 1.6 7.2L12 18l-6.3 3.7 1.6-7.2L2 9.7 9 9z"/></svg>')

def hero(p, kicker, big, biglabel, chips):
    c = p["c"]
    ch = "".join(f'<div class="chip"><b>{v}</b>{l}</div>' for v, l in chips)
    return (f'<div class="hero" style="background:linear-gradient(115deg,{darken(c,.42)} 0%,{darken(c,.75)} 45%,{c} 100%)">'
            f'<div class="yl"></div><div class="hnum">#{p["num"]}</div>'
            f'<div class="hl"><div class="kick">{kicker}</div><div class="hname">{nm(p)}</div><div class="hpos">#{p["num"]} • {p["pos"]}</div></div>'
            f'<div class="hbig"><b>{big}</b><span>{biglabel}</span></div><div class="chips">{ch}</div></div>')

def kpis(items):
    out = f'<div class="kpis" style="grid-template-columns:repeat({len(items)},1fr)">'
    for i, (v, l) in enumerate(items):
        bg = f' style="background:{RED}"' if i % 2 else ''
        out += f'<div class="kpi"{bg}><b>{v}</b><span>{l}</span></div>'
    return out + '</div>'

def insights2(items):
    li = "".join(f"<li>{t}</li>" for t in items)
    return f'<div class="insb"><div>{icon("bulb", GOLD, 44)}</div><div><h3>Key Insights</h3><ul>{li}</ul></div></div>'

def bottom_row(items):
    return (f'<div class="row2" style="margin-top:14px;align-items:stretch;height:172px"><div style="flex:1.55">{insights2(items)}</div>'
            f'<div style="flex:1"><div class="note2"><div class="nt2">{icon("note", NAVY, 24)}Note :</div>'
            f'<div class="nl"></div><div class="nl"></div><div class="nl"></div></div></div></div>')

# ---------- charts ----------
def grouped(w, h, series, ymax, ticks):
    L, R, T, B = 40, 12, 42, 46
    pw, ph = w - L - R, h - T - B
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    x = L
    for name, col, _ in series:
        s += f'<rect x="{x}" y="10" width="13" height="13" rx="3" fill="{col}"/><text x="{x+19}" y="21.5" font-size="13" font-weight="600" fill="#222">{name}</text>'
        x += 19 + len(name) * 7.8 + 18
    for t in ticks:
        y = T + ph - ph * t / ymax
        s += f'<line x1="{L}" x2="{w-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="#e3e6ec"/><text x="{L-8}" y="{y+4:.1f}" font-size="13" text-anchor="end" fill="#333">{t}</text>'
    s += f'<line x1="{L}" x2="{L}" y1="{T}" y2="{T+ph}" stroke="#555"/>'
    gw = pw / 5; n = len(series); bw = gw * 0.8 / n
    for i, p in enumerate(PL):
        for k, (name, col, vals) in enumerate(series):
            v = vals[i]; bx = L + gw * i + gw * 0.1 + k * bw; bh = ph * v / ymax
            s += f'<rect x="{bx:.1f}" y="{T+ph-bh:.1f}" width="{bw-2:.1f}" height="{max(bh,2):.1f}" rx="2.5" fill="{col}"/>'
            if v > 0:
                s += f'<text x="{bx+bw/2-1:.1f}" y="{T+ph-bh-5:.1f}" font-size="12" font-weight="700" text-anchor="middle" fill="#14264f">{v}</text>'
        cx = L + gw * i + gw / 2
        s += f'<text x="{cx:.1f}" y="{T+ph+17}" font-size="12.5" font-weight="500" text-anchor="middle" fill="#222">{p["n1"]}</text>'
        s += f'<text x="{cx:.1f}" y="{T+ph+31}" font-size="12.5" font-weight="500" text-anchor="middle" fill="#222">{p["n2"]}</text>'
    return s + '</svg>'

def stacked_h(w, h, rows, maxv, ticks, legend):
    L, R, T, B = 170, 48, 8, 62
    pw = w - L - R; rowh = (h - T - B) / len(rows)
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    for t in ticks:
        x = L + pw * t / maxv
        s += f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{T}" y2="{h-B}" stroke="#e3e6ec"/><text x="{x:.1f}" y="{h-B+16}" font-size="12.5" text-anchor="middle" fill="#333">{t}</text>'
    for ri, (pi, segs, total) in enumerate(rows):
        y = T + ri * rowh + rowh * 0.17; bh = rowh * 0.66; p = PL[pi]
        s += f'<circle cx="12" cy="{y+bh/2:.1f}" r="6" fill="{p["c"]}"/><text x="26" y="{y+bh/2+5:.1f}" font-size="14" font-weight="700" fill="#14264f">{nm(p)}</text>'
        x = L
        for v, c in segs:
            if v <= 0: continue
            wd = pw * v / maxv
            s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{wd-1.5:.1f}" height="{bh:.1f}" fill="{c}"/>'
            x += wd
        s += f'<text x="{x+7:.1f}" y="{y+bh/2+6:.1f}" font-size="17" font-weight="800" fill="#14264f">{total}</text>'
    lx = 12
    for name, c in legend:
        s += f'<rect x="{lx}" y="{h-22}" width="12" height="12" rx="3" fill="{c}"/><text x="{lx+17}" y="{h-12}" font-size="12.5" font-weight="600" fill="#222">{name}</text>'
        lx += 17 + len(name) * 7.4 + 14
    return s + '</svg>'

def donut_multi(sz, vals, c1, c2):
    tot = sum(vals) or 1; r = sz * 0.36; cx = cy = sz / 2; sw = sz * 0.16; circ = 2 * math.pi * r
    s = f'<svg width="{sz}" height="{sz}" viewBox="0 0 {sz} {sz}" font-family="Inter"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#eef0f4" stroke-width="{sw}"/>'
    cum = 0
    for i, v in enumerate(vals):
        if v <= 0: continue
        ln = circ * v / tot
        s += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{PL[i]["c"]}" stroke-width="{sw}" '
              f'stroke-dasharray="{max(ln-2.5,0.5):.1f} {circ:.1f}" stroke-dashoffset="{-cum:.1f}" transform="rotate(-90 {cx} {cy})"/>')
        cum += ln
    s += (f'<text x="{cx}" y="{cy+8}" font-size="{sz*0.19:.0f}" font-weight="800" text-anchor="middle" fill="{NAVY}">{c1}</text>'
          f'<text x="{cx}" y="{cy+sz*0.15:.0f}" font-size="13" font-weight="600" text-anchor="middle" fill="#5b6477">{c2}</text>')
    return s + '</svg>'

def share_panel_body(vals, c1, c2, sz=200):
    tot = sum(vals) or 1
    leg = "".join(f'<div><i style="background:{PL[i]["c"]}"></i><b>{vals[i]/tot*100:.1f}%</b>{nm(PL[i])}</div>' for i in range(5))
    return f'<div style="display:flex;align-items:center;gap:14px;padding:8px 10px">{donut_multi(sz, vals, c1, c2)}<div class="legend">{leg}</div></div>'

def lollipop_h(w, h, vals, vmax, ticks, fmt):
    L, R, T, B = 148, 56, 8, 30
    pw = w - L - R; order = sorted(range(5), key=lambda i: -vals[i]); rowh = (h - T - B) / 5
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    for t in ticks:
        x = L + pw * t / vmax
        s += f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{T}" y2="{h-B}" stroke="#e3e6ec"/><text x="{x:.1f}" y="{h-B+17}" font-size="12.5" text-anchor="middle" fill="#333">{t}</text>'
    for r, i in enumerate(order):
        y = T + r * rowh + rowh / 2; x = L + pw * vals[i] / vmax; c = PL[i]["c"]
        s += f'<text x="{L-12}" y="{y+5:.1f}" font-size="14" font-weight="700" text-anchor="end" fill="#14264f">{nm(PL[i])}</text>'
        s += f'<line x1="{L}" x2="{x:.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{c}" stroke-width="5" stroke-linecap="round"/>'
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{c}" stroke="#fff" stroke-width="3"/>'
        s += f'<text x="{x+19:.1f}" y="{y+5.5:.1f}" font-size="16" font-weight="800" fill="#14264f">{fmt(vals[i])}</text>'
    return s + '</svg>'

def lanes(w, vals, vmax, step):
    LX, ez, R, T, lh, gap = 170, 34, 18, 28, 35, 7
    h = T + 5 * (lh + gap) + 6; x0 = LX + ez; pw = w - R - x0
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    for r, i in enumerate(sorted(range(5), key=lambda k: -vals[k])):
        y = T + r * (lh + gap); p = PL[i]
        s += f'<circle cx="12" cy="{y+lh/2:.1f}" r="6" fill="{p["c"]}"/><text x="26" y="{y+lh/2+5:.1f}" font-size="14.5" font-weight="700" fill="#14264f">{nm(p)}</text>'
        s += f'<rect x="{LX}" y="{y}" width="{w-R-LX}" height="{lh}" rx="6" fill="{"#2f7d36" if r%2==0 else "#297030"}"/>'
        s += f'<rect x="{LX}" y="{y}" width="{ez}" height="{lh}" rx="6" fill="{NAVY}"/><rect x="{LX+ez-8}" y="{y}" width="8" height="{lh}" fill="{NAVY}"/>'
        s += f'<text x="{LX+ez/2}" y="{y+lh/2+4}" font-size="10" font-weight="800" text-anchor="middle" fill="#fff" transform="rotate(-90 {LX+ez/2} {y+lh/2})">LIONS</text>'
        for t in range(0, vmax + 1, step):
            x = x0 + pw * t / vmax
            if t > 0: s += f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y}" y2="{y+lh}" stroke="#fff" stroke-opacity=".55" stroke-width="{2 if t%(step*2)==0 else 1}"/>'
        ln = pw * vals[i] / vmax
        s += f'<rect x="{x0:.1f}" y="{y+8}" width="{max(ln,4):.1f}" height="{lh-16}" rx="9" fill="{p["c"]}" stroke="#fff" stroke-width="2"/>'
        ex = x0 + ln
        s += (f'<g transform="translate({ex:.1f},{y+lh/2:.1f}) rotate(-20)"><ellipse rx="15" ry="9.5" fill="#8a4b1d" stroke="#fff" stroke-width="1.6"/>'
              f'<path d="M-6 0H6 M-3 -3V3 M0 -3V3 M3 -3V3" stroke="#fff" stroke-width="1.2"/></g>')
        lab = f'{vals[i]} yds'
        if ln > 90: s += f'<text x="{x0+12:.1f}" y="{y+lh/2+6:.1f}" font-size="16" font-weight="800" fill="#fff">{lab}</text>'
        else: s += f'<text x="{ex+24:.1f}" y="{y+lh/2+6:.1f}" font-size="16" font-weight="800" fill="#fff">{lab}</text>'
    for t in range(0, vmax + 1, step * 2):
        s += f'<text x="{x0+pw*t/vmax:.1f}" y="18" font-size="12.5" font-weight="700" text-anchor="middle" fill="#14264f">{t}</text>'
    return s + '</svg>'

# ---------- tables ----------
def heat_table(cols):
    t = (f'<div class="tbl" style="margin-top:16px"><table><tr><th class="strip" style="background:{NAVY}"></th>'
         f'<th style="text-align:left;padding-left:16px;font-size:20px;width:210px">Player</th>')
    for name, ic, vals in cols:
        t += f'<th>{icon(ic, "#fff", 28)}{name}</th>'
    t += '</tr>'
    for i, p in enumerate(PL):
        t += f'<tr><td class="strip" style="background:{p["c"]}"></td><td class="nm">{nm(p)}</td>'
        for name, ic, vals in cols:
            v = vals[i]; mx = max(vals)
            if mx == 0:
                bg, fg, extra = "rgba(58,154,44,.13)", "#2b7a20", ""
            else:
                a = 0.05 + 0.82 * v / mx; bg = f"rgba(20,38,79,{a:.2f})"; fg = "#fff" if a > 0.5 else NAVY
                extra = star_gold() if v == mx else ""
            t += f'<td style="background:{bg};color:{fg};font-size:22px;font-weight:800;padding:9px 4px">{v}{extra}</td>'
        t += '</tr>'
    return t + '</table></div>'

def bar_table(cols, team):
    t = (f'<div class="tbl" style="margin-top:16px"><table><tr><th class="strip" style="background:{NAVY}"></th>'
         f'<th style="text-align:left;padding-left:16px;font-size:20px;width:210px">Player</th>')
    for name, ic, vals, fm in cols:
        t += f'<th>{icon(ic, "#fff", 28)}{name}</th>'
    t += '</tr>'
    for i, p in enumerate(PL):
        t += f'<tr><td class="strip" style="background:{p["c"]}"></td><td class="nm" style="padding:6px 4px 6px 16px">{nm(p)}</td>'
        for name, ic, vals, fm in cols:
            w_ = 100 * vals[i] / (max(vals) or 1)
            t += f'<td style="padding:6px 10px"><div class="db"><i style="width:{w_:.1f}%;background:{p["c"]}"></i><span>{fm(vals[i])}</span></div></td>'
        t += '</tr>'
    t += f'<tr><td class="strip" style="background:{NAVY}"></td><td style="background:{NAVY};color:#fff;text-align:left;padding:8px 4px 8px 16px;font-weight:800">TEAM</td>'
    for v in team:
        t += f'<td style="background:{NAVY};color:#fff;font-weight:800;padding:8px 4px">{v}</td>'
    return t + '</tr></table></div>'

def foot(n):
    return footer_bar(f'{BRAND["name"]} &nbsp;|&nbsp; TEAM REPORT', n)

# ---- redesigned pages 1, 2 + all-purpose + overall comparison (exec'd after new_pages.py) ----
BLUE = "#1f6fd6"; GREEN = "#3a9a2c"; AMBER = "#f2a900"

def radar_n(W, H, R, axes, series, font=11, dots=3.0, fill=0.16):
    n = len(axes); cx = W / 2; cy = H / 2 + 4
    def pt(i, f):
        a = math.radians(-90 + 360 * i / n); return cx + R * f * math.cos(a), cy + R * f * math.sin(a)
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter">'
    for lvl in (0.2, 0.4, 0.6, 0.8, 1.0):
        s += f'<polygon points="{" ".join("%.1f,%.1f" % pt(i, lvl) for i in range(n))}" fill="none" stroke="#d7dbe4"/>'
    for i in range(n):
        x, y = pt(i, 1); s += f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#d7dbe4"/>'
    for color, vals in series:
        s += (f'<polygon points="{" ".join("%.1f,%.1f" % pt(i, v / 100) for i, v in enumerate(vals))}" '
              f'fill="{color}" fill-opacity="{fill}" stroke="{color}" stroke-width="2"/>')
        for i, v in enumerate(vals):
            x, y = pt(i, v / 100); s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{dots}" fill="{color}"/>'
    for i, t in enumerate(axes):
        a = math.radians(-90 + 360 * i / n); c_, s_ = math.cos(a), math.sin(a)
        x = cx + (R + 11) * c_; y = cy + (R + 11) * s_
        anc = "middle" if abs(c_) < 0.25 else ("start" if c_ > 0 else "end")
        lines = t.split("\n"); y0 = y + (4 if abs(s_) < 0.4 else (13 if s_ > 0 else -4 - 13 * (len(lines) - 1)))
        for j, line in enumerate(lines):
            s += f'<text x="{x:.1f}" y="{y0+j*13:.1f}" font-size="{font}" font-weight="600" text-anchor="{anc}" fill="#222">{line}</text>'
    return s + '</svg>'

def heat2(cols, avg=None, first="Player", fs=21, pad=8, mt=14):
    t = (f'<div class="tbl" style="margin-top:{mt}px"><table><tr><th class="strip" style="background:{NAVY}"></th>'
         f'<th style="text-align:left;padding-left:16px;font-size:20px;width:196px">{first}</th>')
    for c in cols:
        t += f'<th>{icon(c["ic"], "#fff", 26)}{c["n"]}</th>'
    t += '</tr>'
    for i, p in enumerate(PL):
        t += f'<tr><td class="strip" style="background:{p["c"]}"></td><td class="nm">{nm(p)}</td>'
        for c in cols:
            if c["b"] == "text":
                t += f'<td style="font-size:{fs-3}px;font-weight:800;color:{p["c"]};padding:{pad}px 4px">{c["v"][i]}</td>'; continue
            vs = c["v"]; lo, hi = min(vs), max(vs); v = vs[i]
            tt = 0 if hi == lo else ((v - lo) / (hi - lo) if c["b"] == "high" else (hi - v) / (hi - lo))
            a = 0.06 + 0.8 * tt; fg = "#fff" if a > 0.5 else NAVY
            extra = star_gold() if tt == 1 and hi != lo else ""
            t += f'<td style="background:rgba(20,38,79,{a:.2f});color:{fg};font-size:{fs}px;font-weight:800;padding:{pad}px 4px">{c["f"](v)}{extra}</td>'
        t += '</tr>'
    if avg:
        t += f'<tr><td class="strip" style="background:{NAVY}"></td><td style="background:{NAVY};color:#fff;text-align:left;padding:8px 4px 8px 16px;font-weight:800">TEAM AVG</td>'
        for v in avg:
            t += f'<td style="background:{NAVY};color:#fff;font-weight:800;padding:8px 4px">{v}</td>'
        t += '</tr>'
    return t + '</table></div>'

def lollipop_n(w, h, vals, vmax, ticks, fmt, L=148, R=56):
    pw = w - L - R; T, B = 8, 30; order = sorted(range(5), key=lambda i: -vals[i]); rowh = (h - T - B) / 5
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    for t in ticks:
        x = L + pw * t / vmax
        s += f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{T}" y2="{h-B}" stroke="#e3e6ec"/><text x="{x:.1f}" y="{h-B+17}" font-size="12.5" text-anchor="middle" fill="#333">{t}</text>'
    for r, i in enumerate(order):
        y = T + r * rowh + rowh / 2; x = L + pw * vals[i] / vmax; c = PL[i]["c"]
        s += f'<text x="{L-12}" y="{y+5:.1f}" font-size="14" font-weight="700" text-anchor="end" fill="#14264f">{nm(PL[i])}</text>'
        s += f'<line x1="{L}" x2="{x:.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{c}" stroke-width="5" stroke-linecap="round"/>'
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{c}" stroke="#fff" stroke-width="3"/>'
        s += f'<text x="{x+19:.1f}" y="{y+5.5:.1f}" font-size="15" font-weight="800" fill="#14264f">{fmt(i, vals[i])}</text>'
    return s + '</svg>'

def donut_custom(sz, vals, colors, c1, c2):
    tot = sum(vals) or 1; r = sz * 0.36; cx = cy = sz / 2; sw = sz * 0.16; circ = 2 * math.pi * r
    s = f'<svg width="{sz}" height="{sz}" viewBox="0 0 {sz} {sz}" font-family="Inter"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#eef0f4" stroke-width="{sw}"/>'
    cum = 0
    for v, c in zip(vals, colors):
        ln = circ * v / tot
        s += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="{sw}" '
              f'stroke-dasharray="{max(ln-2.5,0.5):.1f} {circ:.1f}" stroke-dashoffset="{-cum:.1f}" transform="rotate(-90 {cx} {cy})"/>')
        cum += ln
    s += (f'<text x="{cx}" y="{cy+8}" font-size="{sz*0.19:.0f}" font-weight="800" text-anchor="middle" fill="{NAVY}">{c1}</text>'
          f'<text x="{cx}" y="{cy+sz*0.15:.0f}" font-size="13" font-weight="600" text-anchor="middle" fill="#5b6477">{c2}</text>')
    return s + '</svg>'

def race(w, times):
    LX, R, T, lh, gap = 170, 76, 28, 28, 6; lo, hi = 30, 40
    h = T + 5 * (lh + gap) + 4; pw = w - R - LX
    best = min(times)
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    for r, i in enumerate(sorted(range(5), key=lambda k: times[k])):
        y = T + r * (lh + gap); p = PL[i]; pos = 40 * best / times[i]
        s += f'<circle cx="12" cy="{y+lh/2:.1f}" r="6" fill="{p["c"]}"/><text x="26" y="{y+lh/2+5:.1f}" font-size="14.5" font-weight="700" fill="#14264f">{nm(p)}</text>'
        s += f'<rect x="{LX}" y="{y}" width="{pw}" height="{lh}" rx="6" fill="{"#2f7d36" if r%2==0 else "#297030"}"/>'
        for yd in range(lo + 1, hi):
            x = LX + pw * (yd - lo) / (hi - lo)
            s += f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y}" y2="{y+lh}" stroke="#fff" stroke-opacity=".5" stroke-width="{2 if yd%5==0 else 1}"/>'
        s += f'<rect x="{LX+pw-5}" y="{y}" width="5" height="{lh}" fill="#fff"/>'
        ln = pw * (pos - lo) / (hi - lo)
        s += f'<rect x="{LX}" y="{y+7}" width="{ln:.1f}" height="{lh-14}" rx="8" fill="{p["c"]}" stroke="#fff" stroke-width="2"/>'
        ex = LX + ln
        s += (f'<g transform="translate({ex:.1f},{y+lh/2:.1f}) rotate(-20)"><ellipse rx="14" ry="9" fill="#8a4b1d" stroke="#fff" stroke-width="1.6"/>'
              f'<path d="M-5 0H5 M-2.5 -3V3 M0 -3V3 M2.5 -3V3" stroke="#fff" stroke-width="1.2"/></g>')
        s += f'<text x="{LX+12}" y="{y+lh/2+5.5:.1f}" font-size="14.5" font-weight="800" fill="#fff">{pos:.1f} yds</text>'
        s += f'<text x="{w-R+12}" y="{y+lh/2+6:.1f}" font-size="17" font-weight="800" fill="#14264f">{times[i]:.2f} s</text>'
    for yd in range(lo, hi + 1, 2):
        s += f'<text x="{LX+pw*(yd-lo)/(hi-lo):.1f}" y="18" font-size="12.5" font-weight="700" text-anchor="middle" fill="#14264f">{yd}</text>'
    s += f'<text x="{w-R+34}" y="18" font-size="12.5" font-weight="700" fill="#5b6477">time</text>'
    return s + '</svg>'

def funnel(w, h, att, comp, tds):
    att, comp, tds = list(att), list(comp), list(tds)
    stages = [("Pass attempts", sum(att), NAVY), ("Completions", sum(comp), BLUE), ("Passing TDs", sum(tds), "#d9091f")]
    maxw = w * 0.80; cx = w * 0.44; bh, gap, y0 = 46, 34, 10
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    ws = [max(maxw * v / max(stages[0][1], 1), 30) for _, v, _ in stages]
    for k, (lab, v, c) in enumerate(stages):
        y = y0 + k * (bh + gap)
        if k > 0:
            yb = y - gap
            s += f'<polygon points="{cx-ws[k-1]/2:.1f},{yb} {cx+ws[k-1]/2:.1f},{yb} {cx+ws[k]/2:.1f},{y} {cx-ws[k]/2:.1f},{y}" fill="{NAVY}" fill-opacity=".10"/>'
        s += f'<rect x="{cx-ws[k]/2:.1f}" y="{y}" width="{ws[k]:.1f}" height="{bh}" rx="7" fill="{c}"/>'
        if ws[k] > 170:
            s += f'<text x="{cx}" y="{y+bh/2+7:.1f}" font-size="21" font-weight="800" text-anchor="middle" fill="#fff">{v}<tspan font-size="14" font-weight="600" dx="8">{lab}</tspan></text>'
        else:
            s += f'<text x="{cx+ws[k]/2+12:.1f}" y="{y+bh/2+7:.1f}" font-size="21" font-weight="800" fill="{c}">{v}<tspan font-size="14" font-weight="600" fill="#333" dx="8">{lab}</tspan></text>'
    r1 = sum(comp) / sum(att) * 100 if sum(att) else 0; r2 = sum(tds) / sum(comp) * 100 if sum(comp) else 0
    for k, t in enumerate([f"{r1:.1f}% completed", f"{r2:.1f}% of catches = TD"]):
        yy = y0 + (k + 1) * (bh + gap) - gap / 2 + 5
        s += f'<text x="{w-10}" y="{yy:.1f}" font-size="13" font-weight="700" text-anchor="end" fill="#5b6477">{t}</text>'
    return s + '</svg>'

def diverge(w, h, left, right, vmax, ticks):
    L, T, B = 140, 30, 8; pw = w - L - 14; cx = L + pw / 2; u = pw / 2 / vmax; rowh = (h - T - B) / 5
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    for t in ticks:
        for sg in (-1, 1):
            if t == 0 and sg == 1: continue
            x = cx + sg * u * t
            s += f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{T-4}" y2="{h-B}" stroke="#e3e6ec"/>'
    s += f'<line x1="{cx:.1f}" x2="{cx:.1f}" y1="{T-4}" y2="{h-B}" stroke="#555" stroke-width="1.5"/>'
    s += f'<text x="{cx-8:.1f}" y="18" font-size="13" font-weight="800" text-anchor="end" fill="#d9091f">Interceptions</text><text x="{cx+8:.1f}" y="18" font-size="13" font-weight="800" fill="{GREEN}">Touchdowns</text>'
    for i, p in enumerate(PL):
        y = T + i * rowh + rowh * 0.2; bh = rowh * 0.6
        s += f'<text x="{L-12}" y="{y+bh/2+5:.1f}" font-size="14" font-weight="700" text-anchor="end" fill="#14264f">{nm(p)}</text>'
        if right[i] > 0:
            s += f'<rect x="{cx:.1f}" y="{y:.1f}" width="{u*right[i]:.1f}" height="{bh:.1f}" rx="4" fill="{GREEN}"/><text x="{cx+u*right[i]+7:.1f}" y="{y+bh/2+6:.1f}" font-size="16" font-weight="800" fill="{GREEN}">{right[i]}</text>'
        if left[i] > 0:
            s += f'<rect x="{cx-u*left[i]:.1f}" y="{y:.1f}" width="{u*left[i]:.1f}" height="{bh:.1f}" rx="4" fill="#d9091f"/><text x="{cx-u*left[i]-7:.1f}" y="{y+bh/2+6:.1f}" font-size="16" font-weight="800" text-anchor="end" fill="#d9091f">{left[i]}</text>'
        if left[i] == 0 and right[i] == 0:
            s += f'<text x="{cx+8:.1f}" y="{y+bh/2+5:.1f}" font-size="13" fill="#8a93a6">0 / 0</text>'
    return s + '</svg>'

def photo_or_silhouette(p):
    if p.get("photo"):
        return f'<img src="{p["photo"]}" style="width:100%;height:100%;object-fit:cover;object-position:50% 20%">'
    return silhouette()

def pcards():
    out = '<div style="display:flex;gap:6px;margin-top:14px">'
    for p in PL:
        out += (f'<div style="flex:1;border-radius:18px;overflow:hidden;color:#fff;text-align:center;background:{p["c"]};box-shadow:0 2px 4px rgba(0,0,0,.18)">'
                f'<div style="font-style:italic;font-weight:800;font-size:20px;line-height:1.05;padding:9px 4px 7px">{p["n1"]}<br>{p["n2"]}</div>'
                f'<div style="margin:0 6px;height:84px;border-radius:12px;overflow:hidden;background:#e9f0f7">{photo_or_silhouette(p)}</div>'
                f'<div style="font-weight:800;font-size:20px;padding:7px 0 6px">#{p["num"]} • {p["pos"]}</div></div>')
    return out + '</div>'

def small_panel_wrap(inner):
    return inner
