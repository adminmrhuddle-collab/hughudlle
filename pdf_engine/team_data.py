"""Normalises the team-stats request into the dict T, the match list M and the player list P.
Missing team totals are derived from the players' stats when possible; anything that is not tracked stays None."""

def num(v, d=0):
    try:
        f = float(v)
        return int(f) if f == int(f) else f
    except (TypeError, ValueError):
        return d


def secs(v):
    """Accepts seconds, 'mm:ss' or 'hh:mm:ss' -> seconds (None if empty)."""
    if v in (None, "", 0, "0"):
        return None
    if isinstance(v, (int, float)):
        return int(v)
    parts = str(v).split(":")
    try:
        parts = [int(x) for x in parts]
    except ValueError:
        return None
    s = 0
    for x in parts:
        s = s * 60 + x
    return s or None


KEYS = {  # internal key -> accepted request keys
    "matches": ("matches", "matchesPlayed", "gamesPlayed"), "wins": ("wins",), "losses": ("losses",), "draws": ("draws",),
    "pf": ("pointsFor", "pf", "ptsFor"), "pa": ("pointsAgainst", "pa", "ptsAgainst"), "off_td": ("offensiveTDs", "offensiveTouchdowns", "offTD"),
    "def_int": ("defensiveInterceptions", "defInt", "interceptions"), "tot_yds": ("totalYards", "totalYds"), "pass_yds": ("passingYards", "passYds"),
    "rush_yds": ("rushingYards", "rushYds"), "pass_att": ("passAttempts", "passingAttempts"), "comp": ("completions", "passCompletions"),
    "pass_td": ("passingTDs", "passTD"), "rush_td": ("rushingTDs", "rushTD"), "def_td": ("defensiveTDs", "defTD"), "sacks": ("sacks",),
    "sacks_allowed": ("sacksAllowed",), "flags": ("flagsPulled", "flags"), "pbu": ("passBreakups", "pbu"), "int_thrown": ("interceptionsThrown", "intThrown"),
    "rz_trips": ("redZoneTrips",), "rz_scores": ("redZoneScores",), "third_att": ("thirdDownAttempts",), "third_conv": ("thirdDownConversions",),
}
PLAYER_SUM = {"pass_yds": "passingYards", "rush_yds": "rushingYards", "pass_att": "passingAttempts", "comp": "completions", "pass_td": "passingTDs", "rush_td": "rushingTDs",
              "def_td": "defensiveTDs", "sacks": "sacks", "sacks_allowed": "sacksAllowed", "flags": "flagsPulled", "pbu": "passBreakups", "def_int": "defensiveInterceptions",
              "int_thrown": "interceptionsThrown"}


def normalise(req):
    team = req.get("team") or {}
    raw = req.get("stats") or req.get("teamStats") or {}
    mraw = req.get("matches") or []
    players = [p for p in (req.get("players") or []) if isinstance(p, dict)]
    notes = []

    # ---------- matches
    M = []
    for i, m in enumerate(mraw):
        f = num(m.get("pointsFor", m.get("pf", m.get("scoreFor"))), None); a = num(m.get("pointsAgainst", m.get("pa", m.get("scoreAgainst"))), None)
        if f is None or a is None:
            continue
        M.append(dict(n=len(M) + 1, opp=str(m.get("opponent") or m.get("opponentName") or f"Opponent {len(M)+1}").strip(), f=f, a=a,
                      yds=num(m.get("totalYards", m.get("yards")), None), top=secs(m.get("timeOfPossession", m.get("top"))), date=str(m.get("date") or "")))

    # ---------- team totals
    T = {}
    for k, names in KEYS.items():
        v = None
        for nme in names:
            if raw.get(nme) not in (None, ""):
                v = num(raw[nme], None); break
        T[k] = v
    for k, pk in PLAYER_SUM.items():
        if T[k] is None and players:
            T[k] = sum(num((p.get("stats") or {}).get(pk)) for p in players)
            notes.append(k)
    if M:
        if T["matches"] is None: T["matches"] = len(M)
        if T["pf"] is None: T["pf"] = sum(m["f"] for m in M)
        if T["pa"] is None: T["pa"] = sum(m["a"] for m in M)
        if T["wins"] is None: T["wins"] = sum(1 for m in M if m["f"] > m["a"])
        if T["losses"] is None: T["losses"] = sum(1 for m in M if m["f"] < m["a"])
        if T["draws"] is None: T["draws"] = sum(1 for m in M if m["f"] == m["a"])
    if T["off_td"] is None and T["pass_td"] is not None:
        T["off_td"] = (T["pass_td"] or 0) + (T["rush_td"] or 0)
    if T["tot_yds"] is None and T["pass_yds"] is not None:
        T["tot_yds"] = (T["pass_yds"] or 0) + (T["rush_yds"] or 0)
    T["top_total"] = secs(raw.get("timeOfPossession", raw.get("totalTimeOfPossession")))
    for k in ("matches", "wins", "losses", "draws", "pf", "pa"):
        if T[k] is None: T[k] = 0
    for k in T:
        if T[k] is None and k not in ("rz_trips", "rz_scores", "third_att", "third_conv", "top_total"): T[k] = 0
    if not T["matches"]: T["matches"] = max(T["wins"] + T["losses"] + T["draws"], len(M))
    if M and not T["top_total"] and all(m["top"] for m in M):
        T["top_total"] = sum(m["top"] for m in M)
    T["name"] = str(team.get("name") or "Team").strip().title(); T["city"] = str(team.get("city") or "").strip(); T["founded"] = team.get("founded")

    # ---------- players
    P = []
    for p in players:
        st = p.get("stats") or {}
        g = lambda k: num(st.get(k))
        d = dict(id=p.get("id"), name=str(p.get("name") or "Player").strip().title(), number=str(p.get("number") or ""), photo=None, photo_url=None,
                 pyd=g("passingYards"), ptd=g("passingTDs"), att=g("passingAttempts"), comp=g("completions"), pint=g("interceptionsThrown"),
                 ryd=g("receivingYards"), rtd=g("receivingTDs"), rec=g("receptions"), rsy=g("rushingYards"), rstd=g("rushingTDs"), car=g("carries"),
                 flags=g("flagsPulled"), dint=g("defensiveInterceptions"), sacks=g("sacks"), sall=g("sacksAllowed"), pbu=g("passBreakups"), dtd=g("defensiveTDs"))
        d["scrim"] = d["pyd"] + d["ryd"] + d["rsy"]
        d["otd"] = d["ptd"] + d["rtd"] + d["rstd"]
        d["td"] = d["otd"] + d["dtd"]
        d["idx"] = d["flags"] + d["dint"] * 3 + d["sacks"] * 3 + d["pbu"] * 2 + d["dtd"] * 6
        d["impact"] = round(d["scrim"] / 10 + d["otd"] * 6 + d["idx"], 1)
        P.append(d)
    return T, M, P, notes
