"""Single-player report: builds 4 pages (HTML strings). Every number and sentence is computed from the player's data."""
import math, re
from datetime import date, datetime
from components import *
from player_widgets import tile, grid, ring, band_gauge, hbars, split_bar, meter

# Reference targets used ONLY to scale charts (editable). Documented on the last page.
REF = dict(pass_yds=600, rec_yds=300, rush_yds=400, def_idx=40, ypc=(3, 5, 8), ypr=(8, 12, 20), ypa=(5, 8, 12), comp=(40, 60, 100), dash=(4.4, 5.4), vj=80)
GRN, ORG, YEL, REDC = "#3a9a2c", "#f57c10", "#f2b705", "#d0021b"
nz = lambda v: v not in (None, "", 0, 0.0, "0")


def num(v, d=0):
    try:
        f = float(v)
        return int(f) if f == int(f) else f
    except (TypeError, ValueError):
        return d


def parse_dob(s):
    s = str(s or "").strip()[:10]
    for f in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, f).date()
        except ValueError:
            pass
    return None


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;")


def build_player_pages(p, team, today=None):
    today = today or date.today()
    st = p.get("stats") or {}
    S = lambda k: num(st.get(k))
    name = esc(str(p.get("name") or "Player").strip().title())
    first = name.split()[0] if name.split() else name
    number = esc(p.get("number") or ""); pos = esc(str(p.get("position") or "").upper())
    team_name = esc(str(team.get("name") or "").strip().title())
    exp, hgt, wgt, vj = num(p.get("experience")), num(p.get("height")), num(p.get("weight")), num(p.get("verticalJump"))
    dash = num(p.get("dash40")); hand = str(p.get("dominantHand") or "").strip().title(); level = num(p.get("level"))
    dob = parse_dob(p.get("dob")); age = (today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))) if dob else None
    bmi = wgt / ((hgt / 100) ** 2) if hgt and wgt else None
    att, comp, pyd, ptd, pint = S("passingAttempts"), S("completions"), S("passingYards"), S("passingTDs"), S("interceptionsThrown")
    flags, dint, sacks, sall, pbu, dtd = S("flagsPulled"), S("defensiveInterceptions"), S("sacks"), S("sacksAllowed"), S("passBreakups"), S("defensiveTDs")
    rec, ryd, rtd, car, rsy, rstd = S("receptions"), S("receivingYards"), S("receivingTDs"), S("carries"), S("rushingYards"), S("rushingTDs")
    div = lambda a, b: a / b if b else 0
    comp_pct, ypa, ypr, ypc = div(comp, att) * 100, div(pyd, att), div(ryd, rec), div(rsy, car)
    scrim = pyd + ryd + rsy; td_all = ptd + rtd + rstd + dtd; touches = att + rec + car
    idx = flags + dint * 3 + sacks * 3 + pbu * 2 + dtd * 6; disr = dint + sacks + pbu
    off_pts = scrim / 10 + (ptd + rtd + rstd) * 6; def_pts = idx
    two_way = scrim >= 50 and idx >= 10
    fmt = lambda v: f"{v:,}"
    pl = lambda n, w, p=None: f"{n} {w if n == 1 else (p or w + 's')}"

    # ---------- DNA tags ----------
    tags = []
    def tag(t, sub, ic, c): tags.append((t, sub, ic, c))
    if dint >= 3: tag("Ball Hawk", f"{dint} interceptions", "ball", "#6a1fa0")
    if sacks >= 3: tag("Pass Rusher", f"{sacks} sacks", "bolt", REDC)
    if pbu >= 4: tag("Coverage Specialist", f"{pbu} pass breakups", "bal", ORG)
    if car >= 2 and ypc >= 7: tag("Big-Play Runner", f"{ypc:.1f} yds per carry", "run", GRN)
    if car >= 15: tag("Workhorse", f"{car} carries", "run", GRN)
    if rec >= 2 and ypr >= 16: tag("Deep Threat", f"{ypr:.1f} yds per catch", "target", BLUE)
    if rec >= 6: tag("Reliable Target", f"{rec} receptions", "check", BLUE)
    if att >= 10 and comp_pct >= 60: tag("Accurate Passer", f"{comp_pct:.0f}% completions", "ball", NAVY)
    if td_all >= 3: tag("Scoring Threat", f"{td_all} touchdowns", "trophy", "#c98f00")
    if two_way: tag("Two-Way Player", "impact on both sides", "star", REDC)
    if dash and dash <= 4.6: tag("Speedster", f"{dash:.2f} s in the 40", "clock", "#0b7a8a")
    if vj >= 60: tag("Explosive Jumper", f"{vj} cm vertical", "dumb", "#0b7a8a")
    if not tags: tag("Developing Profile", "more games will define the profile", "star", "#607d8b")
    tags = tags[:8]

    # ---------- shared page bits ----------
    def sec(t): return f'<div class="sec"><i></i>{t}</div>'
    pages = []

    # =============== PAGE 1: PROFILE ===============
    photo = (f'<img src="{p["photo_data_uri"]}" style="width:100%;height:100%;object-fit:cover;object-position:50% 20%">' if p.get("photo_data_uri") else silhouette())
    ident = [("AGE", f"{age} yrs" if age else "n/a"), ("HEIGHT", f"{hgt} cm" if hgt else "n/a"), ("WEIGHT", f"{wgt} kg" if wgt else "n/a"), ("BMI", f"{bmi:.1f}" if bmi else "n/a"),
             ("EXPERIENCE", f"{exp} yrs" if exp else "n/a"), ("DOMINANT HAND", hand or "n/a"), ("40 YD DASH", f"{dash:.2f} s" if dash else "not tested"), ("VERTICAL", f"{vj} cm" if vj else "not tested")]
    idg = "".join(f"<div><small>{k}</small><b>{v}</b></div>" for k, v in ident)
    nsize = 50 if len(name) <= 18 else max(30, int(50 * 18 / len(name)))
    hero = (f'<div class="phero"><div class="yl"></div><div class="jn">#{number}</div><div class="ph">{photo}</div>'
            f'<div class="tx"><div class="kick">PLAYER SCOUTING REPORT</div><div class="nm" style="font-size:{nsize}px">{name}</div>'
            f'<div class="sub"><span class="pill">#{number} • {pos}</span><span class="pill2">{team_name}</span><span class="pill2">ID {esc(p.get("id") or "")}</span></div></div>'
            f'<div class="idg">{idg}</div></div>')
    kp = grid([(fmt(scrim), "Scrimmage Yards", "pass + rec + rush", NAVY, "bars"), (td_all, "Touchdowns", f"{ptd+rtd+rstd} off • {dtd} def", REDC, "trophy"),
               (touches, "Offensive Touches", f"{att} att • {rec} rec • {car} car", BLUE, "run"), (idx, "Defensive Impact", f"{disr} disruptive plays", "#6a1fa0", "bolt")], cols=4)
    dna_html = '<div class="dna">' + "".join(
        f'<div class="tag" style="border-color:{c}"><div class="ti" style="background:{c}">{icon(ic, "#fff", 18)}</div><div><b>{t}</b><small>{s}</small></div></div>' for t, s, ic, c in tags) + '</div>'
    # skill radar (scaled to reference targets)
    ath = []
    if dash: ath.append(max(0, min(100, (REF["dash"][1] - dash) / (REF["dash"][1] - REF["dash"][0]) * 100)))
    if vj: ath.append(max(0, min(100, vj / REF["vj"] * 100)))
    sc = [min(100, pyd / REF["pass_yds"] * 100), min(100, ryd / REF["rec_yds"] * 100), min(100, rsy / REF["rush_yds"] * 100), min(100, idx / REF["def_idx"] * 100), sum(ath) / len(ath) if ath else 0]
    ax = ["Passing", "Receiving", "Rushing", "Defense", "Athleticism"]
    tall = len(tags) <= 4
    rad = radar_n(400, 300 if tall else 250, 102 if tall else 86, ax, [(REDC, sc)], font=15, dots=4.2, fill=0.18)
    rad_leg = "".join(f'<div style="display:flex;justify-content:space-between;gap:14px;font-size:14.5px;font-weight:700;margin:6px 0"><span style="color:#4b5468;font-weight:600">{a}</span><span>{v:.0f}</span></div>' for a, v in zip(ax, sc))
    # athletic gauges
    gh = 190 if tall else 166
    g1 = band_gauge(250, gh, REF["dash"][1] - dash if dash else 0, REF["dash"][1] - 4.0, [(0.4, REDC), (0.9, YEL), (1.4, GRN)], GRN, f"{dash:.2f}s" if dash else "n/a", "40-yard dash", "lower is better" if dash else "not tested yet", na=not dash)
    g2 = band_gauge(250, gh, vj, 80, [(40, REDC), (60, YEL), (80, GRN)], BLUE, f"{vj} cm" if vj else "n/a", "Vertical jump", "reference zones" if vj else "not tested yet", na=not vj)
    ins1 = []
    lead = max([("passing", pyd), ("receiving", ryd), ("rushing", rsy)], key=lambda t: t[1])
    ins1.append(f"{first} has produced {fmt(scrim)} scrimmage yards, mostly {lead[0]} ({div(lead[1], scrim)*100:.0f}%)." if scrim else f"{first} has no offensive yardage recorded yet; the value so far comes from defense." if idx else f"No production has been recorded for {first} yet.")
    ins1.append(f"On defense: {pl(dint, 'interception')}, {pl(sacks, 'sack')}, {pl(pbu, 'pass breakup')} and {pl(flags, 'flag')} pulled (impact index {idx})." if idx else "No defensive production recorded yet.")
    ins1.append(f"Profile: {hgt} cm, {wgt} kg (BMI {bmi:.1f})" + (f", {age} years old" if age else "") + (f", {hand.lower()}-handed." if hand else ".") if hgt and wgt else "Add height and weight to complete the physical profile.")
    pages.append(f'''<div class="page big">{header("PLAYER PROFILE", "SCOUTING REPORT")}
{hero}
{kp}
{panel("Player DNA — what the numbers say about this player", "star", dna_html, style="margin-top:14px")}
<div class="row2" style="margin-top:14px">
{panel("Skill Profile (scaled to reference targets)", "target", '<div style="display:flex;align-items:center;gap:6px;padding:4px 10px 0"><div>' + rad + '</div><div style="flex:1;padding-right:8px">' + rad_leg + '</div></div>', style="flex:1.45")}
{panel("Athletic Testing", "clock", '<div style="display:flex;flex-direction:column;align-items:center;padding:2px 0 4px">' + g1 + g2 + '</div>', style="flex:1")}
</div>
{bottom_row(ins1)}
{foot(1)}</div>''')

    # =============== PAGE 2: OFFENSE ===============
    ph_rows = [("Passing", pyd, NAVY), ("Receiving", ryd, BLUE), ("Rushing", rsy, GREEN)]
    def phase_card(title, ic, color, rows):
        body = "".join(f'<div style="display:flex;justify-content:space-between;padding:7px 4px;border-bottom:1px solid #eef0f4;font-size:16px"><span style="color:#4b5468;font-weight:600">{a}</span><b style="font-size:20px;color:#14264f">{b}</b></div>' for a, b in rows)
        return panel(title, ic, f'<div style="padding:4px 10px 6px">{body}</div>', style="flex:1")
    cards = ('<div class="row2" style="margin-top:14px">' +
             phase_card("Passing", "ball", NAVY, [("Attempts", att), ("Completions", comp), ("Completion %", f"{comp_pct:.0f}%" if att else "n/a"), ("Yards", fmt(pyd)), ("TD / INT", f"{ptd} / {pint}")]) +
             phase_card("Receiving", "target", BLUE, [("Receptions", rec), ("Yards", fmt(ryd)), ("Touchdowns", rtd), ("Yds / reception", f"{ypr:.1f}" if rec else "n/a"), ("Share of yards", f"{div(ryd, scrim)*100:.0f}%" if scrim else "n/a")]) +
             phase_card("Rushing", "run", GREEN, [("Carries", car), ("Yards", fmt(rsy)), ("Touchdowns", rstd), ("Yds / carry", f"{ypc:.1f}" if car else "n/a"), ("Share of yards", f"{div(rsy, scrim)*100:.0f}%" if scrim else "n/a")]) + '</div>')
    yards_bar = split_bar(920, [(pyd, NAVY, "Passing"), (ryd, BLUE, "Receiving"), (rsy, GREEN, "Rushing")])
    td_parts = [(ptd, NAVY, "Passing"), (rtd, BLUE, "Receiving"), (rstd, GREEN, "Rushing"), (dtd, AMBER, "Defensive")]
    td_don = donut_custom(190, [v for v, _, _ in td_parts], [c for _, c, _ in td_parts], td_all, "touchdowns") if td_all else ring(190, 0, "#e7e9ee", "0", "touchdowns")
    td_leg = "".join(f'<div><i style="background:{c}"></i><b>{v}</b>{l}</div>' for v, c, l in td_parts)
    gauges = ('<div style="display:grid;grid-template-columns:repeat(4,1fr);padding:2px 0 6px">' +
              band_gauge(236, 178, ypc, 10, [(REF["ypc"][0], REDC), (REF["ypc"][1], YEL), (10, GRN)], GREEN, f"{ypc:.1f}" if car else "n/a", "Yds / carry", pl(car, "carry", "carries"), na=not car) +
              band_gauge(236, 178, ypr, 25, [(REF["ypr"][0], REDC), (REF["ypr"][1], YEL), (25, GRN)], BLUE, f"{ypr:.1f}" if rec else "n/a", "Yds / reception", pl(rec, "reception"), na=not rec) +
              band_gauge(236, 178, comp_pct, 100, [(REF["comp"][0], REDC), (REF["comp"][1], YEL), (100, GRN)], NAVY, f"{comp_pct:.0f}%" if att else "n/a", "Completion %", pl(att, "attempt"), na=not att) +
              band_gauge(236, 178, ypa, 15, [(REF["ypa"][0], REDC), (REF["ypa"][1], YEL), (15, GRN)], NAVY, f"{ypa:.1f}" if att else "n/a", "Yds / attempt", "passing", na=not att) + '</div>')
    rate = lambda a, b: f"{div(a, b)*100:.0f}%" if b else "n/a"
    tdr = hbars(920, [("TD per carry", rate(rstd, car), div(rstd, car), GREEN), ("TD per reception", rate(rtd, rec), div(rtd, rec), BLUE), ("TD per pass attempt", rate(ptd, att), div(ptd, att) * 4, NAVY),
                      ("Yards per touch", f"{div(scrim, touches):.1f}" if touches else "n/a", div(div(scrim, touches), 20), "#c98f00")], label_w=200, val_w=70, rh=38)
    ins2 = [f"{fmt(scrim)} scrimmage yards on {touches} touches ({div(scrim, touches):.1f} yards per touch)." if touches else "No offensive touches recorded yet.",
            (f"Best phase: {lead[0]} with {fmt(lead[1])} yards" + (f" at {ypc:.1f} per carry on {car} carries." if lead[0] == "rushing" and car else f" at {ypr:.1f} per catch on {rec} receptions." if lead[0] == "receiving" and rec else ".")) if scrim else "Efficiency charts appear as soon as yardage is recorded.",
            f"Scoring: {ptd+rtd+rstd} offensive TDs" + (f" ({rstd} rushing, {rtd} receiving, {ptd} passing)." if ptd + rtd + rstd else ".")]
    pages.append(f'''<div class="page big">{header("OFFENSIVE PRODUCTION", "PASS • CATCH • RUN")}
{grid([(fmt(scrim), "Scrimmage Yards", "total offense", NAVY, "bars"), (touches, "Touches", "att + rec + carries", BLUE, "run"), (ptd + rtd + rstd, "Offensive TDs", f"{rate(ptd+rtd+rstd, touches)} of touches", REDC, "trophy"), (f"{div(scrim, touches):.1f}" if touches else "n/a", "Yards / Touch", "efficiency", GREEN, "target")], cols=4, h=True)}
{cards}
{panel("Where the Yards Come From", "bars", '<div style="padding:10px 14px 4px">' + yards_bar + '</div>', style="margin-top:14px")}
{panel("Efficiency vs Reference Zones", "target", gauges + '<div class="cap">Red = developing, yellow = solid, green = strong, based on the editable reference scale on the last page. The needle marks this player.</div>', style="margin-top:14px")}
<div class="row2" style="margin-top:14px">
{panel("How the Touchdowns Are Scored", "trophy", f'<div style="display:flex;align-items:center;gap:14px;padding:8px 14px">{td_don}<div class="legend">{td_leg}</div></div>', style="flex:1")}
{panel("Scoring Efficiency", "check", '<div style="padding:8px 12px 2px">' + hbars(430, [("TD / carry", rate(rstd, car), div(rstd, car), GREEN), ("TD / reception", rate(rtd, rec), div(rtd, rec), BLUE), ("TD / pass att.", rate(ptd, att), div(ptd, att) * 4, NAVY)], label_w=130, val_w=60, rh=48) + '</div>', style="flex:1")}
</div>
{bottom_row(ins2)}
{foot(2)}</div>''')

    # =============== PAGE 3: DEFENSE ===============
    comps = [("Flags ×1", flags, FLD["flags"]), ("INT ×3", dint * 3, FLD["ints"]), ("Sacks ×3", sacks * 3, FLD["sacks"]), ("PBU ×2", pbu * 2, FLD["pbu"]), ("Def TD ×6", dtd * 6, FLD["td"])]
    idx_bar = split_bar(920, [(v, c, l) for l, v, c in comps], h=60)
    dis_parts = [(dint, PU_ := "#6a1fa0", "Interceptions"), (pbu, ORG, "Pass breakups"), (sacks, REDC, "Sacks")]
    dis_don = donut_custom(268, [v for v, _, _ in dis_parts], [c for _, c, _ in dis_parts], disr, "plays") if disr else ring(268, 0, "#e7e9ee", "0", "plays")
    dis_leg = "".join(f'<div><i style="background:{c}"></i><b>{v}</b>{l}</div>' for v, c, l in dis_parts)
    cov, pr = dint + pbu, sacks
    skills = hbars(920, [("Ball skills (INT + PBU)", f"{cov}", div(cov, 12), "#6a1fa0"), ("Pass rush (sacks)", f"{sacks}", div(sacks, 8), REDC), ("Tackling (flags pulled)", f"{flags}", div(flags, 20), "#607d8b"),
                         ("Defensive scores (TD)", f"{dtd}", div(dtd, 3), GRN)], label_w=240, val_w=60, rh=44)
    ret = (f"{pl(dint, 'interception')} = {dint*3} index points, the biggest block of the index ({div(dint*3, idx)*100:.0f}%)." if idx and dint*3 == max(v for _, v, _ in comps) and dint else
           f"Largest contribution: {max(comps, key=lambda c: c[1])[0].split(' ×')[0]} ({max(v for _, v, _ in comps)} index points)." if idx else "No defensive production recorded yet.")
    ins3 = [f"Defensive impact index {idx}: {pl(flags, 'flag')}, {dint} INT, {pl(sacks, 'sack')}, {pbu} PBU, {dtd} defensive TDs." if idx else "No defensive plays recorded yet.", ret,
            (f"Sacks allowed: {sall}. Pass protection is an area to review." if sall else "Zero sacks allowed: no negative plays in pass protection.")]
    pages.append(f'''<div class="page big">{header("DEFENSIVE PRODUCTION", "COVER • RUSH")}
{grid([(flags, "Flags Pulled", "tackle plays", "#607d8b", "target"), (dint, "Def. INT", f"{dint*3} index pts", "#6a1fa0", "ball"), (sacks, "Sacks", f"{sall} allowed", REDC, "bolt")], cols=3, h=True)}
{grid([(pbu, "Pass Breakups", f"{pbu*2} index pts", ORG, "bal"), (dtd, "Defensive TDs", f"{dtd*6} index pts", GRN, "trophy"), (idx, "Impact Index", "custom total", NAVY, "star")], cols=3, h=True)}
{panel("Impact Index — Where the Points Come From", "star", '<div style="padding:12px 14px 4px">' + idx_bar + '</div><div class="cap">Index = Flags×1 + Interceptions×3 + Sacks×3 + Pass Breakups×2 + Defensive TD×6. Each block is the points that stat adds.</div>', style="margin-top:14px")}
<div class="row2" style="margin-top:14px">
{panel("Anatomy of Disruption", "bolt", f'<div style="display:flex;align-items:center;gap:14px;padding:8px 14px">{dis_don}<div class="legend">{dis_leg}</div></div><div class="cap">Disruptive plays = interceptions + pass breakups + sacks.</div>', style="flex:1")}
{panel("Defensive Skill Mix", "target", '<div style="padding:10px 12px 2px">' + hbars(430, [("Ball skills", f"{cov}", div(cov, 12), "#6a1fa0"), ("Pass rush", f"{sacks}", div(sacks, 8), REDC), ("Tackling", f"{flags}", div(flags, 20), "#607d8b"), ("Scores", f"{dtd}", div(dtd, 3), GRN)], label_w=120, val_w=50, rh=70) + '</div><div class="cap">Bars are scaled to season reference targets (see last page).</div>', style="flex:1")}
</div>
{panel("Takeaway Value", "ball", '<div style="display:flex;gap:14px;padding:12px 14px">' +
   "".join(f'<div style="flex:1;border:2px solid {c};border-radius:12px;text-align:center;overflow:hidden;background:#fff"><div style="background:{c};color:#fff;font-weight:800;font-size:13px;letter-spacing:1.5px;padding:6px 0">{t}</div><div style="font-size:52px;font-weight:900;color:{c};padding:12px 0 2px">{v}</div><div style="font-size:13px;color:#5b6477;font-weight:600;padding-bottom:16px">{s}</div></div>'
           for t, v, s, c in [("TURNOVERS FORCED", dint, "interceptions", "#6a1fa0"), ("PASSES DEFENDED", dint + pbu, "INT + breakups", ORG), ("QB PRESSURE", sacks, "sacks", REDC), ("DEFENSIVE POINTS", dtd * 6, "from defensive TDs", GRN)]) + '</div>', style="margin-top:14px")}
{bottom_row(ins3)}
{foot(3)}</div>''')

    # =============== PAGE 4: EVALUATION ===============
    S_, D_ = [], []
    def good(t, d, ic="check", c=GRN): S_.append((t, d, ic, c))
    def dev(t, d, ic="warn", c=ORG): D_.append((t, d, ic, c))
    if dint >= 2: good("Takes the ball away", f"{dint} interceptions: the highest-value defensive play.", "ball", "#6a1fa0")
    if car >= 2 and ypc >= 6: good("Explosive on the ground", f"{ypc:.1f} yards per carry on {car} carries.", "run")
    if rec >= 1 and ypr >= 15: good("Stretches the field", f"{ypr:.1f} yards per reception.", "target", BLUE)
    if td_all >= 2: good("Finishes drives", f"{td_all} touchdowns across offense and defense.", "trophy", "#c98f00")
    if sacks >= 2: good("Disrupts the quarterback", f"{sacks} sacks recorded.", "bolt", REDC)
    if pbu >= 2: good("Breaks up passes", f"{pbu} pass breakups.", "bal", ORG)
    if att >= 10 and comp_pct >= 60: good("Accurate passing", f"{comp_pct:.0f}% completions on {att} attempts.", "ball", NAVY)
    if two_way: good("Impact on both sides", f"{fmt(scrim)} scrimmage yards and a {idx} defensive index.", "star", REDC)
    if att >= 10 and comp_pct < 50: dev("Passing accuracy", f"{comp_pct:.0f}% completions on {att} attempts.")
    if pint > 0 and att: dev("Ball security", f"{pint} interceptions thrown on {att} attempts.")
    if sall > 0: dev("Pass protection", f"{sall} sacks allowed.")
    if not dash: dev("Speed not measured", "Record the 40-yard dash to complete the athletic profile.", "clock")
    if not vj: dev("Jump not measured", "Record the vertical jump to complete the athletic profile.", "dumb")
    if touches and touches < 10: dev("Small offensive sample", f"Only {touches} touches so far; efficiency numbers will move a lot.", "bars")
    if idx == 0 and scrim == 0: dev("No production recorded", "Stats appear as soon as games are logged in the app.", "bars")
    if not S_: good("Profile still forming", "Not enough volume yet to name clear strengths.", "star", "#607d8b")
    if not D_: dev("No major gaps found", "Keep logging games to confirm the trends.", "check", GRN)
    S_, D_ = S_[:3], D_[:3]
    sl = lambda items: "".join(f'<div class="sl"><div class="si" style="background:{c}">{icon(ic, "#fff", 18)}</div><div><b>{t}</b><span>{d}</span></div></div>' for t, d, ic, c in items)
    # role / balance
    tot_imp = (off_pts + def_pts) or 1
    bal = ring(150, off_pts / tot_imp * 100 if (off_pts + def_pts) else 0, NAVY, f"{off_pts/tot_imp*100:.0f}%" if (off_pts + def_pts) else "n/a", "offense", track="#d0021b" if (off_pts + def_pts) else "#e7e9ee")
    if not (off_pts + def_pts): role = "Not enough data to define a role yet."
    elif two_way: role = "Two-way contributor: meaningful production on offense and defense."
    elif off_pts > def_pts: role = f"Offensive playmaker, mainly {lead[0]}."
    else: role = "Defensive playmaker: impact comes from taking the ball away and creating pressure."
    # completeness
    fields = [("Photo", bool(p.get("photo_data_uri"))), ("Date of birth", dob is not None), ("Height", hgt > 0), ("Weight", wgt > 0), ("Dominant hand", bool(hand)), ("Experience", exp > 0), ("40-yard dash", dash > 0), ("Vertical jump", vj > 0)]
    comp_n = sum(1 for _, ok in fields if ok); comp_pct_prof = comp_n / len(fields) * 100
    miss = ", ".join(n for n, ok in fields if not ok) or "nothing"
    # confidence
    def lvl(n): return 0 if n < 5 else 1 if n < 15 else 2 if n < 30 else 3
    lab = ["very low", "low", "medium", "high"]
    conf = [("Rushing efficiency", car, "carries"), ("Receiving efficiency", rec, "receptions"), ("Passing accuracy", att, "attempts"), ("Defensive index", flags + dint + sacks + pbu, "defensive plays")]
    conf_html = "".join(f'<div style="display:grid;grid-template-columns:210px 1fr 190px;align-items:center;gap:14px;padding:5px 14px"><b style="font-size:15.5px">{n}</b><div style="display:flex;gap:6px">{meter(lvl(v))}</div><span style="font-size:13.5px;color:#4b5468;font-weight:600">n = {v} {u if v != 1 else u.rstrip("s").replace("ie", "y") if u != "carries" else "carry"} · {lab[lvl(v)]}</span></div>' for n, v, u in conf)
    # audit
    checks = []
    def chk(t, ok, d): checks.append((t, ok, d))
    chk("Completions ≤ attempts", comp <= att, f"{comp} completions on {pl(att, 'attempt')}.")
    chk("Passing yards need attempts", not (pyd > 0 and att == 0), f"{pyd} yards on {pl(att, 'attempt')}." if pyd or att else "No passing data.")
    chk("Receiving yards need receptions", not (ryd > 0 and rec == 0), f"{ryd} yards on {pl(rec, 'reception')}." if ryd or rec else "No receiving data.")
    chk("Rushing yards need carries", not (rsy > 0 and car == 0), f"{rsy} yards on {pl(car, 'carry', 'carries')}." if rsy or car else "No rushing data.")
    chk("Yards per carry plausible", not (car and ypc > 15), f"{ypc:.1f} yards per carry." if car else "No carries.")
    chk("Yards per reception plausible", not (rec and ypr > 40), f"{ypr:.1f} yards per reception." if rec else "No receptions.")
    chk("Touchdowns match touches", not ((rstd and not car) or (rtd and not rec) or (ptd and not att)), f"{td_all} TD in total.")
    chk_html = "".join(f'<div class="chk"><div class="si" style="width:26px;height:26px;border-radius:50%;background:{GRN if ok else ORG};display:flex;align-items:center;justify-content:center">{icon("check" if ok else "warn", "#fff", 15)}</div><b>{t}</b><span>{d}</span><div class="st {"ok" if ok else "rv"}">{"CONSISTENT" if ok else "REVIEW"}</div></div>' for t, ok, d in checks)
    n_rev = sum(1 for _, ok, _ in checks if not ok)
    glo = [("Scrimmage yards", "passing + receiving + rushing yards."), ("Touches", "pass attempts + receptions + carries."), ("Yards / touch", "scrimmage yards ÷ touches."),
           ("Impact index", "Flags×1 + INT×3 + Sacks×3 + PBU×2 + Def TD×6."), ("Disruptive plays", "interceptions + pass breakups + sacks."), ("BMI", "weight (kg) ÷ height (m)²."),
           ("Skill profile", f"stat ÷ target: passing {REF['pass_yds']} yds, receiving {REF['rec_yds']}, rushing {REF['rush_yds']}, defense index {REF['def_idx']}; athleticism from 40-yd and vertical."),
           ("Reference zones", f"yds/carry {REF['ypc'][0]}/{REF['ypc'][1]}, yds/rec {REF['ypr'][0]}/{REF['ypr'][1]}, comp % {REF['comp'][0]}/{REF['comp'][1]}, yds/att {REF['ypa'][0]}/{REF['ypa'][1]} (red / yellow / green).")]
    glo_html = '<div class="glo">' + "".join(f"<div><b>{a}:</b> {b}</div>" for a, b in glo) + '</div>'
    pages.append(f'''<div class="page big">{header("SCOUTING EVALUATION", "STRENGTHS • DATA")}
<div class="row2" style="margin-top:16px">
{panel("Strengths", "trophy", sl(S_), style="flex:1")}
{panel("Development Areas", "target", sl(D_), style="flex:1")}
</div>
<div class="row2" style="margin-top:14px">
{panel("Role Balance", "bal", f'<div style="display:flex;align-items:center;gap:16px;padding:8px 14px">{bal}<div style="flex:1"><div style="font-size:17px;font-weight:800;line-height:1.25">{role}</div><div class="cap" style="padding-left:0;margin-top:8px">Offense = scrimmage yards ÷ 10 + 6 × offensive TDs ({off_pts:.0f} pts). Defense (red) = impact index ({def_pts} pts). Offense is navy.</div></div></div>', style="flex:1.2")}
{panel("Profile Completeness", "check", f'<div style="display:flex;align-items:center;gap:16px;padding:8px 14px">{ring(132, comp_pct_prof, GRN if comp_pct_prof >= 75 else ORG, f"{comp_n}/{len(fields)}", "fields")}<div style="flex:1;font-size:14.5px;line-height:1.35;color:#4b5468"><b style="color:#14264f">Missing:</b> {miss}.<br>A complete profile makes comparisons and scouting more reliable.</div></div>', style="flex:1")}
</div>
{panel("How Much Can Each Number Be Trusted? (sample size)", "bars", conf_html + '<div class="cap">Confidence = observations behind a rate: under 5 very low, under 15 low, under 30 medium, 30 or more high.</div>', style="margin-top:14px")}
{panel(f"Automatic Data Check — {len(checks)-n_rev} consistent, {n_rev} to review", "check", chk_html, style="margin-top:12px")}
{panel("How the Metrics Are Calculated", "bulb", glo_html, style="margin-top:14px")}
<div class="nbox" style="margin-top:12px;padding:8px 20px"><div class="nt2">{icon("note", NAVY, 22)}Coach Notes :</div><div class="nl" style="height:26px"></div><div class="nl" style="height:26px"></div></div>
{foot(4)}</div>''')
    return pages
