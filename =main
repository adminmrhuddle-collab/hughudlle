"""Builds the 7 report pages (HTML strings) from the validated request. All numbers/text are computed here."""
import math
from components import *
import components as C

COLORS = [("#d9091f", "#fdeaec"), ("#1f6fd6", "#e8f0fc"), ("#3a9a2c", "#eaf5e8"), ("#f57c10", "#fef1e4"), ("#6a1fa0", "#f1e8f8")]
N = 5


def nice(mx, target=5):
    """Return (axis_max, ticks, step) so that a chart axis always covers the data."""
    mx = max(float(mx), 1.0)
    for step in (1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 5000, 10000):
        if math.ceil(mx * 1.08 / step) <= target + 1:
            top = int(math.ceil(mx * 1.08 / step) * step)
            return top, list(range(0, top + 1, step)), step
    top = int(math.ceil(mx * 1.08))
    return top, [0, top], top


def num(v, default=0):
    try:
        f = float(v)
        return int(f) if f == int(f) else f
    except (TypeError, ValueError):
        return default


def clip(s, n):
    s = str(s or "").strip()
    return s if len(s) <= n else s[:n - 1] + "…"


def build_pages(players, team):
    # ---------- players ----------
    PL[:] = []
    for i, p in enumerate(players):
        parts = str(p.get("name") or f"Player {i+1}").split()
        c, tint = COLORS[i]
        PL.append(dict(n1=clip(parts[0], 13), n2=clip(" ".join(parts[1:]), 14), num=clip(p.get("number") or "", 3), pos=clip(str(p.get("position") or "").upper(), 4),
                       c=c, tint=tint, photo=p.get("photo_data_uri")))
    S = lambda key: [num((p.get("stats") or {}).get(key)) for p in players]
    R = range(N)
    P = lambda key: [num(p.get(key)) for p in players]
    exp, hgt, wgt, vj = P("experience"), P("height"), P("weight"), P("verticalJump")
    dash_raw = P("dash40")
    valid = [d for d in dash_raw if d and d > 0]
    dash_fill = sum(valid) / len(valid) if valid else 5.0
    dash = [d if d and d > 0 else dash_fill for d in dash_raw]
    att, comp, yds, tds, ints = S("passingAttempts"), S("completions"), S("passingYards"), S("passingTDs"), S("interceptionsThrown")
    flags, dint, sacks, sallow, pbu, dtd = S("flagsPulled"), S("defensiveInterceptions"), S("sacks"), S("sacksAllowed"), S("passBreakups"), S("defensiveTDs")
    rec, ryd, rtd = S("receptions"), S("receivingYards"), S("receivingTDs")
    car, rsy, rstd = S("carries"), S("rushingYards"), S("rushingTDs")
    div = lambda a, b: (a / b) if b else 0
    pct = [round(div(comp[i], att[i]) * 100) for i in R]
    ypr = [div(ryd[i], rec[i]) for i in R]
    ypc = [div(rsy[i], car[i]) for i in R]
    nmf = lambda i: f"{PL[i]['n1']} {PL[i]['n2']}".strip()
    arg = lambda v: max(R, key=lambda i: (v[i], -i))
    mx = lambda v: max(max(v), 1)

    # ---------- derived ----------
    idx = [flags[i] + dint[i] * 3 + sacks[i] * 3 + pbu[i] * 2 + dtd[i] * 6 for i in R]
    rows_idx = sorted(R, key=lambda i: -idx[i])
    stk = [(i, [(flags[i], FLD["flags"]), (dint[i] * 3, FLD["ints"]), (sacks[i] * 3, FLD["sacks"]), (pbu[i] * 2, FLD["pbu"]), (dtd[i] * 6, FLD["td"])], idx[i]) for i in rows_idx]
    tot_y = [yds[i] + ryd[i] + rsy[i] for i in R]
    td_inv = [tds[i] + rtd[i] + rstd[i] + dtd[i] for i in R]
    sc_sp = [min(dash) / d * 100 for d in dash]
    sc_jm = [v / mx(vj) * 100 for v in vj]
    sc_sz = [v / mx(wgt) * 100 for v in wgt]
    sc_ht = [v / mx(hgt) * 100 for v in hgt]
    sc_ex = [v / mx(exp) * 100 for v in exp]
    team_att, team_comp = sum(att), sum(comp)
    foot_ = lambda n: foot(n)
    pages = []

    # =============== PAGE 1: PHYSICAL PROFILE ===============
    phys_cols = [dict(n="Experience", ic="trophy", v=exp, f=lambda v: f"{v} yrs", b="high"),
                 dict(n="Height", ic="person", v=hgt, f=lambda v: f"{v} cm", b="high"),
                 dict(n="Weight", ic="weight", v=wgt, f=lambda v: f"{v} kg", b="high"),
                 dict(n="40 Yard Dash", ic="clock", v=dash, f=lambda v: f"{v:.2f} s", b="low"),
                 dict(n="Vertical Jump", ic="run", v=vj, f=lambda v: f"{v} cm", b="high")]
    phys_avg = [f"{sum(exp)/N:.1f} yrs", f"{sum(hgt)/N:.1f} cm", f"{sum(wgt)/N:.1f} kg", f"{sum(dash)/N:.2f} s", f"{sum(vj)/N:.1f} cm"]
    rad_axes = ["Speed\n(40 yd)", "Jump\n(vertical)", "Size\n(weight)", "Height", "Experience"]
    rad1 = radar_n(300, 240, 70, rad_axes, [(PL[i]["c"], [sc_sp[i], sc_jm[i], sc_sz[i], sc_ht[i], sc_ex[i]]) for i in R], font=12.5, dots=3.2, fill=0.10)
    rad_leg = "".join(f'<div><i style="background:{p["c"]}"></i>{p["n1"]}</div>' for p in PL)
    fast, jump = min(R, key=lambda i: dash[i]), arg(vj)
    big = arg([wgt[i] + exp[i] * 0.01 for i in R]); vmax_, vticks, _ = nice(max(vj), 5)
    ins1 = (f"{nmf(fast)} is both the fastest ({dash[fast]:.2f} s) and the highest jumper ({vj[jump]} cm)." if fast == jump
            else f"{nmf(fast)} is the fastest ({dash[fast]:.2f} s); {nmf(jump)} jumps highest ({vj[jump]} cm).")
    ins2 = (f"{nmf(big)} is the biggest: {wgt[big]} kg and {hgt[big]} cm" + (f"; {nmf(arg(exp))} has the most experience ({max(exp)} yrs)." if arg(exp) != big else f", with {exp[big]} years of experience."))
    ins3 = f"Team averages: {sum(dash)/N:.2f} s in the 40, {sum(vj)/N:.1f} cm vertical, {sum(wgt)/N:.1f} kg."
    pages.append(f'''<div class="page big">{header("PHYSICAL PROFILE", "TEAM REPORT")}
{pcards()}
{heat2(phys_cols, phys_avg, pad=5)}
{panel("40-Yard Dash — Race View", "clock", race(950, dash) + f'<div class="cap">Estimate: where each player would be when the fastest time ({min(dash):.2f} s) crosses the 40-yard line, assuming constant speed. Last 10 yards shown.</div>', style="margin-top:14px")}
<div class="row2" style="margin-top:14px">
{panel("Athletic Profile (100 = team best)", "target", '<div style="display:flex;align-items:center;gap:6px;padding:2px 4px">' + rad1 + '<div class="legend" style="margin-left:0">' + rad_leg + '</div></div>', style="flex:1")}
{panel("Vertical Jump", "bolt", lollipop_n(458, 240, vj, vmax_, vticks, lambda i, v: f"{v} cm"), style="flex:1")}
</div>
{foot(1)}</div>''')

    # =============== PAGE 2: PASSING ===============
    ql = arg([yds[i] * 1000 + att[i] for i in R])
    pass_cols = [("Pass Att", "run", att, str), ("Completions", "check", comp, str), ("Comp %", "target", pct, lambda v: f"{v}%"),
                 ("Passing Yds", "ball", yds, str), ("Passing TDs", "trophy", tds, str), ("INT Thrown", "warn", ints, str)]
    team_pass = [team_att, team_comp, f"{div(team_comp, team_att)*100:.1f}%" if team_att else "n/a", sum(yds), sum(tds), sum(ints)]
    ymax_, yt_, _ = nice(max(max(tds), max(ints)), 5)
    low = [nmf(i) for i in R if 0 < att[i] <= 5 and i != ql]
    ins_p3 = (f"{len(low)} other passer{'s' if len(low) != 1 else ''} ha{'ve' if len(low) != 1 else 's'} 5 attempts or fewer, so their percentages swing widely." if low
              else "Completion % is only meaningful with enough attempts; compare it together with the attempts shown.")
    pages.append(f'''<div class="page big">{header("PASSING STATISTICS", "TEAM REPORT")}
{hero(PL[ql], "PASSING LEADER", yds[ql], "PASSING YARDS", [(f"{comp[ql]}/{att[ql]}", "Comp"), (f"{pct[ql]}%" if att[ql] else "n/a", "Comp %"), (tds[ql], "TD"), (ints[ql], "INT")])}
{bar_table(pass_cols, team_pass)}
<div class="row2" style="margin-top:16px">
{panel("Team Passing Funnel", "ball", funnel(458, 220, att, comp, tds), style="flex:1")}
{panel("Share of Passing Yards", "target", share_panel_body(yds, f"{sum(yds):,}", "total yards", 196), style="flex:1")}
</div>
<div class="row2" style="margin-top:16px">
{panel("Completion % (attempts)", "check", lollipop_n(458, 232, pct, 100, [0, 20, 40, 60, 80, 100], lambda i, v: ("n/a" if att[i] == 0 else f"{v}%") + (f" ({att[i]})" if att[i] else ""), R=96), style="flex:1")}
{panel("Touchdowns vs Interceptions", "warn", diverge(458, 232, ints, tds, ymax_, yt_[1:]), style="flex:1")}
</div>
{bottom_row([f"{nmf(ql)} leads the passing game: {att[ql]} of the team's {team_att} attempts, {yds[ql]} yards, {tds[ql]} TD and {ints[ql]} INT.",
  f"As a team the players complete {div(team_comp, team_att)*100:.1f}% and average {div(sum(yds), team_att):.1f} yards per attempt." if team_att else "No pass attempts have been recorded yet.",
  ins_p3])}
{foot(2)}</div>''')

    # =============== PAGE 3: DEFENSE ===============
    dl = arg(idx)
    def_cols = [("Flags Pulled", "target", flags), ("Def INT", "ball", dint), ("Sacks", "bolt", sacks),
                ("Sacks Allowed", "check", sallow), ("Pass Breakups", "bal", pbu), ("Defensive TDs", "trophy", dtd)]
    g_max, g_t, _ = nice(max(max(dint), max(sacks), max(pbu), max(dtd)), 5)
    s_max, s_t, _ = nice(max(idx), 6)
    sa_txt = ("Zero sacks allowed across the whole team." if sum(sallow) == 0 else f"{sum(sallow)} sacks allowed, most by {nmf(arg(sallow))} ({max(sallow)}).")
    sa_cap = " Sacks Allowed is 0 for every player." if sum(sallow) == 0 else ""
    pages.append(f'''<div class="page big">{header("DEFENSE STATISTICS", "TEAM REPORT")}
{hero(PL[dl], "DEFENSIVE IMPACT LEADER", idx[dl], "IMPACT INDEX", [(flags[dl], "Flags"), (dint[dl], "INT"), (sacks[dl], "Sacks"), (dtd[dl], "Def TD")])}
{kpis([(sum(flags), "FLAGS PULLED"), (sum(dint), "INTERCEPTIONS"), (sum(sacks), "SACKS"), (sum(pbu), "PASS BREAKUPS"), (sum(dtd), "DEFENSIVE TDs")])}
{heat_table(def_cols)}
<div class="row2" style="margin-top:16px">
{panel("Defensive Playmakers", "bolt", grouped(458, 292, [("INT", FLD["ints"], dint), ("Sacks", FLD["sacks"], sacks), ("Pass Breakups", FLD["pbu"], pbu), ("Def TD", FLD["td"], dtd)], g_max, g_t), style="flex:1")}
{panel("Defensive Impact Index", "star", stacked_h(458, 262, stk, s_max, s_t, [("Flags ×1", FLD["flags"]), ("INT ×3", FLD["ints"]), ("Sacks ×3", FLD["sacks"]), ("PBU ×2", FLD["pbu"]), ("TD ×6", FLD["td"])]) + f'<div class="cap">Custom index = Flags×1 + INT×3 + Sacks×3 + Pass Breakups×2 + Def TD×6.{sa_cap}</div>', style="flex:1")}
</div>
{bottom_row([f"{nmf(dl)} leads the unit with the top Impact Index ({idx[dl]}): {flags[dl]} flags pulled, {sacks[dl]} sacks, {dint[dl]} interceptions.",
  f"{nmf(arg(dint))} has the most interceptions ({max(dint)}) and {nmf(arg(pbu))} the most pass breakups ({max(pbu)})." if max(dint) + max(pbu) else "No interceptions or pass breakups have been recorded yet.",
  sa_txt])}
{foot(3)}</div>''')

    # =============== PAGE 4: RECEIVING ===============
    rl = arg(ryd)
    r_max, r_t, _ = nice(max(rec), 5); t_max, t_t, _ = nice(max(rtd), 5); yp_max, yp_t, _ = nice(max(ypr), 5)
    eff = [i for i in R if rec[i] >= 3 and i != rl]
    effi = max(eff, key=lambda i: ypr[i]) if eff else None
    vol = sorted(R, key=lambda i: -rec[i])[1] if sum(1 for v in rec if v) > 1 else None
    pages.append(f'''<div class="page big">{header("RECEIVING STATISTICS", "TEAM REPORT")}
{hero(PL[rl], "TOP TARGET", ryd[rl], "RECEIVING YARDS", [(rec[rl], "Receptions"), (rtd[rl], "TD"), (f"{ypr[rl]:.1f}", "Yds / Rec"), (f"{div(ryd[rl], sum(ryd))*100:.1f}%", "Team yards")])}
{bar_table([("Receptions", "check", rec, str), ("Receiving Yds", "ball", ryd, str), ("Receiving TDs", "trophy", rtd, str), ("Yds / Reception", "target", ypr, lambda v: f"{v:.1f}")],
           [sum(rec), sum(ryd), sum(rtd), f"{div(sum(ryd), sum(rec)):.1f}"])}
<div class="row2" style="margin-top:16px">
{panel("Share of Receiving Yards", "target", share_panel_body(ryd, sum(ryd), "total yards", 196), style="flex:1")}
{panel("Yards per Reception", "bolt", lollipop_h(458, 226, ypr, yp_max, yp_t, lambda v: f"{v:.1f}"), style="flex:1")}
</div>
<div class="row2" style="margin-top:16px">
{panel("Receptions", "bars", bar_chart(458, 236, rec, r_max, r_t, str), style="flex:1")}
{panel("Receiving Touchdowns", "trophy", bar_chart(458, 236, rtd, t_max, t_t, str), style="flex:1")}
</div>
{bottom_row([f"{nmf(rl)} is the go-to target: {ryd[rl]} yards, {div(ryd[rl], sum(ryd))*100:.1f}% of team receiving yards and {rtd[rl]} of the {sum(rtd)} TDs." if sum(ryd) else "No receiving yards have been recorded yet.",
  f"{nmf(effi)} is the next most efficient receiver at {ypr[effi]:.1f} yards per catch ({rec[effi]} receptions, {ryd[effi]} yards)." if effi is not None else "Not enough receptions from other players to rank efficiency (3 or more needed).",
  f"{nmf(vol)} is second in volume: {rec[vol]} receptions for {ryd[vol]} yards." if vol is not None else "Only one player has recorded receptions so far."])}
{foot(4)}</div>''')

    # =============== PAGE 5: RUSHING ===============
    ul = arg(rsy)
    l_max = max(nice(max(rsy), 12)[0], 12); _, _, l_step = nice(max(rsy), 12)
    l_vmax = int(math.ceil(max(max(rsy), 1) * 1.08 / l_step) * l_step)
    c_max, c_t, _ = nice(max(ypc), 5)
    effr = [i for i in R if car[i] >= 3 and i != ul]
    eb = max(effr, key=lambda i: ypc[i]) if effr else None
    sec = sorted(R, key=lambda i: -ypc[i]); 
    pages.append(f'''<div class="page big">{header("RUSHING STATISTICS", "TEAM REPORT")}
{hero(PL[ul], "RUSHING LEADER", rsy[ul], "RUSHING YARDS", [(car[ul], "Carries"), (rstd[ul], "TD"), (f"{ypc[ul]:.1f}", "Yds / Carry"), (f"{div(rsy[ul], sum(rsy))*100:.1f}%", "Team yards")])}
{bar_table([("Carries", "run", car, str), ("Rushing Yds", "ball", rsy, str), ("Rushing TDs", "trophy", rstd, str), ("Yds / Carry", "target", ypc, lambda v: f"{v:.1f}")],
           [sum(car), sum(rsy), sum(rstd), f"{div(sum(rsy), sum(car)):.1f}"])}
{panel("Rushing Yards — Field View", "run", lanes(950, rsy, l_vmax, l_step), style="margin-top:16px")}
<div class="row2" style="margin-top:16px">
{panel("Share of Rushing Yards", "target", share_panel_body(rsy, sum(rsy), "total yards", 196), style="flex:1")}
{panel("Yards per Carry", "bolt", lollipop_h(458, 226, ypc, c_max, c_t, lambda v: f"{v:.1f}"), style="flex:1")}
</div>
{bottom_row([f"{nmf(ul)} carries the ground game: {car[ul]} carries, {rsy[ul]} yards and {rstd[ul]} of the team's {sum(rstd)} rushing TDs ({div(rsy[ul], sum(rsy))*100:.1f}% of yards)." if sum(rsy) else "No rushing yards have been recorded yet.",
  f"{nmf(eb)} has the best average among regular carriers: {ypc[eb]:.1f} yards per carry on {car[eb]} attempts." if eb is not None else "Not enough carries from other players to rank efficiency (3 or more needed).",
  f"Team average: {div(sum(rsy), sum(car)):.1f} yards per carry on {sum(car)} carries." if sum(car) else "No carries recorded yet."])}
{foot(5)}</div>''')

    # =============== PAGE 6: ALL-PURPOSE ===============
    role_names = ["Passer", "Receiver", "Rusher", "Defender"]
    role_scores = [[yds[i] / mx(yds), ryd[i] / mx(ryd), rsy[i] / mx(rsy), idx[i] / mx(idx)] for i in R]
    roles = [role_names[max(range(4), key=lambda k: role_scores[i][k])] for i in R]
    ap_cols = [dict(n="Total Yards", ic="bars", v=tot_y, f=lambda v: f"{v:,}", b="high"),
               dict(n="Passing Yds", ic="ball", v=yds, f=str, b="high"), dict(n="Receiving Yds", ic="target", v=ryd, f=str, b="high"),
               dict(n="Rushing Yds", ic="run", v=rsy, f=str, b="high"), dict(n="Defense Index", ic="bolt", v=idx, f=str, b="high"),
               dict(n="TD Involved", ic="trophy", v=td_inv, f=str, b="high"), dict(n="Primary Role", ic="star", v=roles, f=str, b="text")]
    ord_y = sorted(R, key=lambda i: -tot_y[i]); ty_max, ty_t, _ = nice(max(tot_y), 4)
    stk_y = [(i, [(yds[i], NAVY), (ryd[i], BLUE), (rsy[i], GREEN)], f"{tot_y[i]:,}") for i in ord_y]
    ord_t = sorted(R, key=lambda i: -td_inv[i]); tt_max, tt_t, _ = nice(max(td_inv), 4)
    stk_t = [(i, [(tds[i], NAVY), (rtd[i], BLUE), (rstd[i], GREEN), (dtd[i], AMBER)], td_inv[i]) for i in ord_t]
    sc_pie = [sum(tds), sum(rstd), sum(dtd)]; pie_tot = sum(sc_pie) or 1
    pie_leg = "".join(f'<div><i style="background:{c}"></i><b>{v/pie_tot*100:.1f}%</b>{l} ({v})</div>' for v, c, l in zip(sc_pie, [NAVY, GREEN, AMBER], ["Pass → catch", "Rushing", "Defensive"]))
    vl = max(R, key=lambda i: (td_inv[i], tot_y[i], -i)); yl = arg(tot_y)
    phases = [("passing", yds[yl]), ("receiving", ryd[yl]), ("rushing", rsy[yl])]; ph = max(phases, key=lambda t: t[1])
    pages.append(f'''<div class="page big">{header("ALL-PURPOSE PRODUCTION", "OFFENSE &amp; DEFENSE")}
{hero(PL[vl], "MOST VERSATILE PLAYER", td_inv[vl], "TD INVOLVEMENTS", [(f"{tot_y[vl]}", "Total yds"), (rtd[vl], "Rec TD"), (dint[vl], "INT"), (pbu[vl], "Pass breakups")])}
{heat2(ap_cols, fs=19, pad=7)}
{panel("Individual Yards by Phase", "bars", stacked_h(950, 232, stk_y, ty_max, ty_t, [("Passing", NAVY), ("Receiving", BLUE), ("Rushing", GREEN)]), style="margin-top:16px")}
<div class="row2" style="margin-top:16px">
{panel("Touchdown Involvement", "trophy", stacked_h(458, 244, stk_t, tt_max, tt_t, [("Pass", NAVY), ("Receive", BLUE), ("Rush", GREEN), ("Defense", AMBER)]), style="flex:1")}
{panel("How the Team Scores", "target", f'<div style="display:flex;align-items:center;gap:14px;padding:8px 10px">{donut_custom(190, sc_pie, [NAVY, GREEN, AMBER], sum(sc_pie), "team TDs")}<div class="legend">{pie_leg}</div></div><div class="cap">A passing TD and the matching receiving TD are the same score, so it counts once for the team.</div>', style="flex:1")}
</div>
{bottom_row([f"{nmf(vl)} is the most involved player: {td_inv[vl]} TD involvements ({tds[vl]} pass, {rtd[vl]} receiving, {rstd[vl]} rushing, {dtd[vl]} defensive) and {tot_y[vl]} yards.",
  f"{nmf(yl)} leads individual yards ({tot_y[yl]:,}), mostly {ph[0]} ({div(ph[1], tot_y[yl])*100:.0f}%)." if tot_y[yl] else "No yardage has been recorded yet.",
  f"The team scored {sum(sc_pie)} TDs: {sc_pie[0]} passing, {sc_pie[1]} rushing and {sc_pie[2]} defensive."])}
{foot(6)}</div>''')

    # =============== PAGE 7: COMPARISON ===============
    sk = ["Speed", "Jump", "Passing", "Receiving", "Rushing", "Defense"]; sk_s = ["Speed", "Jump", "Pass", "Rec", "Rush", "Def"]
    scores = [[sc_sp[i], sc_jm[i], yds[i] / mx(yds) * 100, ryd[i] / mx(ryd) * 100, rsy[i] / mx(rsy) * 100, idx[i] / mx(idx) * 100] for i in R]
    overall = [sum(s_) / 6 for s_ in scores]
    rcards = ""
    for i, p in enumerate(PL):
        peak = max(range(6), key=lambda k: scores[i][k])
        rcards += (f'<div style="flex:1;text-align:center"><div style="background:{p["c"]};color:#fff;font-weight:800;font-style:italic;font-size:15px;padding:5px 0;border-radius:8px">{nmf(i)}</div>'
                   f'{radar_n(184, 176, 52, sk_s, [(p["c"], scores[i])], font=11.5, dots=2.6, fill=0.22)}'
                   f'<div style="font-size:13px;font-weight:700;color:{p["c"]}">Peak: {sk[peak]}</div></div>')
    cmp_cols = [dict(n=sk[k], ic=ic, v=[scores[i][k] for i in R], f=lambda v: f"{v:.0f}", b="high") for k, ic in enumerate(["clock", "run", "ball", "target", "bolt", "bal"])]
    cmp_cols.append(dict(n="Overall", ic="star", v=overall, f=lambda v: f"{v:.1f}", b="high"))
    leaders = [("FASTEST 40", PL[fast], f"{min(dash):.2f} s"), ("VERTICAL", PL[jump], f"{max(vj)} cm"), ("PASSING", PL[arg(yds)], f"{max(yds)} yds"),
               ("RECEIVING", PL[arg(ryd)], f"{max(ryd)} yds"), ("RUSHING", PL[arg(rsy)], f"{max(rsy)} yds"), ("DEFENSE", PL[arg(idx)], f"index {max(idx)}")]
    lead_html = '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:8px;padding:10px 8px 8px">'
    for lab, p, val in leaders:
        lead_html += (f'<div style="border:2px solid {p["c"]};border-radius:10px;text-align:center;overflow:hidden;background:{p["tint"]}">'
                      f'<div style="background:{p["c"]};color:#fff;font-size:12.5px;font-weight:800;letter-spacing:1px;padding:5px 0">{lab}</div>'
                      f'<div style="font-size:15px;font-weight:800;padding:8px 2px 0;color:{NAVY}">{p["n1"]}<br>{p["n2"] or "&nbsp;"}</div>'
                      f'<div style="font-size:22px;font-weight:900;padding:2px 0 8px;color:{p["c"]}">{val}</div></div>')
    lead_html += '</div>'
    bw_rows = ""
    for i in sorted(R, key=lambda i: -overall[i]):
        b = max(range(6), key=lambda k: scores[i][k]); wk = min(range(6), key=lambda k: scores[i][k])
        bw_rows += (f'<tr><td style="padding:7px 10px;font-weight:700;text-align:left"><i style="display:inline-block;width:11px;height:11px;border-radius:50%;background:{PL[i]["c"]};margin-right:8px"></i>{nmf(i)}</td>'
                    f'<td style="color:{GREEN};font-weight:800;font-size:16px">{sk[b]}</td><td style="color:#d9091f;font-weight:800;font-size:16px">{sk[wk]}</td></tr>')
    bw_tbl = f'<div class="tbl" style="margin:10px 8px 8px"><table><tr><th style="text-align:left;padding-left:10px">Player</th><th>Strongest</th><th>Weakest</th></tr>{bw_rows}</table></div>'
    top_o = arg(overall); top_sk = sorted(range(6), key=lambda k: -scores[top_o][k])[:2]
    pages.append(f'''<div class="page big">{header("PLAYER COMPARISON", "SCOUTING OVERVIEW")}
{panel("Skill Radar — Relative to Team Best (100 = best)", "target", '<div style="display:flex;gap:8px;padding:8px 6px 4px">' + rcards + '</div>', style="margin-top:16px")}
{heat2(cmp_cols, fs=21, pad=7)}
{panel("Category Leaders", "trophy", lead_html, style="margin-top:14px")}
<div class="row2" style="margin-top:14px">
{panel("Overall Index", "star", lollipop_n(458, 230, overall, 100, [0, 20, 40, 60, 80, 100], lambda i, v: f"{v:.1f}"), style="flex:1")}
{panel("Strongest vs Weakest Skill", "bolt", bw_tbl, style="flex:1")}
</div>
{bottom_row([f"{nmf(top_o)} has the best overall index ({overall[top_o]:.1f}), led by {sk[top_sk[0]].lower()} and {sk[top_sk[1]].lower()}.",
  f"Category leaders: passing {PL[arg(yds)]['n1']}, receiving {PL[arg(ryd)]['n1']}, rushing {PL[arg(rsy)]['n1']}, defense {PL[arg(idx)]['n1']}, speed {PL[fast]['n1']}, jump {PL[jump]['n1']}.",
  "Overall Index is an equal-weight average of six scores (100 = team best); compare within a position."])}
{foot(7)}</div>''')
    return pages
