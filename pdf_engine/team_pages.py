"""Team statistics report pages. Every number and sentence is computed from the request (no data is hard-coded).
Python 3.11 compatible: never reuse the f-string's own quote character inside {...}."""
import math
from team_widgets import *
from team_data import num
from pages import nice

W_, L_, D_ = G, LR, GR


def nap(msg, h=150):
    return (f'<div style="height:{h}px;display:flex;align-items:center;justify-content:center;text-align:center;color:#8a93a6;font-weight:700;font-size:15px;padding:0 24px">'
            f'<div><div style="font-size:30px;margin-bottom:4px">—</div>{msg}</div></div>')


def res(m):
    return ("W", W_) if m["f"] > m["a"] else ("L", L_) if m["f"] < m["a"] else ("D", D_)


def plural(n, w, p=None):
    return f"{n} {w if n == 1 else (p or w + 's')}"


class Ctx:
    pass


def build_team_pages(T, M, P, notes=(), banner_uri=None):
    c = Ctx()
    n = max(T["matches"], 1); pf, pa = T["pf"], T["pa"]; diff = pf - pa
    wins, losses, draws = T["wins"], T["losses"], T["draws"]
    win_pct = wins / n * 100
    rush, pas, tot = T["rush_yds"], T["pass_yds"], T["tot_yds"]
    pass_att, comp = T["pass_att"], T["comp"]
    comp_pct = comp / pass_att * 100 if pass_att else None
    run_share = rush / (rush + pas) * 100 if rush + pas else None
    pyth = pf ** 2 / (pf ** 2 + pa ** 2) * 100 if pf + pa else 50.0
    exp_wins = pyth / 100 * n
    ypp = tot / pf if pf else 0; pp100 = pf / tot * 100 if tot else 0
    disr = T["def_int"] + T["pbu"] + T["sacks"]
    td_all = T["off_td"] + T["def_td"]; pts_td = td_all * 6; pts_other = max(pf - pts_td, 0)
    avg_f, avg_a = pf / n, pa / n
    has_m = bool(M); has_yds = has_m and all(m["yds"] is not None for m in M); has_top = has_m and all(m["top"] for m in M)
    avg_y = sum(m["yds"] for m in M) / len(M) if has_yds else None
    avg_t = sum(m["top"] for m in M) / len(M) if has_top else None
    rz_eff = T["rz_scores"] / T["rz_trips"] * 100 if T["rz_trips"] else None
    td_eff = T["third_conv"] / T["third_att"] * 100 if T["third_att"] else None
    tom = T["def_int"] - T["int_thrown"]
    div0 = lambda a, b: a / b if b else 0
    pct = lambda v: f"{v:.0f}%" if v is not None else "n/a"
    pct1 = lambda v: f"{v:.1f}%" if v is not None else "n/a"
    signed = lambda v: f"{v:+.1f}"
    team = T["name"]; TEAM = team.upper()
    mlab = [f"M{m['n']}" for m in M]
    Mr = M[-6:]          # most recent matches shown in lists/cards
    if has_m:
        best_w = max(M, key=lambda m: m["f"] - m["a"]); best_d = min(M, key=lambda m: m["a"]); best_o = max(M, key=lambda m: m["f"])
    pages = []

    # ---------------- banner / timeline ----------------
    nsz = min(54, int(520 / (0.66 * max(len(TEAM), 1))))
    bg = (f"background-image:url({banner_uri})" if banner_uri else f"background:linear-gradient(115deg,{NAVY} 0%,#2a4a9a 60%,#7a0f1e 140%)")
    sub = " &nbsp;•&nbsp; ".join(x for x in [T["city"], f"Est. {T['founded']}" if T["founded"] else ""] if x) or "Flag football team"
    def banner(h=400):
        return (f'<div class="banner" style="height:{h}px;{bg}"><div class="bn"><b style="font-size:{nsz}px">{TEAM}</b><span>{sub}</span></div>'
                f'<div class="rec"><b>{wins} - {losses} - {draws}</b><span>SEASON RECORD</span></div></div>')
    tl = ('<div class="tl">' + "".join(
        f'<div><span class="w" style="background:{res(m)[1]}">{res(m)[0]}</span><div><b>{m["f"]} – {m["a"]}</b><span>M{m["n"]} · vs {m["opp"][:16]}</span></div></div>' for m in Mr) + '</div>') if has_m else ""

    # ---------------- team DNA ----------------
    dna_items = []
    if run_share is None: dna_items.append(("target", GR, "ATTACK IDENTITY", "No passing or rushing yards recorded yet.", "n/a", "RUN SHARE"))
    elif run_share >= 60: dna_items.append(("run", RED, "GROUND-AND-POUND", f"{rush} of {rush+pas} passing+rushing yards came on the ground; {plural(pass_att, 'pass attempt')} in {plural(n, 'match', 'matches')}.", f"{run_share:.0f}%", "RUN SHARE"))
    elif run_share <= 40: dna_items.append(("ball", BL, "AIR ATTACK", f"{pas} of {rush+pas} passing+rushing yards came through the air.", f"{100-run_share:.0f}%", "PASS SHARE"))
    else: dna_items.append(("bal", NAVY, "BALANCED ATTACK", f"{rush} rushing and {pas} passing yards: opponents cannot sit on one option.", f"{run_share:.0f}%", "RUN SHARE"))
    if T["def_int"] / n >= 1.5: dna_items.append(("bolt", PU, "BALL HAWKS", f"{T['def_int']} interceptions, plus {T['pbu']} pass breakups and {T['sacks']} sacks.", f"{T['def_int']/n:.1f}", "INT / MATCH"))
    elif T["sacks"] / n >= 2: dna_items.append(("bolt", RED, "PASS RUSH", f"{T['sacks']} sacks ({T['sacks']/n:.1f} per match) and {T['def_int']} interceptions.", f"{T['sacks']/n:.1f}", "SACKS / MATCH"))
    else: dna_items.append(("bolt", PU, "DEFENSIVE PLAYS", f"{T['def_int']} interceptions, {T['pbu']} pass breakups and {T['sacks']} sacks so far.", f"{disr/n:.1f}", "PLAYS / MATCH"))
    dna_items.append(("star", AM, "SCORING MACHINE" if avg_f >= 25 else "POINT PRODUCTION", f"{pf} points in {plural(n, 'match', 'matches')}" + (f"; no match under {min(m['f'] for m in M)}." if has_m else "."), f"{avg_f:.1f}", "PTS / MATCH"))
    if diff / n >= 7: dna_items.append(("trend", G, "DOMINANT MARGINS", f"Average margin {signed(diff/n)}" + (f"; best +{best_w['f']-best_w['a']}." if has_m else "."), signed(diff / n), "MARGIN / MATCH"))
    elif diff > 0: dna_items.append(("trend", G, "WINNING MARGINS", f"Outscoring opponents {pf}–{pa} over {plural(n, 'match', 'matches')}.", signed(diff / n), "MARGIN / MATCH"))
    elif diff < 0: dna_items.append(("trend", LR, "CATCHING UP", f"Outscored {pf}–{pa}; the margin is the first thing to fix.", signed(diff / n), "MARGIN / MATCH"))
    else: dna_items.append(("trend", GR, "EVEN MATCHUPS", f"Points for and against are level at {pf}.", "0.0", "MARGIN / MATCH"))
    if rz_eff is not None: dna_items.append(("target", BL, "RED ZONE FINISHING" if rz_eff >= 60 else "RED ZONE WORK", f"{T['rz_scores']} scores in {plural(T['rz_trips'], 'trip')}" + (f"; 3rd down converted {T['third_conv']} of {T['third_att']}." if T["third_att"] else "."), f"{rz_eff:.0f}%", "RED ZONE"))
    elif td_eff is not None: dna_items.append(("target", BL, "THIRD-DOWN TEAM", f"{T['third_conv']} conversions in {plural(T['third_att'], 'attempt')}.", f"{td_eff:.0f}%", "3RD DOWN"))
    else: dna_items.append(("target", BL, "TOUCHDOWNS", f"{T['off_td']} offensive and {T['def_td']} defensive touchdowns.", f"{td_all}", "TOTAL TDs"))
    dna_items.append(("check", "#00897b", "CLEAN OFFENSE" if T["int_thrown"] == 0 else "BALL SECURITY", f"{plural(T['int_thrown'], 'interception')} thrown; turnover margin {tom:+d}.", f"{tom:+d}", "TURNOVER MARGIN"))

    # strengths / watch-outs (rule based)
    S_, W2 = [], []
    if avg_f >= 20: S_.append(("Reliable scoring", f"{avg_f:.1f} points per match."))
    if avg_a <= 15 and n: S_.append(("Stingy defense", f"Only {avg_a:.1f} points allowed per match."))
    if diff / n >= 5: S_.append(("Winning margins", f"{signed(diff/n)} points per match."))
    if tom >= 2: S_.append(("Takeaways win possessions", f"{T['def_int']} interceptions and a {tom:+d} turnover margin give the offense extra drives."))
    if run_share is not None and run_share >= 60 and rush: S_.append(("A ground game that works", f"{rush} rushing yards ({rush/n:.1f}/match) and {T['rush_td']} of {T['off_td']} offensive TDs."))
    if rz_eff is not None and rz_eff >= 70: S_.append(("Finishing drives", f"{rz_eff:.0f}% in the red zone ({T['rz_scores']} of {T['rz_trips']})."))
    if td_eff is not None and td_eff >= 50: S_.append(("Keeps drives alive", f"{td_eff:.0f}% on third down."))
    if T["sacks"] / n >= 2: S_.append(("Pass rush", f"{T['sacks']} sacks ({T['sacks']/n:.1f} per match)."))
    if comp_pct is not None and comp_pct >= 60 and pass_att >= 10: S_.append(("Accurate passing", f"{comp_pct:.0f}% completions on {pass_att} attempts."))
    if win_pct >= 70 and n >= 3: S_.append(("Winning habit", f"{wins} wins in {n} matches ({win_pct:.0f}%)."))
    if run_share is not None and run_share >= 70 and pass_att / n < 6: W2.append(("One-dimensional offense", f"Only {plural(pass_att, 'pass attempt')} in {plural(n, 'match', 'matches')}. Opponents will load the box once they scout it."))
    if abs(win_pct - pyth) >= 15 and n >= 2: W2.append(("Results vs numbers", f"Points scored and allowed predict a {pyth:.0f}% win rate, not {win_pct:.0f}%. Expect some " + ("regression." if win_pct > pyth else "improvement.")))
    if avg_a >= 22: W2.append(("Points allowed", f"{avg_a:.1f} per match is high; the defense must tighten up."))
    if T["int_thrown"] >= 3: W2.append(("Ball security", f"{T['int_thrown']} interceptions thrown."))
    if T["sacks_allowed"] >= 3: W2.append(("Pass protection", f"{T['sacks_allowed']} sacks allowed."))
    if rz_eff is not None and rz_eff < 50: W2.append(("Red zone finishing", f"Only {rz_eff:.0f}% of red-zone trips ended in a score."))
    if td_eff is not None and td_eff < 40: W2.append(("Third down", f"Converting only {td_eff:.0f}%."))
    if diff < 0: W2.append(("Negative margin", f"Outscored by {abs(diff)} points over the season."))
    if n < 6: W2.append(("Small sample", f"Only {plural(n, 'match', 'matches')}: every rate in this report is provisional until the season grows."))
    if T["rz_trips"] is None or T["third_att"] is None or not has_top: W2.append(("Tracking gaps", "Red zone, third down or possession time are not recorded, so those sections are limited."))
    fill_s = [("Building a baseline", "Not enough volume yet to name clear strengths."), ("More matches needed", "Strengths appear as results accumulate."), ("Keep logging", "Every match sharpens the picture.")]
    fill_w = [("Keep tracking", "Record every drive result for deeper analysis."), ("Watch the trend", "Compare each new match with the season average."), ("Stay consistent", "No major risk flags in the current data.")]
    S_ = (S_ + fill_s)[:3]; W2 = (W2 + fill_w)[:3]
    top_traits = [d[2].title() for d in dna_items[:2]]
    headline = f"{wins}–{losses}–{draws}: " + (f"{top_traits[0].lower()} with {top_traits[1].lower()}" if n else "season report")
    story1 = (f"{team} {'won all' if wins == n and n else 'won ' + str(wins) + ' of'} <b>{n}</b> {'matches' if n != 1 else 'match'}, scoring <b>{avg_f:.1f}</b> points per match while allowing <b>{avg_a:.1f}</b> "
              f"(margin <b>{signed(diff/n)}</b>). " + (f"The offense lives on the {'ground' if run_share >= 55 else 'air' if run_share <= 45 else 'ground and air'} (<b>{run_share:.0f}%</b> of passing and rushing yards on the ground). " if run_share is not None else "")
              + f"The defense produced <b>{T['def_int']} interceptions</b> and {T['def_td']} defensive touchdowns. " + ("Caution: only a few matches are logged, so treat every rate as provisional." if n < 6 else "The sample is now large enough to start trusting the trends."))
    pages.append(f'''<div class="page big">{header("SEASON REPORT", "EXECUTIVE SUMMARY")}
{banner()}
{story("THE SEASON IN ONE SENTENCE", headline, story1)}
{tl}
<div class="sec"><i></i>TEAM DNA — WHAT THE NUMBERS SAY ABOUT THIS TEAM</div>
{dna(dna_items)}
<div class="row2" style="margin-top:14px">
{panel("Top 3 Strengths", "trophy", listp(S_, G), style="flex:1")}
{panel("Top 3 Watch-outs", "warn", listp(W2, RED), style="flex:1")}
</div>
{foot(1)}</div>''')

    # =============== PAGE 2: SEASON OVERVIEW ===============
    pts_max, pts_t, _ = nice(max([m["f"] for m in M] + [m["a"] for m in M] + [1]), 4) if has_m else (40, [0, 10, 20, 30, 40], 10)
    dmax, dt_, _ = nice(max([abs(m["f"] - m["a"]) for m in M] + [1]), 4) if has_m else (20, [0, 5, 10, 15, 20], 5)
    margin_chart = (cols_chart(458, 300, mlab, [("Margin", G, [max(m["f"] - m["a"], 0) for m in M], [f"{m['f']-m['a']:+d}" for m in M])], dmax, dt_, avg=max(diff / n, 0), avg_label=f"avg {signed(diff/n)}") if has_m else nap("Match results are not available yet.", 300))
    pts_chart = (cols_chart(458, 300, mlab, [("Pts For", NAVY, [m["f"] for m in M], [m["f"] for m in M]), ("Pts Against", RED, [m["a"] for m in M], [m["a"] for m in M])], pts_max, pts_t) if has_m else nap("Match results are not available yet.", 300))
    ins_o = [f"Record {wins}–{losses}–{draws} in {plural(n, 'match', 'matches')}: {pf} points scored, {pa} conceded ({diff:+d}).",
             f"The offense averages {avg_f:.1f} points per match; the defense gives up {avg_a:.1f}.",
             (f"Possession: {mt(avg_t)} average time per match." if has_top else "Time of possession is not tracked yet.")]
    pages.append(f'''<div class="page big">{header("TEAM STATISTICS", "SEASON OVERVIEW")}
<div class="sec" style="margin-top:14px"><i></i>OVERALL PERFORMANCE</div>
{grid([(n, "Matches", "played", "#e8574c", "trophy"), (wins, "Wins", f"{win_pct:.0f}%", G, "trophy"), (losses, "Losses", f"{losses/n*100:.0f}%", OR, "warn"),
       (draws, "Draws", "&nbsp;", GR, "bal"), (pf, "Pts For", f"{avg_f:.1f} / match", AM, "star"), (pa, "Pts Agn", f"{avg_a:.1f} / match", OR, "weight"),
       (f"{diff:+d}", "Pt Diff", f"{signed(diff/n)} / match", BL, "trend"), (mt(avg_t) if has_top else "n/a", "TOP Avg", "per match", PU, "clock")])}
<div class="row2" style="margin-top:14px">
{panel("Win Rate", "target", f'<div style="display:flex;align-items:center;gap:8px;padding:6px 8px 10px">{ring(236, win_pct, G, f"{win_pct:.0f}%", "Win Rate")}<div class="legend">'
  f'<div><i style="background:{G}"></i>Wins ({wins})</div><div><i style="background:{LR}"></i>Losses ({losses})</div><div><i style="background:{GR}"></i>Draws ({draws})</div></div></div>', style="flex:1")}
{panel("Match Results", "bars", '<div style="padding:8px 10px 6px">' + hrows(440, [("Wins", wins, wins / n, G), ("Losses", losses, losses / n, LR), ("Draws", draws, draws / n, GR),
  ("Pts For", pf, 1, AM), ("Pts Alw", pa, div0(pa, pf) if pf else (1 if pa else 0), OR), ("Off. TD", T["off_td"], 1 if T["off_td"] else 0, BL), ("Def INT", T["def_int"], 1 if T["def_int"] else 0, PU)], rh=36) + '</div>', style="flex:1")}
</div>
<div class="row2" style="margin-top:14px">
{panel("Points per Match", "bars", pts_chart, style="flex:1")}
{panel("Point Differential", "trend", margin_chart, style="flex:1")}
</div>
{bottom_row(ins_o)}
{foot(2)}</div>''')

    # =============== PAGE 3: SCORING ENGINE ===============
    parts_pts = [("Offensive TDs", T["off_td"] * 6, NAVY, "#fff"), ("Defensive TDs", T["def_td"] * 6, G, "#fff"), ("Other / not itemised", pts_other, "url(#hat)", NAVY)]
    pb = pts_bar(920, parts_pts, max(pf, pts_td)) if pf or pts_td else nap("No points recorded yet.", 108)
    meter_html = run_meter(444, run_share, 100 - run_share, rush, pas, pass_att) if run_share is not None else nap("No passing or rushing yards yet.", 120)
    cum = [sum(m["f"] - m["a"] for m in M[:i + 1]) for i in range(len(M))]
    cum_html = cum_line(458, 300, cum, [f"After M{i+1}" for i in range(len(M))], G) if len(M) >= 2 else nap("Needs at least 2 matches.", 300)
    sc_chart = (cols_chart(458, 300, mlab, [("Pts For", NAVY, [m["f"] for m in M], [m["f"] for m in M]), ("Pts Against", RED, [m["a"] for m in M], [m["a"] for m in M])], pts_max, pts_t) if has_m else nap("Match results are not available yet.", 236))
    row2 = (panel("Yards per Point by Match", "bars", cols_chart(458, 300, mlab, [("Yards / point", BL, [div0(m["yds"], m["f"]) for m in M], [f"{div0(m['yds'], m['f']):.2f}" for m in M])], nice(max([div0(m['yds'], m['f']) for m in M] + [1]), 4)[0], nice(max([div0(m['yds'], m['f']) for m in M] + [1]), 4)[1], avg=ypp, avg_label=f"avg {ypp:.2f}"), style="flex:1")
            if has_yds else panel("Points Scored vs Allowed", "bars", sc_chart, style="flex:1"))
    row2b = panel("Season Point Differential (cumulative)", "trend", cum_html, style="flex:1")
    scoring_story = (f"Every 100 yards of offense turned into <b>{pp100:.0f} points</b>. " if tot else "Yardage is not recorded, so efficiency cannot be measured. ") + \
        (f"Offense is " + ("very" if run_share >= 70 or run_share <= 30 else "somewhat") + f" tilted: <b>{max(run_share, 100-run_share):.0f}%</b> of passing and rushing yards travel one route. " if run_share is not None else "") + \
        f"Points and allowed points predict a <b>{pyth:.0f}%</b> win rate versus an actual <b>{win_pct:.0f}%</b>."
    pages.append(f'''<div class="page big">{header("SCORING ENGINE", "HOW THE POINTS COME")}
{grid([(f"{avg_f:.1f}", "Points / Match", f"allowed {avg_a:.1f}", AM, "star"), (f"{ypp:.1f}" if tot else "n/a", "Yards per Point", "fewer = more efficient", BL, "bars"),
       (f"{pp100:.1f}" if tot else "n/a", "Pts per 100 Yards", f"{tot} total yards", G, "bolt"), (f"{pyth:.0f}%", "Expected Win %", "from points scored/allowed", PU, "target")], h=True)}
{panel("Where Do the Points Come From?", "bars", '<div style="padding:8px 14px 2px">' + pb + f'<div class="cap">Assumes a touchdown = 6 points. {pts_other} of {pf} points ({div0(pts_other, pf)*100:.0f}%) are not explained by logged touchdowns: extra points, conversions, kicks, or touchdowns not yet logged. See the Data Audit page.</div></div>', style="margin-top:14px")}
<div class="row2" style="margin-top:14px">
{panel("Run vs Pass Identity", "run", '<div style="padding:10px 10px 4px">' + meter_html + f'<div class="cap">Attempted {pass_att/n:.1f} passes per match.</div></div>', style="flex:1")}
{panel("Do the Results Match the Numbers?", "target", '<div style="padding:10px 10px 4px">' + pyth_chart(444, win_pct, pyth, exp_wins, n, wins) + '<div class="cap">Pythagorean expectation = PF² ÷ (PF² + PA²). Short seasons often differ from it.</div></div>', style="flex:1")}
</div>
<div class="row2" style="margin-top:14px">
{row2}
{row2b}
</div>
{story("ANALYST'S READ", "How the scoring works", scoring_story)}
{foot(3)}</div>''')
    # =============== PAGE 4: ATTACK ===============
    oth = max(tot - pas - rush, 0)
    seg = [("Passing", pas, NAVY), ("Rushing", rush, RED), ("Other", oth, GR)]
    seg_total = sum(v for _, v, _ in seg)

    def stackbar(w, segs, total):
        s_ = f'<svg width="{w}" height="104" viewBox="0 0 {w} 104" font-family="Inter">'; x = 0
        for lab, v, col in segs:
            if v <= 0: continue
            wd = (w - 4) * v / total
            s_ += f'<rect x="{x:.1f}" y="8" width="{max(wd-3, 2):.1f}" height="46" rx="6" fill="{col}"/><text x="{x+(wd-3)/2:.1f}" y="38" font-size="20" font-weight="800" text-anchor="middle" fill="#fff">{v}</text>'
            s_ += f'<text x="{x+(wd-3)/2:.1f}" y="76" font-size="14" font-weight="700" text-anchor="middle" fill="#222">{lab}</text><text x="{x+(wd-3)/2:.1f}" y="94" font-size="13" font-weight="600" text-anchor="middle" fill="#6b7385">{v/total*100:.1f}%</text>'
            x += wd
        return s_ + '</svg>'

    def funnel2(w, stages):
        h = 40 * len(stages) + 40; s_ = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter">'; mx_ = max(stages[0][1], 1); cx = w * .42
        for i, (lab, v, col) in enumerate(stages):
            y = 6 + i * 74; wd = max(w * .74 * v / mx_, 60)
            if i:
                pw_ = max(w * .74 * stages[i - 1][1] / mx_, 60)
                s_ += f'<polygon points="{cx-pw_/2:.1f},{y-30} {cx+pw_/2:.1f},{y-30} {cx+wd/2:.1f},{y} {cx-wd/2:.1f},{y}" fill="{NAVY}" fill-opacity=".09"/>'
            s_ += f'<rect x="{cx-wd/2:.1f}" y="{y}" width="{wd:.1f}" height="44" rx="7" fill="{col}"/><text x="{cx}" y="{y+29}" font-size="22" font-weight="800" text-anchor="middle" fill="#fff">{v}<tspan font-size="13.5" font-weight="600" dx="7">{lab}</tspan></text>'
        return s_ + '</svg>'

    td_split = (donut_custom(168, [T["pass_td"], T["rush_td"]], [NAVY, RED], T["off_td"], "off. TDs") if T["pass_td"] + T["rush_td"] else ring(168, 0, RED, "0", "off. TDs"))
    td_leg = (f'<div><i style="background:{NAVY}"></i><b>{div0(T["pass_td"], T["off_td"])*100:.0f}%</b>Passing ({T["pass_td"]})</div>'
              f'<div><i style="background:{RED}"></i><b>{div0(T["rush_td"], T["off_td"])*100:.0f}%</b>Rushing ({T["rush_td"]})</div>')
    ymax_y, yt_y, _ = nice(max([m["yds"] for m in M if m["yds"] is not None] + [1]), 4) if has_yds else (200, [0, 50, 100, 150, 200], 50)
    if rz_eff is not None:
        rz_html = ('<div style="padding:6px 8px 0">' + funnel2(440, [("Red Zone trips", T["rz_trips"], NAVY), ("Scores", T["rz_scores"], RED)])
                   + f'<div class="cap" style="text-align:right">{rz_eff:.1f}% efficiency · {T["rz_trips"]-T["rz_scores"]} trips without a score</div></div>')
    else:
        rz_html = nap("Red zone trips are not tracked yet.", 200)
    ypm_html = cols_chart(458, 236, mlab, [("Total yards", BL, [m["yds"] for m in M], [m["yds"] for m in M])], ymax_y, yt_y, avg=avg_y, avg_label=f"avg {avg_y:.0f}") if has_yds else nap("Yards per match are not tracked yet.", 236)
    comp_html = gauge(458, 236, comp_pct, "#00897b", f"{comp_pct:.0f}%", "Completion rate", f"{comp} of {pass_att} attempts") if comp_pct is not None else nap("No pass attempts recorded yet.", 236)
    ins_a = [(f"Offense produced {tot} yards ({tot/n:.1f} per match)" + (f"; {run_share:.0f}% of passing + rushing yards were on the ground." if run_share is not None else ".")),
             (f"Red Zone efficiency is {rz_eff:.1f}%: {T['rz_scores']} scores in {T['rz_trips']} trips." if rz_eff is not None else f"{T['off_td']} offensive TDs: {T['pass_td']} passing and {T['rush_td']} rushing."),
             (f"Only {plural(pass_att, 'pass attempt')} so far, so passing percentages are not meaningful yet." if pass_att < 10 else f"Passing: {comp_pct:.0f}% completions and {div0(pas, pass_att):.1f} yards per attempt.")]
    rz_trips_v = T["rz_trips"] if T["rz_trips"] is not None else "n/a"
    pages.append(f'''<div class="page big">{header("ATTACKING STATS", "OFFENSE")}
{strip("TOTAL OFFENSE", tot, f"Total Yards &nbsp;·&nbsp; {tot/n:.1f} per match", [(pas, "Passing"), (rush, "Rushing"), (T["off_td"], "Off. TD"), (pct(rz_eff), "Red Zone")])}
{grid([(tot, "Total Yards", f"Per Match: {tot/n:.1f}", "#e8574c", "bars"), (pas, "Passing Yards", f"Attempts: {pass_att}", BL, "ball"), (rush, "Rushing Yards", f"Per Match: {rush/n:.1f}", G, "run"),
       (comp, "Completions", f"{pct(comp_pct)} completion", "#00897b", "check"), (T["pass_td"], "Passing TDs", f"of {T['off_td']} off. TDs", NAVY, "trophy"), (T["rush_td"], "Rushing TDs", f"of {T['off_td']} off. TDs", RED, "trophy"),
       (rz_trips_v, "Red Zone Trips", f"{T['rz_scores'] or 0} scores", OR, "target"), (pct1(rz_eff), "Red Zone Eff.", f"{T['rz_scores']} / {T['rz_trips']}" if rz_eff is not None else "not tracked", PU, "star")], h=True)}
{panel("Where the Yards Come From", "bars", '<div style="padding:8px 14px 4px">' + (stackbar(920, seg, seg_total) if seg_total else nap("No yardage recorded yet.", 104)) + '</div>', style="margin-top:14px")}
<div class="row2" style="margin-top:14px">
{panel("Touchdown Split", "trophy", f'<div style="display:flex;align-items:center;gap:14px;padding:8px 12px">{td_split}<div class="legend">{td_leg}</div></div>', style="flex:1")}
{panel("Red Zone Funnel", "target", rz_html, style="flex:1")}
</div>
<div class="row2" style="margin-top:14px">
{panel("Yards per Match", "run", ypm_html, style="flex:1")}
{panel("Passing Completion", "check", comp_html, style="flex:1")}
</div>
{bottom_row(ins_a)}
{foot(4)}</div>''')

    # =============== PAGE 5: DEFENSE ===============
    disr_vals = [T["def_int"], T["pbu"], T["sacks"]]
    don_dis = donut_custom(170, disr_vals, [PU, OR, RED], disr, "disruptions") if disr else ring(170, 0, PU, "0", "disruptions")
    ap_chart = (cols_chart(458, 236, mlab, [("Pts Against", RED, [m["a"] for m in M], [m["a"] for m in M])], pts_max, pts_t, avg=avg_a, avg_label=f"avg {avg_a:.1f}") if has_m else nap("Match results are not available yet.", 236))
    gm = max(T["flags"], T["pbu"], T["sacks"], T["def_int"], T["def_td"], 1)
    gaunt = hrows(920, [("Flags Pulled", f"{T['flags']/n:.1f}", T["flags"] / gm, "#607d8b"), ("Pass Breakups", f"{T['pbu']/n:.1f}", T["pbu"] / gm, OR), ("Sacks", f"{T['sacks']/n:.1f}", T["sacks"] / gm, RED),
                    ("Interceptions", f"{T['def_int']/n:.1f}", T["def_int"] / gm, PU), ("Defensive TDs", f"{T['def_td']/n:.1f}", T["def_td"] / gm, G)], label_w=150, val_w=60, rh=40)
    dtitle = "creates, not just prevents" if (tom > 0 or T["def_int"] >= 3) else "is still building its identity"
    dstory = (f"Opponents average <b>{avg_a:.1f}</b> points per match. The unit has <b>{T['def_int']}</b> interceptions and {T['def_td']} defensive scores for a turnover margin of <b>{tom:+d}</b>"
              + (f", and the team outscores opponents by {diff/n:.1f} per match." if diff > 0 else ".") + f" Pressure ({T['sacks']} sacks) and coverage ({T['pbu']} breakups) are what keep takeaways coming.")
    pages.append(f'''<div class="page big">{header("DEFENSIVE STATS", "DEFENSE LAB")}
{grid([(T["def_int"], "Def. INT", f"Per Match: {T['def_int']/n:.1f}", PU, "bolt"), (T["def_td"], "Defensive TDs", "scored by defense", G, "trophy"), (T["sacks"], "Sacks", f"Allowed: {T['sacks_allowed']}", RED, "bolt"),
       (T["flags"], "Flags Pulled", "defensive stops", "#607d8b", "target"), (T["pbu"], "Pass Breakups", f"{T['pbu']/n:.1f} per match", OR, "bal"), (T["int_thrown"], "INT Thrown", "offensive turnovers", GR, "warn")], cols=3, h=True)}
<div class="row2" style="margin-top:14px">
{panel("Turnover Battle", "bal", f'<div style="display:flex;align-items:center;gap:10px;padding:8px 12px 6px"><div>{duel(290, T["def_int"], T["int_thrown"])}</div>'
  f'<div style="text-align:center;flex:1"><div style="font-size:64px;font-weight:900;color:{G if tom >= 0 else LR};line-height:1">{tom:+d}</div><div style="font-size:12.5px;font-weight:800;letter-spacing:2px;color:#6b7385">MARGIN</div></div></div><div class="cap">Interceptions only. Add fumbles when they are tracked.</div>', style="flex:1")}
{panel("Anatomy of Disruption", "bolt", f'<div style="display:flex;align-items:center;gap:14px;padding:8px 12px">{don_dis}<div class="legend">'
  f'<div><i style="background:{PU}"></i><b>{div0(T["def_int"], disr)*100:.0f}%</b>Interceptions</div><div><i style="background:{OR}"></i><b>{div0(T["pbu"], disr)*100:.0f}%</b>Pass breakups</div><div><i style="background:{RED}"></i><b>{div0(T["sacks"], disr)*100:.0f}%</b>Sacks</div></div></div><div class="cap">Coverage plays (INT + PBU) are {div0(T["def_int"]+T["pbu"], disr)*100:.0f}% of all disruptions.</div>', style="flex:1")}
</div>
<div class="row2" style="margin-top:14px">
{panel("Points Allowed per Match", "warn", ap_chart, style="flex:1")}
{panel("Defense Also Scores", "trophy", f'<div style="display:flex;align-items:center;gap:14px;padding:8px 12px">{ring(186, div0(T["def_td"]*6, pf)*100, G, str(T["def_td"]*6), "points from defensive TDs")}<div class="legend"><div><i style="background:{G}"></i><b>{T["def_td"]}</b>Defensive TDs</div><div><i style="background:#e7e9ee"></i><b>{div0(T["def_td"]*6, pf)*100:.0f}%</b>of all points</div></div></div><div class="cap">Assumes a touchdown = 6 points.</div>', style="flex:1")}
</div>
{panel("The Gauntlet: What Every Opponent Faces in a Typical Match", "target", '<div style="padding:8px 14px 6px">' + gaunt + '</div>', style="margin-top:14px")}
{story("ANALYST'S READ", "A defense that " + dtitle, dstory)}
{foot(5)}</div>''')

    # =============== PAGE 6: SITUATIONAL ===============
    if has_top:
        tmax, tt_, _ = nice(max(m["top"] / 60 for m in M), 4)
        top_html = cols_chart(458, 262, mlab, [("Minutes", PU, [m["top"] / 60 for m in M], [mt(m["top"]) for m in M])], tmax, tt_, avg=avg_t / 60, avg_label=f"avg {mt(avg_t)}")
    else:
        top_html = nap("Time of possession is not tracked yet.", 262)
    sit_rows = [("3rd Down", pct(td_eff), (td_eff or 0) / 100, BL), ("Red Zone", pct(rz_eff), (rz_eff or 0) / 100, RED), ("Completion", pct(comp_pct), (comp_pct or 0) / 100, "#00897b"), ("Win Rate", f"{win_pct:.0f}%", win_pct / 100, G)]
    g3 = gauge(290, 180, td_eff or 0, BL, pct1(td_eff), "3rd down conversion", f"{T['third_conv']} of {T['third_att']} attempts" if td_eff is not None else "not tracked yet")
    g4 = gauge(290, 180, rz_eff or 0, RED, pct1(rz_eff), "Red zone scoring", f"{T['rz_scores']} of {T['rz_trips']} trips" if rz_eff is not None else "not tracked yet")
    g5 = gauge(290, 180, win_pct, G, f"{win_pct:.0f}%", "Season win rate", f"{wins} of {n} matches")
    mrows = ""
    for m in Mr[-3:]:
        r, rc = res(m)
        mrows += (f'<div class="mrow"><div class="w" style="background:{rc}">{r}</div><div class="o"><b>vs {m["opp"][:22]}</b><small>Match {m["n"]}</small></div><div class="sc">{m["f"]} – {m["a"]}</div>'
                  f'<div class="c" style="color:{rc}">{m["f"]-m["a"]:+d}<small>MARGIN</small></div><div class="c">{m["yds"] if m["yds"] is not None else "n/a"}<small>YARDS</small></div><div class="c">{mt(m["top"]) if m["top"] else "n/a"}<small>TOP</small></div></div>')
    streak = 0
    for m in reversed(M):
        if m["f"] > m["a"]: streak += 1
        else: break
    hl = []
    if has_m:
        hl = [(f"{best_w['f']-best_w['a']:+d}", "Best margin", f"Match {best_w['n']}", G, "trophy"), (best_o["f"], "Most points", f"Match {best_o['n']}", AM, "star"),
              (best_d["a"], "Fewest allowed", f"Match {best_d['n']}", BL, "bolt"), (streak, "Win streak", "current", RED, "trend")]
    ins_s = [(f"Third down: {T['third_conv']} conversions in {T['third_att']} attempts ({td_eff:.1f}%)" + (f", with {rz_eff:.1f}% efficiency in the Red Zone." if rz_eff is not None else ".")) if td_eff is not None else "Third-down data is not tracked yet.",
             (f"Total possession {mt(T['top_total'])}, {mt(avg_t)} per match." if has_top and T["top_total"] else "Time of possession is not tracked yet."),
             (f"Best margin {best_w['f']-best_w['a']:+d} (match {best_w['n']}); best defensive match: only {best_d['a']} points allowed." if has_m else "Match details will add highlights here.")]
    match_list = ('<div class="sec"><i></i>ALL MATCHES</div><div class="mh"><div></div><div>OPPONENT</div><div>SCORE</div><div>MARGIN</div><div>YARDS</div><div>TOP</div></div>' + mrows) if has_m else ""
    hl_html = ('<div class="sec"><i></i>SEASON HIGHLIGHTS</div>' + grid(hl)) if has_m else ""
    pages.append(f'''<div class="page big">{header("SITUATIONAL STATS", "&amp; ALL MATCHES")}
<div class="row2" style="margin-top:16px">
{panel("3rd Down %", "target", g3, style="flex:1")}
{panel("Red Zone Eff.", "target", g4, style="flex:1")}
{panel("Win Rate", "trophy", g5, style="flex:1")}
</div>
{grid([(T["third_att"] if T["third_att"] is not None else "n/a", "3rd Attempts", f"{T['third_conv'] or 0} conversions", BL, "target"), (pct1(td_eff), "3rd Down %", "conversion rate", "#00897b", "check"), (mt(T["top_total"]) if T["top_total"] else "n/a", "Total TOP", "time of possession", PU, "clock"), (mt(avg_t) if has_top else "n/a", "Avg TOP", "per match", OR, "clock")], h=True)}
<div class="row2" style="margin-top:14px">
{panel("Time of Possession per Match", "clock", top_html, style="flex:1")}
{panel("3rd Down, Red Zone & More", "bars", '<div style="padding:12px 12px 4px">' + hrows(436, sit_rows, label_w=110, rh=54) + '</div>', style="flex:1")}
</div>
{match_list}
{hl_html}
{bottom_row(ins_s)}
{foot(6)}</div>''')

    # =============== PAGE 7: MATCH REPLAYS ===============
    if has_m:
        def match_card(m):
            r, rc = res(m)
            tags = []
            if m is best_o: tags.append(("SEASON-HIGH POINTS", AM))
            if m is best_d: tags.append(("BEST DEFENSIVE MATCH", PU))
            if m is best_w and m["f"] > m["a"]: tags.append(("BIGGEST MARGIN", G))
            if has_yds and m["yds"] == max(x["yds"] for x in M): tags.append(("MOST YARDS", BL))
            if has_top and m["top"] == max(x["top"] for x in M): tags.append(("LONGEST POSSESSION", "#00897b"))
            if not tags: tags.append(("SOLID WIN" if r == "W" else "TOUGH LOSS" if r == "L" else "DRAW", rc))
            sent = []
            if m is best_o: sent.append(f"Season-high {m['f']} points")
            if m is best_d: sent.append(f"only {m['a']} points allowed, the best defensive match")
            if has_yds and m["yds"] == max(x["yds"] for x in M): sent.append(f"{m['yds']} yards, the most of the season")
            if not sent: sent.append(f"{m['f']} points scored, {m['a']} allowed")
            txt = (", ".join(sent)).capitalize() + f". Margin {m['f']-m['a']:+d} against {m['opp']}" + (f"; the team held the ball for {mt(m['top'])}." if m["top"] else ".")
            rows = [("Points for", (m["f"] / avg_f - 1) * 100 if avg_f else 0, "high", m["f"]), ("Points against", (m["a"] / avg_a - 1) * 100 if avg_a else 0, "low", m["a"])]
            if has_yds: rows.append(("Yards", (m["yds"] / avg_y - 1) * 100 if avg_y else 0, "high", m["yds"]))
            if has_top: rows.append(("Possession", (m["top"] / avg_t - 1) * 100 if avg_t else 0, "high", mt(m["top"])))
            chips = "".join(f'<span class="tag" style="background:{col}">{t}</span>' for t, col in tags)
            word = {"W": "WIN", "L": "LOSS", "D": "DRAW"}[r]
            grad = {"W": "linear-gradient(160deg,#2e7d32,#4caf50)", "L": "linear-gradient(160deg,#b71c1c,#f44336)", "D": "linear-gradient(160deg,#607d8b,#90a4ae)"}[r]
            return (f'<div class="mc"><div class="sb" style="background:{grad}"><div class="r">{word}</div><div class="s">{m["f"]}–{m["a"]}</div><div class="m">{m["f"]-m["a"]:+d}</div></div>'
                    f'<div class="bd"><h4>Match {m["n"]} · vs {m["opp"][:28]}</h4><p>{txt}</p>{chips}</div>'
                    f'<div style="padding:10px 12px 0"><div style="font-size:11.5px;font-weight:800;letter-spacing:1.5px;color:#8a93a6;margin-bottom:2px">VS SEASON AVERAGE</div>{mini_vs(rows)}</div></div>')
        rows_vs = [("Points for", avg_f, f"{avg_f:.1f}", [m["f"] for m in Mr], "high"), ("Points against", avg_a, f"{avg_a:.1f}", [m["a"] for m in Mr], "low")]
        if has_yds: rows_vs.append(("Yards", avg_y, f"{avg_y:.0f}", [m["yds"] for m in Mr], "high"))
        if has_top: rows_vs.append(("Possession", avg_t, mt(int(avg_t)), [m["top"] for m in Mr], "high"))
        cum_r = cum_line(930, 118, cum[-6:], [f"After M{m['n']}" for m in Mr], G) if len(Mr) >= 2 else nap("Needs at least 2 matches.", 118)
        cards = "".join(match_card(m) for m in Mr[-4:])
        rw = sum(1 for m in Mr if m["f"] > m["a"]); rl = sum(1 for m in Mr if m["f"] < m["a"]); rd = sum(1 for m in Mr if m["f"] == m["a"])
        pages.append(f'''<div class="page big">{header("MATCH REPLAYS", "GAME BY GAME")}
{cards}
{panel("Recent Matches Against the Season Average", "target", '<div style="padding:6px 10px 6px">' + vs_avg(930, rows_vs, rh=38) + '<div class="cap">Numbered dots are the recent matches in order. Green = better than the season average, red = worse (for points against, lower is better).</div></div>', style="margin-top:14px")}
{panel("Season Point Differential (running total)", "trend", cum_r, style="margin-top:14px")}
{bottom_row([f"Best margin {best_w['f']-best_w['a']:+d} (match {best_w['n']}); best offensive match {best_o['f']} points (match {best_o['n']}); best defensive match {best_d['a']} allowed (match {best_d['n']}).",
             f"Record in the shown matches: {rw} wins, {rl} losses, {rd} draws.",
             f"Average match: {avg_f:.1f} scored, {avg_a:.1f} allowed" + (f", {avg_y:.0f} yards." if has_yds else ".")])}
{foot(7)}</div>''')
    else:
        pages.append(f'''<div class="page big">{header("MATCH REPLAYS", "GAME BY GAME")}
{panel("Match Details", "target", nap("Match-by-match results are not available yet. Log matches in the app and they will appear here.", 480), style="margin-top:16px")}
{foot(7)}</div>''')
    # ---- remaining sections are added below

    # =============== TOP PERFORMERS (2 pages) ===============
    RK = [AM, "#9aa5b4", "#c9803a"]
    def sil(): return silhouette()
    def phto(p): return f'<img src="{p["photo"]}" style="width:100%;height:100%;object-fit:cover;object-position:50% 20%">' if p.get("photo") else sil()
    def short(p, k=16): return p["name"] if len(p["name"]) <= k else p["name"][:k - 1] + "…"
    if P:
        ranked = sorted(P, key=lambda p: (-p["impact"], -p["scrim"], p["name"]))
        mvp = ranked[0]
        offl = max(P, key=lambda p: (p["scrim"] / 10 + p["otd"] * 6, p["scrim"]))
        defl = max(P, key=lambda p: (p["idx"], p["flags"]))
        tot_scrim = sum(p["scrim"] for p in P); tot_otd = sum(p["otd"] for p in P)
        # ---- page 8
        mvp_chips = [(f"{mvp['scrim']}", "Scrimmage yds"), (f"{mvp['td']}", "Touchdowns"), (f"{mvp['idx']}", "Defense index"), (f"{mvp['dint'] + mvp['sacks'] + mvp['pbu']}", "Disruptive plays")]
        chips = "".join(f'<div class="tpc"><b>{v}</b>{l}</div>' for v, l in mvp_chips)
        num_txt = f"#{mvp['number']}" if mvp["number"] else ""
        hero = (f'<div class="tphero"><div class="yl"></div><div class="jn">{num_txt}</div><div class="ph">{phto(mvp)}</div>'
                f'<div class="tx"><div class="kick">TEAM MVP · MOST TOTAL IMPACT</div><div class="nm">{mvp["name"]}</div>'
                f'<div class="big"><b>{mvp["impact"]:g}</b><span>IMPACT SCORE</span></div></div><div class="chs">{chips}</div></div>')
        def pod(rk, p):
            tp = p["scrim"] / 10; ot = p["otd"] * 6; di = p["idx"]; tt = max(tp + ot + di, 1)
            seg = "".join(f'<i style="width:{v/tt*100:.1f}%;background:{col}"></i>' for v, col in [(tp, NAVY), (ot, RED), (di, "#6a1fa0")])
            return (f'<div class="pod"><div class="pk" style="background:{RK[rk]}">{rk+1}</div><div class="pp">{phto(p)}</div><div class="pn">{short(p, 15)}</div>'
                    f'<div class="pv">{p["impact"]:g}<small>IMPACT</small></div><div class="pb">{seg}</div></div>')
        podium = '<div class="podium">' + "".join(pod(i, p) for i, p in enumerate(ranked[:3])) + '</div>'
        pod_leg = f'<div class="cap" style="padding-top:6px"><span style="color:{NAVY}">■</span> yards ÷ 10 &nbsp; <span style="color:{RED}">■</span> offensive TD × 6 &nbsp; <span style="color:#6a1fa0">■</span> defense index</div>'
        cats = [("Passing Yards", "pyd", NAVY), ("Receiving Yards", "ryd", BL), ("Rushing Yards", "rsy", G), ("Touchdowns", "td", AM),
                ("Interceptions", "dint", PU), ("Sacks", "sacks", RED), ("Flags Pulled", "flags", "#607d8b"), ("Pass Breakups", "pbu", OR)]
        def leadcard(title, key, col):
            top = sorted([p for p in P if p[key] > 0], key=lambda p: (-p[key], p["name"]))[:3]
            if not top: body = '<div style="color:#9aa0ab;font-size:13px;font-weight:600;padding:14px 4px">No data yet</div>'
            else:
                m0 = top[0][key]
                body = "".join(f'<div class="lr"><div class="lt"><span>{i+1}. {short(p, 13)}</span><b>{p[key]}</b></div><div class="lb"><i style="width:{p[key]/m0*100:.0f}%;background:{col}"></i></div></div>' for i, p in enumerate(top))
            return f'<div class="lc"><div class="lh" style="background:{col}">{title}</div>{body}</div>'
        lead_html = '<div class="lgrid">' + "".join(leadcard(*c_) for c_ in cats) + '</div>'
        ins_t = [f"{mvp['name']} has the highest total impact ({mvp['impact']:g}): {mvp['scrim']} scrimmage yards, {mvp['td']} touchdowns and a {mvp['idx']} defensive index.",
                 f"Best offensive player: {offl['name']} ({offl['scrim']} yards, {offl['otd']} offensive TDs). Best defender: {defl['name']} (index {defl['idx']}).",
                 f"The top 3 players account for {div0(sum(p['scrim'] for p in ranked[:3]), tot_scrim)*100:.0f}% of the roster's scrimmage yards." if tot_scrim else "No scrimmage yards recorded yet."]
        pages.append(f'''<div class="page big">{header("TOP PERFORMERS", "STAR PLAYERS")}
{hero}
{panel("Impact Podium", "trophy", podium + pod_leg, style="margin-top:14px")}
<div class="sec" style="margin-top:14px"><i></i>CATEGORY LEADERS</div>
{lead_html}
{bottom_row(ins_t)}
{foot(8)}</div>''')

        # ---- page 9: roster ranking
        top10 = ranked[:10]
        mx_imp = max(p["impact"] for p in top10) or 1
        rows = '<div class="rk-h"><div>#</div><div>PLAYER</div><div>IMPACT BREAKDOWN</div><div>YARDS</div><div>TD</div><div>DEF</div><div>IMPACT</div></div>'
        for i, p in enumerate(top10):
            tp, ot, di = p["scrim"] / 10, p["otd"] * 6, p["idx"]
            seg = "".join(f'<i style="width:{v/mx_imp*100:.1f}%;background:{col}"></i>' for v, col in [(tp, NAVY), (ot, RED), (di, "#6a1fa0")])
            rows += (f'<div class="rk-r"><div class="n" style="background:{RK[i] if i < 3 else "#d5dae4"};color:{"#fff" if i < 3 else NAVY}">{i+1}</div><div class="nm">{short(p, 20)}<small>{("#" + p["number"]) if p["number"] else ""}</small></div>'
                     f'<div class="bar">{seg}</div><div>{p["scrim"]}</div><div>{p["td"]}</div><div>{p["idx"]}</div><div class="im">{p["impact"]:g}</div></div>')
        def share_donut(key, title, unit, total_):
            tops = sorted([p for p in P if p[key] > 0], key=lambda p: -p[key])[:4]
            cols_ = [NAVY, RED, G, AM, "#9aa0ab"]
            vals = [p[key] for p in tops]; rest = total_ - sum(vals)
            if rest > 0: vals.append(rest)
            if not vals: return nap("No data yet.", 190)
            labs = [short(p, 12) for p in tops] + (["Others"] if rest > 0 else [])
            leg = "".join(f'<div><i style="background:{cols_[i]}"></i><b>{v/total_*100:.0f}%</b>{labs[i]}</div>' for i, v in enumerate(vals))
            return f'<div style="display:flex;align-items:center;gap:12px;padding:8px 10px">{donut_custom(170, vals, cols_[:len(vals)], total_, unit)}<div class="legend">{leg}</div></div>'
        offs = sorted(P, key=lambda p: -(p["scrim"] / 10 + p["otd"] * 6))[:5]
        defs = sorted(P, key=lambda p: -p["idx"])[:5]
        def minilist(items, key_fn, fmt_, col):
            m0 = max([key_fn(p) for p in items] + [1])
            return '<div style="padding:8px 12px 6px">' + "".join(f'<div class="lr"><div class="lt"><span>{i+1}. {short(p, 18)}</span><b>{fmt_(p)}</b></div><div class="lb"><i style="width:{key_fn(p)/m0*100:.0f}%;background:{col}"></i></div></div>' for i, p in enumerate(items)) + '</div>'
        two_way = [p for p in P if p["scrim"] >= 50 and p["idx"] >= 10]
        tw_txt = (", ".join(short(p, 16) for p in two_way[:3]) + (" produce on both sides of the ball." if len(two_way) > 1 else " produces on both sides of the ball.")) if two_way else "No player has strong production on both offense and defense yet."
        ins_r = [f"{len(P)} players have recorded stats; the ranking uses the Impact Score = yards ÷ 10 + offensive TDs × 6 + defensive index.",
                 f"Best offensive output: {offs[0]['name']} ({offs[0]['scrim']} yards, {offs[0]['otd']} offensive TDs)." if offs and offs[0]["scrim"] else "No offensive output recorded yet.",
                 tw_txt]
        pages.append(f'''<div class="page big">{header("TOP PERFORMERS", "IMPACT RANKING")}
{panel("Roster Impact Ranking (top 10)", "bars", '<div class="rk">' + rows + '</div>' + pod_leg, style="margin-top:16px")}
<div class="row2" style="margin-top:14px">
{panel("Share of Roster Yards", "target", share_donut("scrim", "yards", "yards", tot_scrim), style="flex:1")}
{panel("Who Scores the Touchdowns", "trophy", share_donut("otd", "TDs", "off. TDs", tot_otd), style="flex:1")}
</div>
<div class="row2" style="margin-top:14px">
{panel("Top Offensive Players", "run", minilist(offs, lambda p: p["scrim"] / 10 + p["otd"] * 6, lambda p: f"{p['scrim']} yds · {p['otd']} TD", NAVY), style="flex:1")}
{panel("Top Defensive Players", "bolt", minilist(defs, lambda p: p["idx"], lambda p: f"idx {p['idx']}", "#6a1fa0"), style="flex:1")}
</div>
{bottom_row(ins_r)}
{foot(9)}</div>''')

    # =============== COACH'S CORNER ===============
    ppm = pass_att / n
    if run_share is not None and run_share >= 65:
        c1 = ("Stack the box", RED, f"They will put extra defenders near the line, because {run_share:.0f}% of our yards are rushing and we averaged {ppm:.1f} pass attempts per match.", "quick passes and play-action; build real passing volume.")
    elif run_share is not None and run_share <= 35:
        c1 = ("Bracket the receivers", RED, f"They will double our top targets, because {100-run_share:.0f}% of our yards come through the air.", "a run package and screens to punish the coverage.")
    else:
        c1 = ("Take away our first option", RED, "With a balanced attack they will try to take away whichever option is working that day.", "stay balanced and attack the weakest matchup.")
    if T["def_int"] / n >= 1.5:
        c2 = ("Avoid our coverage", PU, f"They will not test us deep: {T['def_int']} interceptions and {T['pbu']} breakups say throwing into our zones is costly.", "disguise coverages and keep the pass rush honest, so they must throw.")
    elif T["sacks"] / n >= 2:
        c2 = ("Get the ball out fast", PU, f"They will use quick throws to beat our pass rush ({T['sacks']} sacks).", "tighten the underneath coverage and rotate rushers.")
    else:
        c2 = ("Test our defense", PU, f"They will probe for weaknesses: we allow {avg_a:.1f} points per match.", "set a clear defensive plan and win the turnover battle.")
    if rz_eff is not None and rz_eff < 70:
        c3 = ("Make us settle", BL, f"They will aim to hold us in the red zone: {T['rz_trips']-T['rz_scores']} of {T['rz_trips']} trips ended without a score.", "a short-yardage package, a two-point plan and a fast tempo inside the 20.")
    else:
        c3 = ("Slow the game down", BL, "They will try to shorten the game and control the clock to limit our possessions.", "keep the tempo up and score on the first drives.")
    cc = '<div class="cmpc">' + "".join(f'<div class="cc"><div class="t" style="background:{col}">{icon("target", "#fff", 18)}{t}</div><div class="b">{d}<em>OUR ANSWER</em>{a}</div></div>' for t, col, d, a in [c1, c2, c3]) + '</div>'
    goals = [("Pass attempts / match", f"{ppm:.1f}", 8, ppm, "≥ 8", "high"), ("Points allowed / match", f"{avg_a:.1f}", 18, avg_a, "≤ 18", "low"),
             ("Interceptions / match", f"{T['def_int']/n:.1f}", 2, T["def_int"] / n, "≥ 2.0", "high"), ("Interceptions thrown", f"{T['int_thrown']}", 0, T["int_thrown"], "0", "low")]
    if rz_eff is not None: goals.insert(1, ("Red zone efficiency", f"{rz_eff:.0f}%", 75, rz_eff, "≥ 75%", "high"))
    if td_eff is not None: goals.insert(2, ("3rd down conversion", f"{td_eff:.0f}%", 60, td_eff, "≥ 60%", "high"))
    cl = ""
    for lab, cur, tgt, v, tx, bt in goals:
        ok = (v >= tgt) if bt == "high" else (v <= tgt)
        ratio = min(v / tgt, 1) if bt == "high" and tgt else (1 if ok else max(0, tgt / v if v else 1))
        col = G if ok else OR
        cl += (f'<div class="cl"><div class="bx"></div><div><b>{lab}</b><small>now {cur} · target {tx}</small></div><div class="pg"><i style="width:{ratio*100:.0f}%;background:{col}"></i></div>'
               f'<div class="tv" style="color:{col}">{"ON TRACK" if ok else "BUILD"}</div></div>')
    off_f = []
    if ppm < 8: off_f.append("Passing tree: 15 min/day of route timing")
    if rz_eff is not None and rz_eff < 75: off_f.append("Red-zone and short-yardage reps")
    off_f.append("Ball security: carry and pitch drills")
    if len(off_f) < 3: off_f.append("Tempo and two-minute offense")
    def_f = []
    if avg_a > 18: def_f.append("Tackle form to cut points allowed")
    def_f += ["Disguised coverage and zone-turnover drills", "Pass-rush stunts to keep the sack rate up"]
    trk = []
    if not has_top: trk.append("Log time of possession")
    if T["rz_trips"] is None or T["third_att"] is None: trk.append("Log red-zone trips and third downs")
    if not has_yds: trk.append("Log yards for every match")
    trk += ["Record every drive result", "Log carries, fumbles and penalties"]
    focus = [("OFFENSE", RED, off_f[:3]), ("DEFENSE", PU, def_f[:3]), ("TRACKING", NAVY, trk[:3])]
    fc = '<div class="cmpc">' + "".join(f'<div class="cc"><div class="t" style="background:{col}">{t}</div><div class="b">' + "".join(f'<div style="display:flex;gap:8px;margin:4px 0"><span style="color:{col};font-weight:900">▸</span><span>{x}</span></div>' for x in xs) + '</div></div>' for t, col, xs in focus) + '</div>'
    first_weak = W2[0][0].lower() if W2 and W2[0][0] not in ("Keep tracking",) else "consistency"
    pages.append(f'''<div class="page big">{header("COACH'S CORNER", "ACTION PLAN")}
{story("THE COACH'S READ", "Keep what works, build what is missing", f"The plan for the next matches: protect what already works (<b>{S_[0][0].lower()}</b>) while fixing the biggest gap (<b>{first_weak}</b>). The goals below are suggested targets and can be edited by the coaching staff.")}
{panel("How an Opponent Would Try to Beat Us (and Our Answer)", "target", cc, style="margin-top:14px")}
{panel("Next-Match Goals (suggested targets, edit as you wish)", "check", cl, style="margin-top:14px")}
{panel("Training Focus This Week", "dumb", fc, style="margin-top:14px")}
<div class="note2" style="margin-top:14px;height:215px"><div class="nt2">{icon("note", NAVY, 24)}Coach's Notes :</div><div class="nl"></div><div class="nl"></div><div class="nl"></div></div>
{foot(10)}</div>''')

    # =============== DATA AUDIT & GLOSSARY ===============
    checks = []
    def chk(t, ok, d): checks.append((t, ok, d))
    chk("Record adds up", wins + losses + draws == T["matches"], f"Wins + losses + draws = {wins+losses+draws}; matches played = {T['matches']}.")
    if has_m:
        okm = sum(m["f"] for m in M) == pf and sum(m["a"] for m in M) == pa and (not has_yds or (tot and sum(m["yds"] for m in M) == tot) or not tot)
        chk("Match records match totals", okm, "Points" + (" and yards" if has_yds else "") + " of each match sum to the team totals." if okm else f"Matches sum to {sum(m['f'] for m in M)}–{sum(m['a'] for m in M)} vs team totals {pf}–{pa}.")
    chk("Touchdown split", T["pass_td"] + T["rush_td"] == T["off_td"], f"Passing TDs {T['pass_td']} + rushing TDs {T['rush_td']} = {T['pass_td']+T['rush_td']}; offensive TDs = {T['off_td']}.")
    if T["rz_trips"] is not None or T["third_att"] is not None:
        chk("Red zone and 3rd down", (T["rz_scores"] or 0) <= (T["rz_trips"] or 0) and (T["third_conv"] or 0) <= (T["third_att"] or 0), "Scores ≤ trips and conversions ≤ attempts.")
    chk("Yards reconcile", tot == pas + rush, f"Total {tot} yds vs passing {pas} + rushing {rush} = {pas+rush}." + (f" {tot-pas-rush:+d} yards unexplained (returns? penalties?)." if tot != pas + rush else ""))
    chk("Points vs touchdowns", pts_td <= pf <= td_all * 8 if td_all else pf == 0, f"{td_all} TDs explain {pts_td} to {td_all*8} points (6 + 2-point conversion). The team scored {pf}.")
    chk("Passing sample", pass_att >= 10, f"{plural(pass_att, 'pass attempt')} in {plural(n, 'match', 'matches')}." + ("" if pass_att >= 10 else " Completion % and yards per attempt are not meaningful."))
    if P and not ({"pass_yds", "rush_yds"} & set(notes)):
        sp, sr = sum(p["pyd"] for p in P), sum(p["rsy"] for p in P)
        chk("Players add up to the team", sp == pas and sr == rush, f"Player passing {sp} vs team {pas}; player rushing {sr} vs team {rush}.")
    au = ""
    for nm_, ok, det in checks:
        col = G if ok else OR
        au += f'<div class="au"><div class="ic" style="background:{col}">{"✓" if ok else "!"}</div><b>{nm_}</b><span>{det}</span><div class="st" style="background:{col}22;color:{col}">{"CONSISTENT" if ok else "REVIEW"}</div></div>'
    confs = [("Win rate", n, "matches"), ("Per-match averages", n, "matches"), ("Completion %", pass_att, "attempts"), ("Red zone efficiency", T["rz_trips"] or 0, "trips"), ("3rd down %", T["third_att"] or 0, "attempts"), ("Turnover margin", n, "matches")]
    cf = ""
    for lab, n_, unit in confs:
        lvl, bar = conf_bar(n_, 5, 15, 30)
        cf += f'<div class="cf"><b>{lab}</b>{bar}<small>n = {n_} {unit} · {["very low", "low", "medium", "high"][lvl-1]}</small></div>'
    gloss = [("Pt Diff", "Points for − points against."), ("Expected Win %", "PF² ÷ (PF² + PA²), the Pythagorean expectation."), ("Yards per Point", "Total yards ÷ points for. Lower = more efficient."),
             ("Run Share", "Rushing yards ÷ (passing + rushing yards)."), ("Red Zone Eff.", "Red-zone scores ÷ red-zone trips."), ("3rd Down %", "Third-down conversions ÷ attempts."),
             ("Turnover Margin", "Takeaways − giveaways (interceptions here)."), ("Disruptive Plays", "Interceptions + pass breakups + sacks."), ("Impact Score", "Player yards ÷ 10 + offensive TDs × 6 + defensive index."),
             ("Defensive Index", "Flags×1 + INT×3 + Sacks×3 + PBU×2 + Def TD×6.")]
    gl = '<div class="gl">' + "".join(f"<div><b>{a}</b> · {b}</div>" for a, b in gloss) + "</div>"
    n_rev = sum(1 for ch in checks if not ch[1])
    pages.append(f'''<div class="page big">{header("DATA AUDIT", "&amp; GLOSSARY")}
{story("BEFORE YOU TRUST THE NUMBERS", f"{len(checks)-n_rev} checks passed, {n_rev} need a second look", "A report is only as good as the data behind it. These automatic checks compare the numbers against each other to catch entry mistakes and missing tracking, and show how much weight each statistic can carry.")}
{panel("Automatic Data Checks", "check", au, style="margin-top:14px")}
{panel("How Much Can Each Number Be Trusted? (sample-size confidence)", "target", cf + '<div class="cap" style="padding:6px 14px 6px">Confidence = number of observations behind a rate: under 5 very low, under 15 low, under 30 medium, 30 or more high.</div>', style="margin-top:14px")}
{panel("Glossary: How Each Metric Is Calculated", "bulb", gl, style="margin-top:14px")}
{foot(11)}</div>''')
    return pages
