"""Team-vs-team comparison report pages (6 pages). Every number/sentence is computed from the data.
Python 3.11 compatible: never reuse the f-string's own quote character inside {...}."""
import html
from team_widgets import *
from pages import nice
from compare_data import compare_all, radar_scores, MD

CA, CB = "#1f6fd6", "#d0021b"     # team A blue, team B red
MUTE = "#8a93a6"

CMPCSS = """
/* Use the legacy print break as well as the modern declaration. Chrome on
   GitHub Actions otherwise creates an empty second page for this report. */
.page{break-after:auto;page-break-after:always}
.page.big + .page.big{break-before:auto;page-break-before:auto}
.vsb{position:relative;display:grid;grid-template-columns:1fr 150px 1fr;align-items:center;border-radius:20px;overflow:hidden;margin-top:14px;height:262px;color:#fff;box-shadow:0 2px 6px rgba(0,0,0,.25)}
.vsb .ta,.vsb .tb{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 14px}
.vsb .ta{background:linear-gradient(135deg,#0f3a86,#1f6fd6)}.vsb .tb{background:linear-gradient(225deg,#7a0f1e,#d0021b)}
.vsb .lg{width:116px;height:116px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.3);overflow:hidden}
.vsb .nm{font-size:30px;font-weight:900;font-style:italic;line-height:1.05;margin-top:10px}
.vsb .rc{font-size:22px;font-weight:800;margin-top:4px;letter-spacing:1px}.vsb .ct{font-size:13px;opacity:.85;letter-spacing:2px;font-weight:700;margin-top:2px}
.vsb .mid{background:#14264f;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center}
.vsb .mid b{font-size:64px;font-weight:900;font-style:italic;line-height:1}.vsb .mid span{font-size:12px;letter-spacing:3px;font-weight:700;opacity:.8}
.sbar{display:flex;height:46px;border-radius:12px;overflow:hidden;margin-top:10px;font-weight:900;font-size:20px;color:#fff;box-shadow:0 1px 3px rgba(20,38,79,.2)}
.sbar div{display:flex;align-items:center;justify-content:center;white-space:nowrap}
.bf{background:#fff;border:1.5px solid #dfe4ee;border-radius:14px;margin-top:12px;overflow:hidden;box-shadow:0 1px 3px rgba(20,38,79,.08)}
.bfh{display:grid;grid-template-columns:1fr 1fr;color:#fff;font-weight:900;font-size:17px;font-style:italic}
.bfh div{padding:8px 16px}.bfh div:last-child{text-align:right}
.bfr{display:grid;grid-template-columns:84px 1fr 206px 1fr 84px;align-items:center;gap:8px;padding:8px 12px;border-bottom:1px solid #e9ecf2}
.bfr:last-child{border-bottom:0}
.bfr .l{display:flex;justify-content:flex-end}.bfr .r{display:flex;justify-content:flex-start}
.bfr .bar{height:24px;border-radius:7px}
.bfr .lab{text-align:center;font-weight:800;font-size:15.5px;line-height:1.15}.bfr .lab small{display:block;font-size:11.5px;color:#6b7385;font-weight:600;margin-top:1px}
.bfr .v{font-size:22px;font-weight:900;line-height:1}.bfr .v small{display:block;font-size:11.5px;font-weight:700;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:92px}
.bfr .v.a{text-align:left}.bfr .v.b{text-align:right}.bfr .v.b small{margin-left:auto}
.bf.l2 .bfr{padding:15px 12px}.bf.l2 .bar{height:30px}.bf.l2 .lab{font-size:17px}.bf.l2 .v{font-size:25px}
.stk{display:flex;height:34px;border-radius:9px;overflow:hidden;background:#eceef2}.stk div{display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:14px}
.sl{font-size:14.5px;font-weight:800;margin:12px 0 5px;color:#14264f}.lg2{display:flex;gap:14px;font-size:12.5px;font-weight:700;margin-top:10px;color:#4b556c;flex-wrap:wrap}.lg2 i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.sc2 .sc td{padding:4px 10px}
.pcg{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:12px}
.pcard{display:flex;gap:12px;background:#fff;border:1.5px solid #dfe4ee;border-radius:14px;padding:10px;margin-bottom:10px;box-shadow:0 1px 3px rgba(20,38,79,.08)}
.pcard .ph2{width:86px;height:108px;border-radius:10px;overflow:hidden;flex:none;background:#e9eef6;position:relative}
.pcard .rk{position:absolute;left:5px;top:5px;width:26px;height:26px;border-radius:50%;color:#fff;font-weight:900;font-size:14px;display:flex;align-items:center;justify-content:center;z-index:2}
.pcard .pi{flex:1;min-width:0}.pcard .pi b{display:block;font-size:19px;font-weight:900;font-style:italic;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pcard .pi small{font-size:12px;color:#6b7385;font-weight:700;letter-spacing:1px}
.pcard .im{font-size:34px;font-weight:900;line-height:1;margin-top:4px}.pcard .im span{font-size:11px;letter-spacing:2px;color:#6b7385;font-weight:700;margin-left:6px}
.pcard .ms{display:flex;gap:6px;margin-top:7px;flex-wrap:wrap}.pcard .ms i{font-style:normal;background:#eef1f7;border-radius:999px;padding:2px 10px;font-size:12.5px;font-weight:700;color:#14264f}
.fm{display:flex;gap:6px;margin-top:6px}.fm div{flex:1;background:#f4f6fa;border-radius:10px;padding:6px 4px;text-align:center}
.fm .w{display:inline-block;width:26px;height:26px;border-radius:50%;color:#fff;font-weight:900;line-height:26px;font-size:13px}
.fm b{display:block;font-size:14.5px;font-weight:800;margin-top:3px}.fm small{font-size:10.5px;color:#6b7385;font-weight:600}
.sc{width:100%;border-collapse:collapse}.sc td,.sc th{padding:6px 10px;font-size:14px;border-bottom:1px solid #e9ecf2}
.sc th{background:#14264f;color:#fff;font-size:12px;letter-spacing:1.5px;text-align:center;padding:8px}
.sc td.n{font-weight:800;color:#14264f}.sc td.c{text-align:center;font-weight:800;font-size:15px}
.sc td.g{text-align:center;font-size:11.5px;letter-spacing:1px;font-weight:800;color:#fff}
.sc tr.grp td{background:#eef1f7;font-weight:900;letter-spacing:2px;font-size:12px;color:#14264f;padding:4px 10px}
"""


def esc(x):
    return html.escape(str(x))


def tlogo(t, color, sz=104):
    if t.get("logo"):
        return f'<img src="{t["logo"]}" style="width:{sz}px;height:{sz}px;object-fit:contain">'
    ini = esc("".join(w[0] for w in t["name"].split()[:2]).upper() or "T")
    return (f'<svg width="{sz}" height="{sz}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="{color}"/><circle cx="50" cy="50" r="34" fill="#14264f"/>'
            f'<text x="50" y="60" font-size="28" font-weight="900" font-style="italic" text-anchor="middle" fill="#fff" font-family="Inter">{ini}</text></svg>')


def mark(v, who, win):
    """colour for the value text"""
    if win is None:
        return NAVY
    if win == "T":
        return "#5b6477"
    return (CA if who == "A" else CB) if win == who else MUTE


def bfrow(r, names=None):
    a, b = r["a"], r["b"]
    if a is None or b is None:
        ba = bb = ""
    else:
        mx = max(abs(a), abs(b), 1e-9)
        wa = max(abs(a) / mx * 100, 2) if a else 0; wb = max(abs(b) / mx * 100, 2) if b else 0
        ba = f'<div class="bar" style="width:{wa:.1f}%;background:{CA};opacity:{1 if r["win"] in ("A", None, "T") else .45}"></div>'
        bb = f'<div class="bar" style="width:{wb:.1f}%;background:{CB};opacity:{1 if r["win"] in ("B", None, "T") else .45}"></div>'
    sa = f'<small style="color:{MUTE}">{esc(names[0])}</small>' if names else ""
    sb = f'<small style="color:{MUTE}">{esc(names[1])}</small>' if names else ""
    return (f'<div class="bfr"><div class="v a" style="color:{mark(a, "A", r["win"])}">{r["fa"]}{sa}</div><div class="l">{ba}</div>'
            f'<div class="lab">{r["label"]}<small>{r["sub"]}</small></div><div class="r">{bb}</div>'
            f'<div class="v b" style="color:{mark(b, "B", r["win"])}">{r["fb"]}{sb}</div></div>')


def bf(rows, A, B, names=None, cls=""):
    head = (f'<div class="bfh"><div style="background:{CA}">{esc(A["name"].upper())}</div><div style="background:{CB}">{esc(B["name"].upper())}</div></div>')
    return f'<div class="bf {cls}">' + head + "".join(bfrow(r, names[i] if names else None) for i, r in enumerate(rows)) + '</div>'


def stack(label, parts):
    tot = sum(v for _, v, _ in parts)
    if not tot:
        return f'<div class="sl">{label}</div><div class="stk"><div style="background:#c9ced8;flex:1">none recorded</div></div>'
    segs = "".join(f'<div style="background:{c};width:{v/tot*100:.1f}%">{v if v/tot > .08 else ""}</div>' for _, v, c in parts if v)
    return f'<div class="sl">{label}</div><div class="stk">{segs}</div>'


def legend2(parts):
    return '<div class="lg2">' + "".join(f'<span><i style="background:{c}"></i>{n}</span>' for n, c in parts) + '</div>'


def nap(msg, h=120):
    return (f'<div style="height:{h}px;display:flex;align-items:center;justify-content:center;text-align:center;color:#8a93a6;font-weight:700;font-size:15px">'
            f'<div>{msg}</div></div>')


def lead(A, B, rows, who, k=3):
    """top-k advantages of team `who` by relative gap, as (title, text)"""
    out = []
    for r in sorted([r for r in rows if r["win"] == who and r["gap"] >= 0.08], key=lambda r: -r["gap"])[:k]:
        mine, other = (r["fa"], r["fb"]) if who == "A" else (r["fb"], r["fa"])
        out.append((r["label"], f'{mine} against {other} ({r["sub"]}).'))
    return out


def pcard(p, rank, color):
    ph = photo_or_silhouette(p)
    ms = []
    if p["scrim"]: ms.append(f'{p["scrim"]} scrimmage yds')
    if p["td"]: ms.append(f'{p["td"]} TD')
    if p["idx"]: ms.append(f'def index {p["idx"]}')
    return (f'<div class="pcard"><div class="ph2"><div class="rk" style="background:{color}">{rank}</div>{ph}</div><div class="pi"><b>{esc(p["name"])}</b>'
            f'<small>#{esc(p["number"]) if p["number"] else "-"}</small><div class="im" style="color:{color}">{p["impact"]:.1f}<span>IMPACT</span></div>'
            f'<div class="ms">{"".join(f"<i>{m}</i>" for m in ms) or "<i>no stats yet</i>"}</div></div></div>')


def form_block(S, color):
    M = S["M"][-5:]
    if not M:
        return nap("No match list", 70)
    chips = "".join(f'<div><span class="w" style="background:{G if m["f"] > m["a"] else LR if m["f"] < m["a"] else GR}">{"W" if m["f"] > m["a"] else "L" if m["f"] < m["a"] else "D"}</span>'
                    f'<b>{m["f"]}-{m["a"]}</b><small>{esc(m["opp"][:12])}</small></div>' for m in M)
    return f'<div class="fm">{chips}</div>'


def plural(n, w, p=None):
    return f"{n} {w if n == 1 else (p or w + 's')}"


def build_compare_pages(A, B, notes=()):
    rows = compare_all(A, B)
    R = {r["key"]: r for r in rows}
    comp = [r for r in rows if r["win"] is not None]
    aw = sum(1 for r in comp if r["win"] == "A"); bw = sum(1 for r in comp if r["win"] == "B"); tw = sum(1 for r in comp if r["win"] == "T")
    an, bn = esc(A["name"]), esc(B["name"])
    pages = []
    foot_ = lambda i: foot(i)

    # overall verdict
    if aw == bw:
        lead_t = None
    else:
        lead_t = "A" if aw > bw else "B"
    pts_edge = A["mpg"] - B["mpg"]
    if lead_t:
        W_, L_ = (A, B) if lead_t == "A" else (B, A)
        wn = aw if lead_t == "A" else bw; ln = bw if lead_t == "A" else aw
        head = f"{W_['name']} holds the edge"
        body = (f"<b>{esc(W_['name'])}</b> leads <b>{wn}</b> of <b>{len(comp)}</b> comparable categories against <b>{ln}</b> for {esc(L_['name'])} ({tw} too close to call). "
                f"Scoring margin per match: <b>{A['mpg']:+.1f}</b> for {an} versus <b>{B['mpg']:+.1f}</b> for {bn}. ")
    else:
        head = "Too close to call"
        body = f"Both teams win <b>{aw}</b> categories ({tw} too close to call). Scoring margin per match: <b>{A['mpg']:+.1f}</b> for {an}, <b>{B['mpg']:+.1f}</b> for {bn}. "
    small_n = min(A["n"], B["n"])
    body += (f"Caution: one team has only {plural(small_n, 'match', 'matches')} logged, so treat every rate as provisional." if small_n < 4
             else "Every rate below is per match, so teams with a different number of matches stay comparable.")

    # direct meetings
    def meets():
        out = []
        for S, other, side in ((A, B, "A"), (B, A, "B")):
            for m in S["M"]:
                if m["opp"].strip().lower() == other["name"].strip().lower():
                    out.append((side, m))
        seen, res = set(), []
        for side, m in out:
            fa, fb = (m["f"], m["a"]) if side == "A" else (m["a"], m["f"])
            k = (m["date"], fa, fb)
            if k not in seen:
                seen.add(k); res.append((m["date"], fa, fb))
        return res
    meet = meets()
    meet_html = ""
    if meet:
        cells = "".join(f'<div><span class="w" style="background:{CA if fa > fb else CB if fb > fa else GR}">{"A" if fa > fb else "B" if fb > fa else "D"}</span><div><b>{fa} – {fb}</b><span>{esc(d) or "previous meeting"}</span></div></div>' for d, fa, fb in meet[-4:])
        meet_html = (f'<div class="sec"><i></i>HEAD-TO-HEAD HISTORY ({an} first)</div><div class="tl">{cells}</div>')

    # =============== PAGE 1 ===============
    kr = ["win_pct", "ppg", "papg", "mpg", "ypg", "tom_pg"]
    key_rows = [R[k] for k in kr if R[k]["a"] is not None and R[k]["b"] is not None]
    sa_ = lead(A, B, rows, "A"); sb_ = lead(A, B, rows, "B")
    fill = [("Even matchup", "No category separates the teams by a clear margin yet.")]
    sa_ = sa_ or fill; sb_ = sb_ or fill
    tot = max(aw + tw + bw, 1)
    pages.append(f'''<div class="page big">{header("TEAM COMPARISON", "HEAD TO HEAD")}
<div class="vsb"><div class="ta"><div class="lg">{tlogo(A, CA, 100)}</div><div class="nm">{an}</div><div class="rc">{A["wins"]}-{A["losses"]}-{A["draws"]}</div><div class="ct">{esc(A["city"].upper()) or "TEAM A"}</div></div>
<div class="mid"><b>VS</b><span>{plural(A["n"], "MATCH", "MATCHES")} / {plural(B["n"], "MATCH", "MATCHES")}</span></div>
<div class="tb"><div class="lg">{tlogo(B, CB, 100)}</div><div class="nm">{bn}</div><div class="rc">{B["wins"]}-{B["losses"]}-{B["draws"]}</div><div class="ct">{esc(B["city"].upper()) or "TEAM B"}</div></div></div>
<div class="sec"><i></i>CATEGORY SCOREBOARD — WHO WINS MORE CATEGORIES</div>
<div class="sbar"><div style="background:{CA};width:{aw/tot*100:.1f}%">{aw if aw else ""}</div><div style="background:#9aa0ab;width:{tw/tot*100:.1f}%">{tw if tw else ""}</div><div style="background:{CB};width:{bw/tot*100:.1f}%">{bw if bw else ""}</div></div>
<div style="display:flex;justify-content:space-between;font-size:12.5px;font-weight:700;color:#6b7385;margin-top:4px"><span>{an} wins {aw}</span><span>{tw} too close</span><span>{bn} wins {bw}</span></div>
{story("THE MATCHUP IN ONE SENTENCE", head, body)}
<div class="sec"><i></i>KEY NUMBERS (PER MATCH)</div>
{bf(key_rows, A, B) if key_rows else nap("Not enough data to compare.")}
{meet_html}
<div class="row2" style="margin-top:14px">
{panel(an + " advantages", "trophy", listp(sa_, CA), style="flex:1")}
{panel(bn + " advantages", "trophy", listp(sb_, CB), style="flex:1")}
</div>
{foot_(1)}</div>''')

    # =============== PAGE 2: OFFENSE ===============
    orows = [R[k] for k in ("ypg", "pass_ypg", "rush_ypg", "otd_pg", "comp_pct", "rz", "third", "run_share")]
    orows = [r for r in orows if r["a"] is not None or r["b"] is not None]
    rs_a, rs_b = A["run_share"], B["run_share"]
    def style_of(rs, S):
        if rs is None: return "no passing/rushing yards tracked"
        return "run-heavy" if rs >= 60 else "pass-first" if rs <= 40 else "balanced"
    ins_o = [f"{an} is {style_of(rs_a, A)}, {bn} is {style_of(rs_b, B)}.",
             (f"Total yards per match: {R['ypg']['fa']} vs {R['ypg']['fb']}." if R["ypg"]["a"] is not None and R["ypg"]["b"] is not None else "Yardage is not tracked for both teams."),
             f"Points per match: {R['ppg']['fa']} vs {R['ppg']['fb']}."]
    pages.append(f'''<div class="page big">{header("TEAM COMPARISON", "OFFENSE")}
<div class="sec" style="margin-top:14px"><i></i>HOW EACH OFFENSE MOVES THE BALL</div>
{bf(orows, A, B, cls="l2") if orows else nap("No offensive data for either team.")}
<div class="row2" style="margin-top:14px">
{panel("Scoring per match", "star", '<div style="padding:10px 14px">' + hrows(430, [(A["name"][:12], round(A["ppg"], 1), A["ppg"] / max(A["ppg"], B["ppg"], 1e-9), CA), (B["name"][:12], round(B["ppg"], 1), B["ppg"] / max(A["ppg"], B["ppg"], 1e-9), CB)], rh=44) + '</div>', style="flex:1")}
{panel("Yards per match", "bars", '<div style="padding:10px 14px">' + (hrows(430, [(A["name"][:12], round(A["ypg"]), A["ypg"] / max(A["ypg"], B["ypg"], 1e-9), CA), (B["name"][:12], round(B["ypg"]), B["ypg"] / max(A["ypg"], B["ypg"], 1e-9), CB)], rh=44) if A["ypg"] is not None and B["ypg"] is not None else nap("Not tracked", 88)) + '</div>', style="flex:1")}
</div>
<div class="row2" style="margin-top:14px">
{panel("Run vs pass mix", "run", '<div style="padding:4px 16px 12px">' + "".join(stack(esc(S["name"]), [("Rushing yds", S["T"]["rush_yds"], CA if i == 0 else CB), ("Passing yds", S["T"]["pass_yds"], "#9aa0ab")]) for i, S in enumerate((A, B))) + legend2([("Rushing yards", "#14264f"), ("Passing yards", "#9aa0ab")]) + '</div>', style="flex:1")}
{panel("Where touchdowns come from", "star", '<div style="padding:4px 16px 12px">' + "".join(stack(esc(S["name"]), [("Rushing TD", S["T"]["rush_td"], "#3a9a2c"), ("Passing TD", S["T"]["pass_td"], "#1f8fef"), ("Defensive TD", S["T"]["def_td"], "#8e24aa")]) for S in (A, B)) + legend2([("Rushing TD", "#3a9a2c"), ("Passing TD", "#1f8fef"), ("Defensive TD", "#8e24aa")]) + '</div>', style="flex:1")}
</div>
{bottom_row(ins_o)}
{foot_(2)}</div>''')

    # =============== PAGE 3: DEFENSE ===============
    drows = [R[k] for k in ("papg", "sacks_pg", "int_pg", "pbu_pg", "flags_pg", "dtd")]
    srows = [R[k] for k in ("int_thrown_pg", "sall_pg", "tom_pg")]
    ins_d = [f"Points allowed per match: {R['papg']['fa']} ({an}) vs {R['papg']['fb']} ({bn}).",
             f"Takeaways minus giveaways: {R['tom_pg']['fa']} vs {R['tom_pg']['fb']} per match.",
             f"Defensive plays (INT + PBU + sacks): {A['plays_pg']:.1f} vs {B['plays_pg']:.1f} per match."]
    pages.append(f'''<div class="page big">{header("TEAM COMPARISON", "DEFENSE")}
<div class="sec" style="margin-top:14px"><i></i>DEFENSE — STOPPING THE OTHER TEAM</div>
{bf(drows, A, B, cls="l2")}
<div class="sec"><i></i>BALL SECURITY — GIVING THE BALL AWAY (LOWER IS BETTER, EXCEPT MARGIN)</div>
{bf(srows, A, B, cls="l2")}
<div class="row2" style="margin-top:14px">
{panel("Defensive plays mix", "bolt", '<div style="padding:4px 16px 12px">' + "".join(stack(esc(S["name"]), [("Sacks", S["T"]["sacks"], "#d9091f"), ("Interceptions", S["T"]["def_int"], "#8e24aa"), ("Pass breakups", S["T"]["pbu"], "#f2a900")]) for S in (A, B)) + legend2([("Sacks", "#d9091f"), ("Interceptions", "#8e24aa"), ("Pass breakups", "#f2a900")]) + '</div>', style="flex:1")}
{panel("Turnover battle (season)", "bal", '<div style="padding:8px 14px">' + hrows(430, [(A["name"][:10] + " +", A["T"]["def_int"], A["T"]["def_int"] / max(A["T"]["def_int"], A["T"]["int_thrown"], B["T"]["def_int"], B["T"]["int_thrown"], 1), CA), (A["name"][:10] + " -", A["T"]["int_thrown"], A["T"]["int_thrown"] / max(A["T"]["def_int"], A["T"]["int_thrown"], B["T"]["def_int"], B["T"]["int_thrown"], 1), "#9aa0ab"), (B["name"][:10] + " +", B["T"]["def_int"], B["T"]["def_int"] / max(A["T"]["def_int"], A["T"]["int_thrown"], B["T"]["def_int"], B["T"]["int_thrown"], 1), CB), (B["name"][:10] + " -", B["T"]["int_thrown"], B["T"]["int_thrown"] / max(A["T"]["def_int"], A["T"]["int_thrown"], B["T"]["def_int"], B["T"]["int_thrown"], 1), "#9aa0ab")], rh=40) + '<div class="cap">+ interceptions made, - interceptions thrown</div></div>', style="flex:1")}
</div>
{bottom_row(ins_d)}
{foot_(3)}</div>''')

    # =============== PAGE 4: SHAPE & FORM ===============
    ax, sa, sb = radar_scores(A, B)
    radar = radar_n(470, 400, 138, ax, [(CA, sa), (CB, sb)], font=13, dots=4, fill=0.18)
    legend = (f'<div style="display:flex;gap:20px;justify-content:center;font-weight:800;font-size:14px"><span style="color:{CA}">■ {an}</span><span style="color:{CB}">■ {bn}</span></div>')
    def ringp(S, c):
        return ring(190, S["win_pct"], c, f'{S["win_pct"]:.0f}%', "win rate")
    def mchart(S, c):
        Mm = S["M"][-8:]
        if not Mm:
            return nap("No match list", 220)
        mx, tk, _ = nice(max([m["f"] for m in Mm] + [m["a"] for m in Mm] + [1]), 4)
        return cols_chart(452, 250, [f"M{m['n']}" for m in Mm], [("Pts For", c, [m["f"] for m in Mm], [m["f"] for m in Mm]), ("Pts Against", "#9aa0ab", [m["a"] for m in Mm], [m["a"] for m in Mm])], mx, tk)
    ins_f = [f"Radar axes are relative: the stronger team on an axis scores 100, the other is scaled against it.",
             f"Pythagorean expectation (from points for/against): {R['pyth']['fa']} vs {R['pyth']['fb']}.",
             f"Last results: {an} {A['wins']}-{A['losses']}-{A['draws']}, {bn} {B['wins']}-{B['losses']}-{B['draws']}."]
    pages.append(f'''<div class="page big">{header("TEAM COMPARISON", "TEAM SHAPE & FORM")}
<div class="row2" style="margin-top:14px">
{panel("Team Shape (relative)", "target", '<div style="padding:6px 8px">' + radar + legend + '</div>', style="flex:1.25")}
{panel("Win Rate", "trophy", f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:8px"><div style="display:flex;gap:6px;align-items:center">{ringp(A, CA)}{ringp(B, CB)}</div>{legend}</div>', style="flex:1")}
</div>
<div class="row2" style="margin-top:14px">
{panel(an + " — recent matches", "clock", '<div style="padding:8px 12px 10px">' + form_block(A, CA) + '</div>', style="flex:1")}
{panel(bn + " — recent matches", "clock", '<div style="padding:8px 12px 10px">' + form_block(B, CB) + '</div>', style="flex:1")}
</div>
<div class="row2" style="margin-top:14px">
{panel(an + " — points by match", "bars", '<div style="padding:4px 6px">' + mchart(A, CA) + '</div>', style="flex:1")}
{panel(bn + " — points by match", "bars", '<div style="padding:4px 6px">' + mchart(B, CB) + '</div>', style="flex:1")}
</div>
{bottom_row(ins_f)}
{foot_(4)}</div>''')

    # =============== PAGE 5: KEY PLAYERS ===============
    def top3(S):
        return sorted(S["P"], key=lambda p: -p["impact"])[:3]
    ta, tb = top3(A), top3(B)
    cols = lambda L, c: "".join(pcard(p, i + 1, c) for i, p in enumerate(L)) or nap("No player stats", 120)
    def leader(S, key):
        if not S["P"]: return None
        p = max(S["P"], key=lambda p: p[key])
        return p if p[key] > 0 else None
    cats = [("Passing yards", "pyd"), ("Rushing yards", "rsy"), ("Receiving yards", "ryd"), ("Touchdowns", "td"), ("Sacks", "sacks"), ("Interceptions", "dint"), ("Flags pulled", "flags")]
    prow, pnames = [], []
    for lab, k in cats:
        la, lb = leader(A, k), leader(B, k)
        a, b = (la[k] if la else None), (lb[k] if lb else None)
        if a is None and b is None: continue
        from compare_data import winner
        prow.append(dict(label=lab, sub="team leader", a=a, b=b, fa=str(a) if a is not None else "—", fb=str(b) if b is not None else "—", win=winner(a, b, 1) if a is not None and b is not None else None))
        pnames.append((la["name"] if la else "", lb["name"] if lb else ""))
    depth = [dict(label="Total impact", sub="sum of player impact", a=A["impact_total"], b=B["impact_total"], fa=f'{A["impact_total"]:.0f}', fb=f'{B["impact_total"]:.0f}', win=None),
             dict(label="Players with a TD", sub="scored at least once", a=A["scorers"], b=B["scorers"], fa=str(A["scorers"]), fb=str(B["scorers"]), win=None),
             dict(label="Top-3 share", sub="of total impact", a=A["top3_share"], b=B["top3_share"], fa=(f'{A["top3_share"]:.0f}%' if A["top3_share"] is not None else "n/a"), fb=(f'{B["top3_share"]:.0f}%' if B["top3_share"] is not None else "n/a"), win=None)]
    from compare_data import winner as wn_
    depth[0]["win"] = wn_(A["impact_total"], B["impact_total"], 1) if A["P"] and B["P"] else None
    depth[1]["win"] = wn_(A["scorers"], B["scorers"], 1) if A["P"] and B["P"] else None
    depth_nm = [("", "")] * 3
    ins_p = []
    if ta and tb:
        ins_p.append(f"Best player of each team: {esc(ta[0]['name'])} ({ta[0]['impact']:.1f}) and {esc(tb[0]['name'])} ({tb[0]['impact']:.1f}).")
    if A["top3_share"] is not None and B["top3_share"] is not None:
        hi = A if A["top3_share"] > B["top3_share"] else B
        ins_p.append(f"{esc(hi['name'])} depends more on its top 3 players ({hi['top3_share']:.0f}% of total impact).")
    ins_p.append("Impact = scrimmage yards / 10 + offensive TDs x 6 + defense index (flags + INT x3 + sacks x3 + PBU x2 + def TD x6).")
    pages.append(f'''<div class="page big">{header("TEAM COMPARISON", "KEY PLAYERS")}
<div class="pcg">
<div><div class="sec" style="margin:0 0 8px"><i style="background:{CA}"></i>{an} — TOP 3</div>{cols(ta, CA)}</div>
<div><div class="sec" style="margin:0 0 8px"><i></i>{bn} — TOP 3</div>{cols(tb, CB)}</div></div>
<div class="sec" style="margin-top:6px"><i></i>BEST PLAYER IN EACH CATEGORY</div>
{bf(prow, A, B, pnames) if prow else nap("No player stats for either team.")}
<div class="sec" style="margin-top:12px"><i></i>ROSTER DEPTH</div>
{bf(depth, A, B)}
{bottom_row(ins_p[:3], h=150)}
{foot_(5)}</div>''')

    # =============== PAGE 6: FULL SCOREBOARD + VERDICT ===============
    def plan(X, Y, who):
        me, other = ("A", "B") if who == "A" else ("B", "A")
        ex = [r for r in sorted(rows, key=lambda r: -r["gap"]) if r["win"] == me and r["gap"] >= 0.08][:2]
        dg = [r for r in sorted(rows, key=lambda r: -r["gap"]) if r["win"] == other and r["gap"] >= 0.08][:1]
        out = []
        for r in ex:
            out.append(("Press: " + r["label"], f'{X["name"] if who == "A" else Y["name"]} is clearly better here ({r["fa"] if who == "A" else r["fb"]} vs {r["fb"] if who == "A" else r["fa"]}): make it the focus of the game plan.'))
        for r in dg:
            out.append(("Neutralise: " + r["label"], f'The opponent has the edge ({r["fb"] if who == "A" else r["fa"]} vs {r["fa"] if who == "A" else r["fb"]}): prepare a specific answer.'))
        return out or [("No clear edge", "The teams are level in every category; execution decides.")]
    tr = ""; last = None
    names = dict(results="RESULTS", offense="OFFENSE", style="STYLE (NO WINNER)", defense="DEFENSE", security="BALL SECURITY")
    for r in rows:
        if r["group"] != last:
            tr += f'<tr class="grp"><td colspan="4">{names[r["group"]]}</td></tr>'; last = r["group"]
        w = r["win"]
        cell = ('<td class="g" style="background:#9aa0ab">n/a</td>' if w is None and r["dir"] != 0 else
                '<td class="g" style="background:#c9ced8;color:#5b6477">style</td>' if r["dir"] == 0 else
                '<td class="g" style="background:#9aa0ab">CLOSE</td>' if w == "T" else
                f'<td class="g" style="background:{CA if w == "A" else CB}">{an[:10].upper() if w == "A" else bn[:10].upper()}</td>')
        tr += (f'<tr><td class="n">{r["label"]}</td><td class="c" style="color:{mark(r["a"], "A", w)}">{r["fa"]}</td>'
               f'<td class="c" style="color:{mark(r["b"], "B", w)}">{r["fb"]}</td>{cell}</tr>')
    table = f'<table class="sc"><tr><th style="text-align:left">METRIC</th><th>{an[:14].upper()}</th><th>{bn[:14].upper()}</th><th>EDGE</th></tr>{tr}</table>'
    gaps = []
    if aw + bw:
        gaps.append(f"{an} leads {aw} categories, {bn} leads {bw}; {tw} are within 3%.")
    miss = [r["label"] for r in rows if r["dir"] != 0 and (r["a"] is None or r["b"] is None)]
    if miss:
        gaps.append("Not compared (missing for at least one team): " + ", ".join(miss[:5]) + ("..." if len(miss) > 5 else "") + ".")
    if A["notes"] or B["notes"]:
        gaps.append("Some team totals were derived from the sum of player stats.")
    if small_n < 4:
        gaps.append(f"Small sample ({plural(small_n, 'match', 'matches')} for one team).")
    gaps = gaps or ["All metrics were available for both teams."]
    pages.append(f'''<div class="page big">{header("TEAM COMPARISON", "FULL SCOREBOARD")}
<div class="sec" style="margin-top:14px"><i></i>EVERY METRIC, SIDE BY SIDE</div>
<div class="bf sc2" style="margin-top:8px">{table}</div>
<div class="row2" style="margin-top:14px">
{panel("Game plan: " + an, "target", listp(plan(A, B, "A"), CA), style="flex:1")}
{panel("Game plan: " + bn, "target", listp(plan(A, B, "B"), CB), style="flex:1")}
</div>
{bottom_row(gaps[:3], h=140)}
{foot_(6)}</div>''')
    return pages
