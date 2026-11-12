"""Widgets and charts for the team statistics report (extracted from the approved design)."""
import math
from components import *   # header, panel, icon, foot, CSS, donut_custom, ...
G = "#4caf50"; LR = "#f44336"; GR = "#9aa0ab"; AM = "#f2b705"; OR = "#f57c10"; BL = "#1f8fef"; PU = "#8e24aa"
mt = lambda s: f"{int(s)//60}:{int(s)%60:02d}"

TCSS = """
.tg{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px}
.tg3{grid-template-columns:repeat(3,1fr)}
.tile{background:#fff;border:1.5px solid #dfe4ee;border-radius:14px;padding:11px 8px 10px;text-align:center;box-shadow:0 1px 3px rgba(20,38,79,.08)}
.tile .ic{width:38px;height:38px;border-radius:50%;margin:0 auto 5px;display:flex;align-items:center;justify-content:center}
.tile b{font-size:31px;font-weight:800;display:block;line-height:1.05;color:#14264f}
.tile span{font-size:14px;font-weight:700;color:#14264f}
.tile small{display:block;font-size:12.5px;color:#6b7385;font-weight:600;margin-top:1px}
.tile.h{display:flex;align-items:center;gap:14px;text-align:left;padding:10px 14px}
.tile.h .ic{width:58px;height:58px;margin:0;flex:none}
.tile.h b{font-size:30px}.tile.h span{font-size:16px;display:block}
.banner{position:relative;height:205px;border-radius:18px;overflow:hidden;margin-top:14px;box-shadow:0 2px 6px rgba(0,0,0,.25);background-size:cover;background-position:center}
.banner:after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 35%,rgba(10,16,36,.92) 100%)}
.banner .bn{position:absolute;left:26px;bottom:16px;z-index:2;color:#fff}
.banner .bn b{display:block;font-size:46px;font-weight:900;font-style:italic;line-height:1}
.banner .bn span{font-size:17px;font-weight:600;opacity:.9;letter-spacing:1px}
.banner .rec{position:absolute;right:20px;bottom:16px;z-index:2;color:#fff;text-align:right}
.banner .rec b{display:block;font-size:50px;font-weight:900;line-height:1}
.banner .rec span{font-size:13px;letter-spacing:3px;font-weight:700;opacity:.9}
.mrow{display:grid;grid-template-columns:62px 1fr 140px 90px 100px 100px;align-items:center;gap:6px;background:#fff;border:1.5px solid #dfe4ee;border-radius:14px;padding:10px 14px;margin-top:9px;box-shadow:0 1px 3px rgba(20,38,79,.08)}
.mrow .w{width:44px;height:44px;border-radius:50%;background:#4caf50;color:#fff;font-weight:900;font-size:22px;display:flex;align-items:center;justify-content:center}
.mrow .o b{display:block;font-size:19px;font-weight:800}.mrow .o small{font-size:13px;color:#6b7385;font-weight:600}
.mrow .sc{font-size:30px;font-weight:900;text-align:center;color:#14264f}
.mrow .c{text-align:center;font-size:18px;font-weight:800}.mrow .c small{display:block;font-size:11.5px;color:#6b7385;font-weight:600;letter-spacing:1px}
.mh{display:grid;grid-template-columns:62px 1fr 140px 90px 100px 100px;gap:6px;padding:0 14px;margin-top:12px;font-size:12px;font-weight:800;letter-spacing:1.5px;color:#6b7385}
.mh div:nth-child(n+3){text-align:center}
.sec{display:flex;align-items:center;gap:10px;font-size:22px;font-weight:800;margin-top:16px}
.sec i{width:5px;height:24px;background:#d0021b;display:block}
"""

def tile(val, label, sub, color, ic, h=False):
    return (f'<div class="tile{" h" if h else ""}"><div class="ic" style="background:{color}">{icon(ic, "#fff", 30 if h else 22)}</div>'
            f'<div><b>{val}</b><span>{label}</span><small>{sub}</small></div></div>')

def grid(items, cols=4, h=False):
    return f'<div class="tg{" tg3" if cols == 3 else ""}">' + "".join(tile(*t, h=h) for t in items) + '</div>'

def ring(sz, pct, color, center, sub):
    r = sz * .38; cx = cy = sz / 2; sw = sz * .105; circ = 2 * math.pi * r
    return (f'<svg width="{sz}" height="{sz}" viewBox="0 0 {sz} {sz}" font-family="Inter"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e7e9ee" stroke-width="{sw}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-dasharray="{circ*pct/100:.1f} {circ:.1f}" transform="rotate(-90 {cx} {cy})"/>'
            f'<text x="{cx}" y="{cy+sz*.04:.0f}" font-size="{sz*.2:.0f}" font-weight="900" text-anchor="middle" fill="{NAVY}">{center}</text>'
            f'<text x="{cx}" y="{cy+sz*.17:.0f}" font-size="{sz*.07:.0f}" font-weight="600" text-anchor="middle" fill="#7b8294">{sub}</text></svg>')

def gauge(w, h, pct, color, center, sub, detail):
    cx = w / 2; r = min(w * .38, h * .66); cy = h * .70; sw = 20; L = math.pi * r
    p = f"M {cx-r:.1f} {cy:.1f} A {r:.1f} {r:.1f} 0 0 1 {cx+r:.1f} {cy:.1f}"
    s = (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter"><path d="{p}" fill="none" stroke="#e7e9ee" stroke-width="{sw}" stroke-linecap="round"/>'
         f'<path d="{p}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-dasharray="{L*pct/100:.1f} {L+10:.1f}"/>'
         f'<text x="{cx}" y="{cy-8:.0f}" font-size="42" font-weight="900" text-anchor="middle" fill="{NAVY}">{center}</text>'
         f'<text x="{cx}" y="{cy+16:.0f}" font-size="14" font-weight="700" text-anchor="middle" fill="#14264f">{sub}</text>'
         f'<text x="{cx}" y="{cy+36:.0f}" font-size="13" font-weight="600" text-anchor="middle" fill="#7b8294">{detail}</text>'
         f'<text x="{cx-r:.0f}" y="{cy+22:.0f}" font-size="11" fill="#9aa0ab" text-anchor="middle">0</text><text x="{cx+r:.0f}" y="{cy+22:.0f}" font-size="11" fill="#9aa0ab" text-anchor="middle">100</text></svg>')
    return s

def hrows(w, rows, label_w=96, val_w=46, rh=36):
    # rows: (label, value_text, ratio, color)
    h = rh * len(rows) + 6; bw = w - label_w - val_w - 8
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    for i, (lab, vt, ratio, c) in enumerate(rows):
        y = 4 + i * rh + rh / 2
        s += f'<text x="4" y="{y+6:.1f}" font-size="17" font-weight="500" fill="#14264f">{lab}</text>'
        s += f'<rect x="{label_w}" y="{y-5:.1f}" width="{bw}" height="10" rx="5" fill="#eceef2"/><rect x="{label_w}" y="{y-5:.1f}" width="{max(bw*ratio,10 if ratio>0 else 0):.1f}" height="10" rx="5" fill="{c}"/>'
        s += f'<text x="{w-4}" y="{y+6:.1f}" font-size="18" font-weight="800" text-anchor="end" fill="#14264f">{vt}</text>'
    return s + '</svg>'

def cols_chart(w, h, labels, series, ymax, ticks, avg=None, avg_label=None):
    # series: list of (name,color,vals,valtexts)
    L, R, Tp, B = 40, 14, 34, 28; pw, ph = w - L - R, h - Tp - B
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    x = L
    for nm_, c, _, _ in series:
        if len(series) > 1 or True:
            s += f'<rect x="{x}" y="9" width="13" height="13" rx="3" fill="{c}"/><text x="{x+19}" y="20.5" font-size="13" font-weight="600" fill="#222">{nm_}</text>'; x += 36 + len(nm_) * 7.6
    for t in ticks:
        y = Tp + ph - ph * t / ymax
        s += f'<line x1="{L}" x2="{w-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="#e3e6ec"/><text x="{L-8}" y="{y+4:.1f}" font-size="12.5" text-anchor="end" fill="#333">{t}</text>'
    gw = pw / len(labels); k = len(series); bw = gw * .62 / k
    for i, lab in enumerate(labels):
        for j, (nm_, c, vals, vt) in enumerate(series):
            bx = L + gw * i + (gw - bw * k) / 2 + j * bw; bh = ph * vals[i] / ymax
            s += f'<rect x="{bx:.1f}" y="{Tp+ph-bh:.1f}" width="{bw-3:.1f}" height="{max(bh,2):.1f}" rx="4" fill="{c}"/>'
            s += f'<text x="{bx+bw/2-1.5:.1f}" y="{Tp+ph-bh-6:.1f}" font-size="15" font-weight="800" text-anchor="middle" fill="{NAVY}">{vt[i]}</text>'
        s += f'<text x="{L+gw*i+gw/2:.1f}" y="{Tp+ph+19}" font-size="13" font-weight="700" text-anchor="middle" fill="#222">{lab}</text>'
    if avg is not None:
        y = Tp + ph - ph * avg / ymax
        s += f'<line x1="{L}" x2="{w-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="{RED}" stroke-width="2" stroke-dasharray="6 5"/><line x1="{w-R-92}" x2="{w-R-72}" y1="15" y2="15" stroke="{RED}" stroke-width="2" stroke-dasharray="5 3"/><text x="{w-R}" y="20" font-size="12.5" font-weight="700" text-anchor="end" fill="{RED}">{avg_label}</text>'
    return s + '</svg>'

def bottom_row(items, h=158):
    return (f'<div class="row2" style="margin-top:12px;align-items:stretch;height:{h}px"><div style="flex:2.3">{insights2(items)}</div>'
            f'<div style="flex:1"><div class="note2"><div class="nt2">{icon("note", NAVY, 24)}Note :</div>'
            f'<div class="nl"></div><div class="nl"></div><div class="nl"></div></div></div></div>')


def strip(kicker, big, biglabel, chips, c1=NAVY, c2="#2a4a9a"):
    ch = "".join(f'<div class="chip"><b>{v}</b>{l}</div>' for v, l in chips)
    return (f'<div class="hero" style="height:146px;background:linear-gradient(115deg,{c1} 0%,{c2} 100%)"><div class="yl"></div>'
            f'<div class="hl"><div class="kick">{kicker}</div><div class="hname" style="font-size:38px">{biglabel}</div></div>'
            f'<div class="hbig"><b>{big}</b></div><div class="chips">{ch}</div></div>')


def duel(w, a, b):
    mx = max(a, b, 1); s = f'<svg width="{w}" height="150" viewBox="0 0 {w} 150" font-family="Inter">'
    for i, (lab, v, c) in enumerate([("Takeaways (Def INT)", a, G), ("Giveaways (INT thrown)", b, LR)]):
        y = 8 + i * 66
        s += f'<text x="4" y="{y+14}" font-size="15" font-weight="700" fill="#14264f">{lab}</text><rect x="4" y="{y+24}" width="{w-70}" height="22" rx="8" fill="#eceef2"/>'
        s += f'<rect x="4" y="{y+24}" width="{max((w-70)*v/mx,0):.1f}" height="22" rx="8" fill="{c}"/><text x="{w-6}" y="{y+43}" font-size="24" font-weight="900" text-anchor="end" fill="{c}">{v}</text>'
    return s + '</svg>'


CSS2 = """
.story{background:#fff;border:1.5px solid #dfe4ee;border-left:9px solid #d0021b;border-radius:14px;padding:16px 24px 14px;margin-top:14px;box-shadow:0 1px 4px rgba(20,38,79,.1)}
.story .sk{font-size:13px;font-weight:800;letter-spacing:3px;color:#d0021b}
.story .sh{font-size:30px;font-weight:900;font-style:italic;line-height:1.1;margin-top:4px;color:#14264f}
.story p{font-size:16px;line-height:1.5;color:#2b3550;margin-top:8px}
.story p b{color:#14264f}
.dg{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.dna{display:flex;align-items:center;gap:12px;background:#fff;border:1.5px solid #dfe4ee;border-radius:14px;padding:11px 14px;box-shadow:0 1px 3px rgba(20,38,79,.08)}
.dna .di{width:46px;height:46px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center}
.dna .dt{flex:1}.dna .dt b{display:block;font-size:15.5px;font-weight:800;letter-spacing:.5px;color:#14264f}
.dna .dt span{display:block;font-size:12.8px;line-height:1.3;color:#5b6477;font-weight:500;margin-top:2px}
.dna .dv{font-size:27px;font-weight:900;text-align:right;line-height:1}
.dna .dv small{display:block;font-size:10.5px;font-weight:700;letter-spacing:1px;color:#8a93a6;margin-top:3px}
.lp{padding:8px 12px 6px}
.li{display:flex;gap:12px;align-items:flex-start;margin:9px 0}
.li .n{width:30px;height:30px;border-radius:50%;color:#fff;font-weight:800;font-size:15px;display:flex;align-items:center;justify-content:center;flex:none}
.li b{display:block;font-size:15.5px;font-weight:800;color:#14264f}
.li span{display:block;font-size:13.2px;line-height:1.35;color:#4b556c;margin-top:1px}
.tl{display:flex;gap:10px;margin-top:12px}
.tl div{flex:1;background:#fff;border:1.5px solid #dfe4ee;border-radius:14px;padding:9px 12px;display:flex;align-items:center;gap:10px}
.tl .w{width:34px;height:34px;border-radius:50%;background:#4caf50;color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center;flex:none}
.tl b{display:block;font-size:20px;font-weight:900}.tl span{font-size:12.5px;color:#6b7385;font-weight:600}
.mc{display:grid;grid-template-columns:168px 1fr 372px;gap:0;background:#fff;border:1.5px solid #dfe4ee;border-radius:16px;overflow:hidden;margin-top:12px;box-shadow:0 1px 4px rgba(20,38,79,.1)}
.mc .sb{background:linear-gradient(160deg,#2e7d32,#4caf50);color:#fff;text-align:center;padding:14px 6px}
.mc .sb .r{font-size:13px;font-weight:800;letter-spacing:3px;opacity:.9}.mc .sb .s{font-size:36px;font-weight:900;line-height:1.1;margin-top:4px}
.mc .sb .m{display:inline-block;background:rgba(255,255,255,.2);border-radius:999px;padding:3px 14px;font-weight:800;font-size:16px;margin-top:8px}
.mc .bd{padding:12px 16px}.mc .bd h4{font-size:19px;font-weight:800}.mc .bd p{font-size:14px;line-height:1.4;color:#3c4760;margin-top:5px}
.tag{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.5px;padding:3px 10px;border-radius:999px;margin:7px 6px 0 0;color:#fff}
.cmpc{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:10px 10px 8px}
.cc{border:1.5px solid #dfe4ee;border-radius:12px;overflow:hidden;background:#fff}
.cc .t{padding:7px 12px;color:#fff;font-weight:800;font-size:14px;display:flex;gap:8px;align-items:center}
.cc .b{padding:8px 12px 10px;font-size:13px;line-height:1.38;color:#3c4760}
.cc .b em{display:block;font-style:normal;font-size:11.5px;font-weight:800;letter-spacing:1.5px;color:#d0021b;margin-top:6px}
.cc .b em.g{color:#2e7d32}
.cl{display:grid;grid-template-columns:30px 1fr 150px 74px;gap:10px;align-items:center;padding:7px 14px;border-bottom:1px solid #e9ecf2}
.cl .bx{width:22px;height:22px;border:2.5px solid #14264f;border-radius:6px}
.cl b{font-size:15px;font-weight:700}.cl small{display:block;font-size:12px;color:#6b7385;font-weight:600}
.cl .pg{height:11px;border-radius:6px;background:#eceef2;position:relative}.cl .pg i{position:absolute;left:0;top:0;bottom:0;border-radius:6px}
.cl .tv{font-size:13px;font-weight:800;text-align:right;color:#14264f}
.au{display:grid;grid-template-columns:34px 220px 1fr 78px;gap:10px;align-items:center;padding:8px 14px;border-bottom:1px solid #e9ecf2}
.au .ic{width:28px;height:28px;border-radius:50%;color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center;font-size:16px}
.au b{font-size:14.5px;font-weight:800}.au span{font-size:13px;color:#4b556c;line-height:1.3}
.au .st{font-size:11.5px;font-weight:800;letter-spacing:1px;text-align:center;padding:4px 0;border-radius:6px}
.gl{display:grid;grid-template-columns:1fr 1fr;gap:6px 18px;padding:10px 14px}
.gl div{font-size:13px;line-height:1.35;color:#3c4760;border-bottom:1px dashed #d6dae2;padding-bottom:5px}.gl b{color:#14264f;font-weight:800}
.cf{display:grid;grid-template-columns:170px 1fr 210px;gap:10px;align-items:center;padding:6px 14px}
.cf b{font-size:14.5px;font-weight:700}.cf small{font-size:12.5px;color:#6b7385;font-weight:600}
.cfb{display:flex;gap:4px}.cfb i{flex:1;height:14px;border-radius:4px;background:#e4e7ee}
"""

def story(kick, head, body):
    return f'<div class="story"><div class="sk">{kick}</div><div class="sh">{head}</div><p>{body}</p></div>'

def dna(items):
    out = '<div class="dg">'
    for ic, c, title, ev, val, vl in items:
        out += (f'<div class="dna"><div class="di" style="background:{c}">{icon(ic, "#fff", 26)}</div><div class="dt"><b>{title}</b><span>{ev}</span></div>'
                f'<div class="dv" style="color:{c}">{val}<small>{vl}</small></div></div>')
    return out + '</div>'

def listp(items, color):
    return '<div class="lp">' + "".join(f'<div class="li"><div class="n" style="background:{color}">{i+1}</div><div><b>{h}</b><span>{t}</span></div></div>' for i, (h, t) in enumerate(items)) + '</div>'

def vs_avg(w, rows, rh=46, lab=150):
    h = rh * len(rows) + 30; plot = w - lab - 16; cx = lab + plot / 2; half = plot / 2 - 18
    mx = max([abs((v / avg - 1) * 100) for _, avg, _, vals, _ in rows for v in vals if avg] + [1]) * 1.12
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    s += f'<text x="{cx-half}" y="14" font-size="12" font-weight="700" fill="#8a93a6">below average</text><text x="{cx+half}" y="14" font-size="12" font-weight="700" fill="#8a93a6" text-anchor="end">above average</text>'
    for r, (lab_, avg, atx, vals, better) in enumerate(rows):
        y = 30 + r * rh + rh / 2
        s += f'<rect x="0" y="{y-rh/2+3}" width="{w}" height="{rh-6}" rx="8" fill="{"#f4f6fa" if r%2==0 else "#fff"}"/>'
        s += f'<text x="10" y="{y-2}" font-size="14.5" font-weight="800" fill="#14264f">{lab_}</text><text x="10" y="{y+14}" font-size="12" font-weight="600" fill="#6b7385">avg {atx}</text>'
        s += f'<line x1="{cx}" x2="{cx}" y1="{y-rh/2+6}" y2="{y+rh/2-6}" stroke="#14264f" stroke-width="2"/>'
        for i, v in enumerate(vals):
            d = (v / avg - 1) * 100 if avg else 0; x = cx + d / mx * half
            good = (d >= 0) == (better == "high"); c = G if good else LR
            if abs(d) < 0.5: c = GR
            s += f'<circle cx="{x:.1f}" cy="{y}" r="12" fill="{c}" stroke="#fff" stroke-width="2.5"/><text x="{x:.1f}" y="{y+4.5}" font-size="13" font-weight="800" text-anchor="middle" fill="#fff">{i+1}</text>'
    return s + '</svg>'

def cum_line(w, h, vals, labels, color):
    L, R, Tp, B = 46, 28, 28, 30; pw, ph = w - L - R, h - Tp - B; mx = max(max(vals), 1) * 1.2; n_ = len(vals)
    xs = [L + pw * (0.08 + 0.84 * i / max(n_ - 1, 1)) if n_ > 1 else L + pw / 2 for i in range(n_)]; ys = [Tp + ph - ph * v / mx for v in vals]
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    for t in range(0, int(mx) + 1, max(5, int(round(mx / 4 / 5)) * 5)):
        y = Tp + ph - ph * t / mx
        s += f'<line x1="{L}" x2="{w-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="#e3e6ec"/><text x="{L-8}" y="{y+4:.1f}" font-size="12.5" text-anchor="end" fill="#333">{t}</text>'
    area = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    s += f'<polygon points="{xs[0]:.1f},{Tp+ph} {area} {xs[-1]:.1f},{Tp+ph}" fill="{color}" fill-opacity=".14"/><polyline points="{area}" fill="none" stroke="{color}" stroke-width="3.2"/>'
    for x, y, v, lb in zip(xs, ys, vals, labels):
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{color}" stroke="#fff" stroke-width="2.5"/><text x="{x:.1f}" y="{y-13:.1f}" font-size="16" font-weight="900" text-anchor="middle" fill="{NAVY}">{v:+d}</text>'
        s += f'<text x="{x:.1f}" y="{Tp+ph+19}" font-size="13" font-weight="700" text-anchor="middle" fill="#222">{lb}</text>'
    return s + '</svg>'

def run_meter(w, run, pas_, rush, pas, pass_att):
    s = f'<svg width="{w}" height="120" viewBox="0 0 {w} 120" font-family="Inter">'; bw = w - 16
    s += f'<rect x="8" y="34" width="{max(bw*run/100, 0):.1f}" height="34" rx="8" fill="{RED}"/><rect x="{8+bw*run/100:.1f}" y="34" width="{max(bw*pas_/100, 0):.1f}" height="34" rx="8" fill="{NAVY}"/>'
    if run > 14: s += f'<text x="{8+bw*run/200:.1f}" y="57" font-size="19" font-weight="900" text-anchor="middle" fill="#fff">RUN {run:.1f}%</text>'
    if pas_ > 14: s += f'<text x="{8+bw*run/100+bw*pas_/200:.1f}" y="57" font-size="19" font-weight="900" text-anchor="middle" fill="#fff">PASS {pas_:.0f}%</text>'
    mx = 8 + bw * .5; s += f'<line x1="{mx}" x2="{mx}" y1="24" y2="78" stroke="#14264f" stroke-width="2" stroke-dasharray="4 3"/><text x="{mx}" y="18" font-size="12" font-weight="700" text-anchor="middle" fill="#14264f">balanced (50%)</text>'
    s += f'<text x="8" y="104" font-size="13" font-weight="600" fill="#5b6477">Rushing {rush} yds</text><text x="{w-8}" y="104" font-size="13" font-weight="600" text-anchor="end" fill="#5b6477">Passing {pas} yds · {pass_att} attempts</text>'
    return s + '</svg>'

def pts_bar(w, parts, pf):
    """parts = [(label, points, fill, text_color)] ; pf = total points for"""
    pf = max(pf, 1)
    s = (f'<svg width="{w}" height="108" viewBox="0 0 {w} 108" font-family="Inter"><defs><pattern id="hat" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="9" height="9" fill="#e9ecf2"/>'
         f'<line x1="0" y1="0" x2="0" y2="9" stroke="#c9ced9" stroke-width="3"/></pattern></defs>')
    x = 0; bw = w - 4
    for lab, v, c, tc in parts:
        if v <= 0: continue
        wd = bw * v / pf
        s += f'<rect x="{x:.1f}" y="8" width="{max(wd-3, 2):.1f}" height="48" rx="7" fill="{c}"/><text x="{x+(wd-3)/2:.1f}" y="39" font-size="21" font-weight="900" text-anchor="middle" fill="{tc}">{v}</text>'
        s += f'<text x="{x+(wd-3)/2:.1f}" y="78" font-size="14" font-weight="700" text-anchor="middle" fill="#222">{lab}</text><text x="{x+(wd-3)/2:.1f}" y="96" font-size="13" font-weight="600" text-anchor="middle" fill="#6b7385">{v/pf*100:.0f}% of points</text>'
        x += wd
    return s + '</svg>'

def pyth_chart(w, win_pct, pyth, exp_wins, n, wins):
    s = f'<svg width="{w}" height="150" viewBox="0 0 {w} 150" font-family="Inter">'
    for i, (lab, v, c) in enumerate([("Actual win rate", win_pct, G), ("Expected (points)", pyth, BL)]):
        y = 12 + i * 52
        s += (f'<text x="4" y="{y+14}" font-size="14" font-weight="700" fill="#14264f">{lab}</text><rect x="4" y="{y+22}" width="{w-84}" height="20" rx="8" fill="#eceef2"/><rect x="4" y="{y+22}" width="{(w-84)*v/100:.1f}" height="20" rx="8" fill="{c}"/>'
              f'<text x="{w-6}" y="{y+39}" font-size="22" font-weight="900" text-anchor="end" fill="{c}">{v:.0f}%</text>')
    s += f'<text x="4" y="136" font-size="13" font-weight="600" fill="#5b6477">Expected wins {exp_wins:.1f} of {n} · actual {wins} ({wins-exp_wins:+.1f})</text>'
    return s + '</svg>'

def mini_vs(rowsm):
    # rowsm: (label, pct diff, better, valuetext)
    s = '<svg width="360" height="120" viewBox="0 0 360 120" font-family="Inter">'; cx = 214; half = 110
    for i, (lab, d, better, vt) in enumerate(rowsm):
        y = 14 + i * 27; good = (d >= 0) == (better == "high"); c = G if good else LR
        if abs(d) < 0.5: c = GR
        wd = min(abs(d) / 60, 1) * half
        s += f'<text x="4" y="{y+5}" font-size="13" font-weight="700" fill="#14264f">{lab}</text>'
        s += f'<rect x="{cx if d>=0 else cx-wd:.1f}" y="{y-7}" width="{max(wd,2):.1f}" height="14" rx="4" fill="{c}"/>'
        s += f'<text x="{352}" y="{y+5}" font-size="13" font-weight="800" text-anchor="end" fill="#14264f">{vt}</text>'
        s += f'<text x="{(cx+wd+6) if d>=0 else (cx-wd-6):.1f}" y="{y+4.5}" font-size="11.5" font-weight="700" text-anchor="{"start" if d>=0 else "end"}" fill="{c}">{d:+.0f}%</text>'
    return s + f'<line x1="{cx}" x2="{cx}" y1="2" y2="116" stroke="#14264f" stroke-width="1.5"/></svg>'

def conf_bar(n_, lo, mid, hi):
    lvl = 1 if n_ < lo else 2 if n_ < mid else 3 if n_ < hi else 4
    cols = ["#e53935", "#fb8c00", "#fdd835", "#43a047"]
    return lvl, '<div class="cfb">' + "".join(f'<i style="background:{cols[k] if k < lvl else "#e4e7ee"}"></i>' for k in range(4)) + '</div>'



TPCSS = """
.tphero{position:relative;border-radius:22px;overflow:hidden;color:#fff;height:330px;margin-top:16px;box-shadow:0 3px 8px rgba(0,0,0,.25);background:linear-gradient(115deg,#0b1736 0%,#14264f 55%,#7a0f1e 140%)}
.tphero .yl{position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.06) 0 3px,transparent 3px 64px)}
.tphero .jn{position:absolute;right:-6px;top:-30px;font-size:300px;font-weight:900;font-style:italic;color:rgba(255,255,255,.07);line-height:1}
.tphero .ph{position:absolute;left:26px;top:26px;width:220px;height:278px;border-radius:20px;border:4px solid #f2b705;overflow:hidden;background:#e9f0f7;box-shadow:0 4px 14px rgba(0,0,0,.4)}
.tphero .tx{position:absolute;left:274px;top:26px;right:26px}
.tphero .kick{font-size:13.5px;letter-spacing:3.5px;font-weight:700;color:#f2b705}
.tphero .nm{font-size:48px;font-weight:900;font-style:italic;line-height:1.05;margin-top:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tphero .big{margin-top:10px}.tphero .big b{font-size:96px;font-weight:900;font-style:italic;line-height:1;color:#fff}
.tphero .big span{font-size:17px;font-weight:800;letter-spacing:3px;margin-left:12px;opacity:.85}
.tphero .chs{position:absolute;left:274px;right:26px;bottom:26px;display:flex;gap:12px}
.tpc{flex:1;border-left:3px solid #f2b705;padding-left:12px}.tpc b{display:block;font-size:30px;font-weight:900;line-height:1.1}.tpc{font-size:12.5px;letter-spacing:1px;font-weight:700;opacity:.92}
.podium{display:flex;gap:12px;padding:12px}
.pod{flex:1;border:1.5px solid #dfe4ee;border-radius:14px;padding:10px;text-align:center;position:relative;background:#fff}
.pod .pk{position:absolute;left:10px;top:10px;width:34px;height:34px;border-radius:50%;color:#fff;font-weight:900;font-size:19px;display:flex;align-items:center;justify-content:center;z-index:2}
.pod .pp{width:100px;height:100px;border-radius:50%;overflow:hidden;margin:2px auto 6px;border:3px solid #14264f;background:#e9f0f7}
.pod .pn{font-size:17px;font-weight:800;color:#14264f}.pod .pv{font-size:34px;font-weight:900;color:#d0021b;line-height:1.1}.pod .pv small{display:block;font-size:11px;letter-spacing:2px;color:#8a93a6}
.pod .pb{display:flex;height:11px;border-radius:6px;overflow:hidden;background:#eceef2;margin-top:8px}.pod .pb i{display:block;height:100%}
.lgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:10px}
.lc{border:1.5px solid #dfe4ee;border-radius:12px;overflow:hidden;background:#fff;padding-bottom:6px}
.lh{color:#fff;font-weight:800;font-size:13.5px;letter-spacing:.5px;padding:7px 10px}
.lr{padding:5px 10px 0}.lt{display:flex;justify-content:space-between;font-size:13.5px;font-weight:600;color:#14264f}.lt b{font-weight:900;font-size:15px}
.lb{height:8px;border-radius:4px;background:#eceef2;margin-top:3px}.lb i{display:block;height:100%;border-radius:4px}
.rk{padding:6px 10px}
.rk-h,.rk-r{display:grid;grid-template-columns:40px 230px 1fr 70px 50px 50px 80px;gap:10px;align-items:center;padding:6px 6px}
.rk-h{font-size:11.5px;letter-spacing:1.5px;font-weight:800;color:#8a93a6;border-bottom:2px solid #14264f}
.rk-r{border-bottom:1px solid #e8ebf2;font-size:16px;font-weight:700;color:#14264f}
.rk-r .n{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900}
.rk-r .nm{font-weight:800}.rk-r .nm small{margin-left:6px;color:#8a93a6;font-weight:600;font-size:12.5px}
.rk-r .bar{display:flex;height:16px;border-radius:8px;overflow:hidden;background:#eceef2}.rk-r .bar i{display:block;height:100%}
.rk-r .im{font-weight:900;color:#d0021b;font-size:20px}
"""
