"""Derives comparable per-match metrics for two teams and decides the winner of every category.
Python 3.11 compatible. Missing data stays None and is never counted as a win."""
from team_data import normalise


def _mt(s):
    return f"{int(s)//60}:{int(s)%60:02d}"


f1 = lambda v: f"{v:.1f}"
f0 = lambda v: f"{v:.0f}"
pc = lambda v: f"{v:.0f}%"
sg = lambda v: f"{v:+.1f}"


def derive(req):
    T, M, P, notes = normalise(req)
    n = max(T["matches"], 1)
    d = lambda a, b: (a / b if b else None)
    S = dict(name=T["name"], city=T["city"], n=n, wins=T["wins"], losses=T["losses"], draws=T["draws"], T=T, M=M, P=P, notes=notes)
    S["win_pct"] = T["wins"] / n * 100
    S["ppg"] = T["pf"] / n; S["papg"] = T["pa"] / n; S["mpg"] = (T["pf"] - T["pa"]) / n
    S["pyth"] = T["pf"] ** 2 / (T["pf"] ** 2 + T["pa"] ** 2) * 100 if T["pf"] + T["pa"] else None
    has_y = bool(T["tot_yds"] or T["pass_yds"] or T["rush_yds"])
    S["ypg"] = T["tot_yds"] / n if has_y else None
    S["pass_ypg"] = T["pass_yds"] / n if has_y else None
    S["rush_ypg"] = T["rush_yds"] / n if has_y else None
    S["comp_pct"] = d(T["comp"], T["pass_att"]); S["comp_pct"] = S["comp_pct"] * 100 if S["comp_pct"] is not None else None
    S["otd_pg"] = T["off_td"] / n if (T["off_td"] or has_y) else None
    S["run_share"] = d(T["rush_yds"], T["rush_yds"] + T["pass_yds"]); S["run_share"] = S["run_share"] * 100 if S["run_share"] is not None else None
    S["rz"] = T["rz_scores"] / T["rz_trips"] * 100 if T["rz_trips"] else None
    S["third"] = T["third_conv"] / T["third_att"] * 100 if T["third_att"] else None
    S["top"] = (sum(m["top"] for m in M) / len(M)) if M and all(m["top"] for m in M) else None
    S["sacks_pg"] = T["sacks"] / n; S["int_pg"] = T["def_int"] / n; S["pbu_pg"] = T["pbu"] / n; S["flags_pg"] = T["flags"] / n
    S["dtd"] = T["def_td"]
    S["int_thrown_pg"] = T["int_thrown"] / n; S["sall_pg"] = T["sacks_allowed"] / n
    S["tom_pg"] = (T["def_int"] - T["int_thrown"]) / n
    S["plays_pg"] = (T["def_int"] + T["pbu"] + T["sacks"]) / n
    S["roster"] = len(P)
    S["impact_total"] = sum(p["impact"] for p in P)
    top3 = sorted(P, key=lambda p: -p["impact"])[:3]
    S["top3_share"] = sum(p["impact"] for p in top3) / S["impact_total"] * 100 if S["impact_total"] > 0 else None
    S["scorers"] = sum(1 for p in P if p["td"] > 0)
    return S


# key, label, unit/sub, direction (+1 higher is better, -1 lower is better, 0 no winner), formatter, group
METRICS = [
    ("win_pct", "Win rate", "% of matches", 1, pc, "results"),
    ("ppg", "Points scored", "per match", 1, f1, "results"),
    ("papg", "Points allowed", "per match", -1, f1, "results"),
    ("mpg", "Scoring margin", "per match", 1, sg, "results"),
    ("pyth", "Pythagorean win %", "from points for/against", 1, pc, "results"),
    ("ypg", "Total yards", "per match", 1, f0, "offense"),
    ("pass_ypg", "Passing yards", "per match", 1, f0, "offense"),
    ("rush_ypg", "Rushing yards", "per match", 1, f0, "offense"),
    ("comp_pct", "Completion %", "passes completed", 1, pc, "offense"),
    ("otd_pg", "Offensive TDs", "per match", 1, f1, "offense"),
    ("rz", "Red zone scoring", "trips ending in a score", 1, pc, "offense"),
    ("third", "Third-down conversion", "% converted", 1, pc, "offense"),
    ("run_share", "Run share", "rushing / (rushing + passing) yds", 0, pc, "style"),
    ("top", "Time of possession", "per match", 0, _mt, "style"),
    ("sacks_pg", "Sacks", "per match", 1, f1, "defense"),
    ("int_pg", "Interceptions", "per match", 1, f1, "defense"),
    ("pbu_pg", "Pass breakups", "per match", 1, f1, "defense"),
    ("flags_pg", "Flags pulled", "per match", 1, f1, "defense"),
    ("dtd", "Defensive TDs", "season total", 1, f0, "defense"),
    ("int_thrown_pg", "Interceptions thrown", "per match", -1, f1, "security"),
    ("sall_pg", "Sacks allowed", "per match", -1, f1, "security"),
    ("tom_pg", "Turnover margin", "takeaways - giveaways, per match", 1, sg, "security"),
]
MD = {m[0]: m for m in METRICS}


def winner(a, b, direction):
    """'A', 'B', 'T' (tie / too close) or None (not comparable)."""
    if a is None or b is None or direction == 0:
        return None
    hi = max(abs(a), abs(b))
    if hi == 0 or abs(a - b) / hi < 0.03:
        return "T"
    better_a = a > b if direction > 0 else a < b
    return "A" if better_a else "B"


def gap(a, b):
    hi = max(abs(a), abs(b), 1e-9)
    return abs(a - b) / hi


def compare_all(A, B):
    rows = []
    for key, label, sub, direction, fmt, group in METRICS:
        a, b = A.get(key), B.get(key)
        rows.append(dict(key=key, label=label, sub=sub, dir=direction, fmt=fmt, group=group, a=a, b=b,
                         fa=fmt(a) if a is not None else "n/a", fb=fmt(b) if b is not None else "n/a", win=winner(a, b, direction),
                         gap=gap(a, b) if a is not None and b is not None else 0))
    return rows


RADAR = [("Scoring", "ppg", 1), ("Defense", "papg", -1), ("Passing", "pass_ypg", 1), ("Rushing", "rush_ypg", 1),
         ("Defensive\nplays", "plays_pg", 1), ("Ball\nsecurity", "_giveaways", -1)]


def radar_scores(A, B):
    A = dict(A, _giveaways=A["int_thrown_pg"] + A["sall_pg"]); B = dict(B, _giveaways=B["int_thrown_pg"] + B["sall_pg"])
    ax, sa, sb = [], [], []
    for lab, key, dr in RADAR:
        a, b = A.get(key), B.get(key)
        if a is None or b is None:
            a = b = 0
        if dr > 0:
            hi = max(a, b); x, y = (a / hi * 100, b / hi * 100) if hi else (50, 50)
        else:
            lo = min(a, b)
            x = 100 if a == 0 else lo / a * 100; y = 100 if b == 0 else lo / b * 100
        ax.append(lab); sa.append(max(x, 4)); sb.append(max(y, 4))
    return ax, sa, sb


def normalise_pair(req):
    teams = req.get("teams")
    if not teams and req.get("teamA") and req.get("teamB"):
        teams = [req["teamA"], req["teamB"]]
    return teams
