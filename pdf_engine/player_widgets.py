"""Small widgets used only by the single-player report (tiles, gauges with reference bands, meters)."""
import math
from components import NAVY, RED, icon, darken

PCSS = """
.tg{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px}
.tile{background:#fff;border:1.5px solid #dfe4ee;border-radius:14px;padding:11px 8px 10px;text-align:center;box-shadow:0 1px 3px rgba(20,38,79,.08)}
.tile .ic{width:38px;height:38px;border-radius:50%;margin:0 auto 5px;display:flex;align-items:center;justify-content:center}
.tile b{font-size:31px;font-weight:800;display:block;line-height:1.05;color:#14264f}
.tile span{font-size:14px;font-weight:700;color:#14264f}
.tile small{display:block;font-size:12.5px;color:#6b7385;font-weight:600;margin-top:1px}
.tile.h{display:flex;align-items:center;gap:14px;text-align:left;padding:10px 14px}
.tile.h .ic{width:52px;height:52px;margin:0;flex:none}
.tile.h b{font-size:29px}.tile.h span{font-size:15.5px;display:block}
.sec{display:flex;align-items:center;gap:10px;font-size:22px;font-weight:800;margin-top:16px}
.sec i{width:5px;height:24px;background:#d0021b;display:block}
.phero{position:relative;border-radius:22px;overflow:hidden;color:#fff;height:352px;margin-top:16px;box-shadow:0 3px 8px rgba(0,0,0,.25);background:linear-gradient(115deg,#0b1736 0%,#14264f 55%,#7a0f1e 140%)}
.phero .yl{position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.06) 0 3px,transparent 3px 64px)}
.phero .jn{position:absolute;right:-6px;top:-40px;font-size:330px;font-weight:900;font-style:italic;color:rgba(255,255,255,.07);line-height:1}
.phero .ph{position:absolute;left:26px;top:26px;width:236px;height:300px;border-radius:22px;border:4px solid #d0021b;overflow:hidden;background:#e9f0f7;box-shadow:0 4px 14px rgba(0,0,0,.4)}
.phero .tx{position:absolute;left:292px;top:26px;right:26px}
.phero .kick{font-size:13.5px;letter-spacing:4px;font-weight:700;opacity:.8}
.phero .nm{font-size:50px;font-weight:900;font-style:italic;line-height:1.02;margin-top:6px;white-space:nowrap}
.phero .sub{display:flex;gap:10px;margin-top:12px;align-items:center;flex-wrap:wrap}
.phero .pill{background:#d0021b;border-radius:999px;padding:5px 16px;font-size:17px;font-weight:800;letter-spacing:1px}
.phero .pill2{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.34);border-radius:999px;padding:5px 16px;font-size:16px;font-weight:600}
.phero .idg{position:absolute;left:292px;right:26px;bottom:26px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px 14px}
.phero .idg div{border-left:3px solid #d0021b;padding-left:11px}
.phero .idg small{display:block;font-size:12px;letter-spacing:2px;font-weight:700;opacity:.72}
.phero .idg b{font-size:25px;font-weight:800;line-height:1.15}
.dna{display:flex;flex-wrap:wrap;gap:10px;padding:12px 14px 12px}
.tag{display:flex;align-items:center;gap:9px;border-radius:12px;padding:8px 15px 8px 10px;border:1.5px solid;background:#fff}
.tag .ti{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.tag b{font-size:16.5px;font-weight:800;display:block;line-height:1.1;color:#14264f}.tag small{font-size:12px;color:#5b6477;font-weight:600}
.sl{display:flex;gap:12px;align-items:flex-start;padding:7px 14px;border-bottom:1px solid #e8ebf2}.sl:last-child{border:none}
.sl .si{width:34px;height:34px;flex:none;border-radius:50%;display:flex;align-items:center;justify-content:center}
.sl b{font-size:16.5px;font-weight:800;color:#14264f;display:block}.sl span{font-size:14px;color:#4b5468;line-height:1.3}
.chk{display:grid;grid-template-columns:34px 270px 1fr 92px;align-items:center;gap:10px;padding:5px 14px;border-bottom:1px solid #e8ebf2;font-size:14px}
.chk:last-child{border:none}.chk b{font-weight:800;color:#14264f;font-size:15px}.chk span{color:#4b5468}
.chk .st{font-size:11.5px;font-weight:800;letter-spacing:1px;border-radius:999px;padding:4px 0;text-align:center}
.ok{background:#e4f4e6;color:#2b7a20}.rv{background:#fdebd3;color:#b86b00}
.glo{display:grid;grid-template-columns:1fr 1fr;gap:3px 26px;padding:8px 16px;font-size:12.5px;color:#4b5468;line-height:1.35}
.glo b{color:#14264f}
.nbox{border:2px solid #14264f;border-radius:14px;background:#fff;padding:12px 20px}
.nbox .nt2{display:flex;align-items:center;gap:10px;font-size:22px;font-weight:800;color:#14264f}
.nbox .nl{border-bottom:1px solid #d6dae2;height:30px}
"""


def tile(val, label, sub, color, ic, h=False):
    return (f'<div class="tile{" h" if h else ""}"><div class="ic" style="background:{color}">{icon(ic, "#fff", 28 if h else 22)}</div>'
            f'<div><b>{val}</b><span>{label}</span><small>{sub}</small></div></div>')


def grid(items, cols=4, h=False):
    return f'<div class="tg" style="grid-template-columns:repeat({cols},1fr)">' + "".join(tile(*t, h=h) for t in items) + '</div>'


def ring(sz, pct, color, center, sub, track="#e7e9ee"):
    pct = max(0, min(100, pct))
    r = sz * .38; cx = cy = sz / 2; sw = sz * .105; circ = 2 * math.pi * r
    return (f'<svg width="{sz}" height="{sz}" viewBox="0 0 {sz} {sz}" font-family="Inter"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{track}" stroke-width="{sw}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-dasharray="{circ*pct/100:.1f} {circ:.1f}" transform="rotate(-90 {cx} {cy})"/>'
            f'<text x="{cx}" y="{cy+sz*.05:.0f}" font-size="{sz*.2:.0f}" font-weight="900" text-anchor="middle" fill="{NAVY}">{center}</text>'
            f'<text x="{cx}" y="{cy+sz*.18:.0f}" font-size="{max(sz*.07, 11):.0f}" font-weight="600" text-anchor="middle" fill="#7b8294">{sub}</text></svg>')


def band_gauge(w, h, value, vmax, bands, color, center, sub, detail, na=False):
    """Semicircle gauge with reference zones. bands = [(upper_value, hex)], value clipped to vmax."""
    cx = w / 2; r = min(w * .38, h * .66); cy = h * .70; sw = 20; arc = math.pi
    def pt(f, rr):
        a = math.pi + arc * f
        return cx + rr * math.cos(a), cy + rr * math.sin(a)
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    lo = 0
    for up, c in bands:
        f0, f1 = lo / vmax, min(up, vmax) / vmax
        x0, y0 = pt(f0, r); x1, y1 = pt(f1, r)
        s += f'<path d="M {x0:.1f} {y0:.1f} A {r:.1f} {r:.1f} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{c}" stroke-opacity=".28" stroke-width="{sw}"/>'
        lo = up
    if not na and value > 0:
        f = max(0, min(1, value / vmax)); x1, y1 = pt(f, r)
        s += f'<path d="M {cx-r:.1f} {cy:.1f} A {r:.1f} {r:.1f} 0 {1 if f > .5 else 0} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
        nx, ny = pt(f, r - 22); mx_, my_ = pt(f, r + 22)
        s += f'<line x1="{nx:.1f}" y1="{ny:.1f}" x2="{mx_:.1f}" y2="{my_:.1f}" stroke="{NAVY}" stroke-width="3" stroke-linecap="round"/>'
    s += (f'<text x="{cx}" y="{cy-6:.0f}" font-size="{38 if not na else 30}" font-weight="900" text-anchor="middle" fill="{NAVY if not na else "#9aa0ab"}">{center}</text>'
          f'<text x="{cx}" y="{cy+17:.0f}" font-size="14" font-weight="700" text-anchor="middle" fill="#14264f">{sub}</text>'
          f'<text x="{cx}" y="{cy+36:.0f}" font-size="12.5" font-weight="600" text-anchor="middle" fill="#7b8294">{detail}</text>'
          f'<text x="{cx-r:.0f}" y="{cy+22:.0f}" font-size="11" fill="#9aa0ab" text-anchor="middle">0</text><text x="{cx+r:.0f}" y="{cy+22:.0f}" font-size="11" fill="#9aa0ab" text-anchor="middle">{vmax:g}</text></svg>')
    return s


def hbars(w, rows, label_w=150, val_w=70, rh=40):
    """rows: (label, value_text, ratio 0..1, color)"""
    h = rh * len(rows) + 6; bw = w - label_w - val_w - 8
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'
    for i, (lab, vt, ratio, c) in enumerate(rows):
        y = 4 + i * rh + rh / 2; ratio = max(0, min(1, ratio))
        s += f'<text x="4" y="{y+6:.1f}" font-size="16.5" font-weight="600" fill="#14264f">{lab}</text>'
        s += f'<rect x="{label_w}" y="{y-6:.1f}" width="{bw}" height="12" rx="6" fill="#eceef2"/><rect x="{label_w}" y="{y-6:.1f}" width="{max(bw*ratio, 12 if ratio > 0 else 0):.1f}" height="12" rx="6" fill="{c}"/>'
        s += f'<text x="{w-4}" y="{y+6:.1f}" font-size="18" font-weight="800" text-anchor="end" fill="#14264f">{vt}</text>'
    return s + '</svg>'


def split_bar(w, parts, h=46):
    """One horizontal stacked bar. parts = [(value, color, label)]; labels of narrow blocks are staggered so they never overlap."""
    tot = sum(v for v, _, _ in parts) or 1
    s = f'<svg width="{w}" height="{h+44}" viewBox="0 0 {w} {h+44}" font-family="Inter">'
    x = 0; last_end = -1; row = 0
    live = [p for p in parts if p[0] > 0]
    if not live:
        s += f'<rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="#eceef2"/><text x="{w/2}" y="{h/2+6}" font-size="15" font-weight="700" text-anchor="middle" fill="#9aa0ab">no data yet</text>'
    for v, c, lab in live:
        wd = w * v / tot
        s += f'<rect x="{x:.1f}" y="0" width="{max(wd-3, 2):.1f}" height="{h}" rx="8" fill="{c}"/>'
        if wd > 62:
            s += f'<text x="{x+wd/2-1:.1f}" y="{h/2+7}" font-size="21" font-weight="800" text-anchor="middle" fill="#fff">{v:g}</text>'
        lw = len(lab) * 7.6
        lx = x + wd / 2 if wd > lw + 8 else x + 2
        anchor = "middle" if wd > lw + 8 else "start"
        left = lx - lw / 2 if anchor == "middle" else lx
        row = 1 if left < last_end + 6 and row == 0 else 0
        s += f'<text x="{lx:.1f}" y="{h+20+row*17}" font-size="13" font-weight="700" text-anchor="{anchor}" fill="#14264f">{lab}{"" if wd > 62 else f" ({v:g})"}</text>'
        last_end = left + lw + (0 if anchor == "middle" else 40)
        x += wd
    return s + '</svg>'


def meter(level, total=4):
    c = ["#d0021b", "#f57c10", "#f2b705", "#3a9a2c"][max(0, min(3, level))]
    return ''.join(f'<span style="flex:1;height:14px;border-radius:7px;background:{c if i <= level else "#e7e9ee"}"></span>' for i in range(total))
