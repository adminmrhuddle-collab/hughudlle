"""Team-vs-team comparison PDF. Usage: python pdf_engine/compare_main.py --input work/request.json --output work/report.pdf
Request: {"teams": [ {team, stats, matches, players}, {team, stats, matches, players} ]}   (each entry has the team-stats report shape)"""
import argparse, html, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import components as C                        # noqa: E402
import main as M_                             # noqa: E402
from compare_data import derive, normalise_pair   # noqa: E402
from compare_pages import build_compare_pages, CMPCSS   # noqa: E402
from team_widgets import TCSS, CSS2, TPCSS    # noqa: E402
from team_main import validate_team           # noqa: E402
from validation import photo_url              # noqa: E402
from images import fetch_data_uri, fetch_logo_uri  # noqa: E402


def validate_pair(req):
    if not isinstance(req, dict):
        raise ValueError("Request must be a JSON object")
    teams = normalise_pair(req)
    if not isinstance(teams, list) or len(teams) != 2:
        raise ValueError("Provide exactly two teams in 'teams' (or teamA and teamB)")
    for t in teams:
        validate_team(t)
    if str(teams[0]["team"]["id"]) == str(teams[1]["team"]["id"]):
        raise ValueError("The two teams must be different (same team.id)")
    return teams


def prepare(t):
    S = derive(t)
    by_id = {str(p.get("id")): p for p in t.get("players") or [] if isinstance(p, dict)}
    for p in sorted(S["P"], key=lambda p: -p["impact"])[:3]:
        src = by_id.get(str(p["id"]))
        p["photo"] = fetch_data_uri(photo_url(src), size=(360, 450)) if src else None
    S["logo"] = fetch_logo_uri(t["team"].get("logoUrl"))
    return S


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--keep-html", default=None)
    a = ap.parse_args()
    req = json.load(open(a.input, encoding="utf-8"))
    teams = validate_pair(req)
    A, B = prepare(teams[0]), prepare(teams[1])
    C.BRAND.update(name="TEAM VS TEAM", sub="MATCHUP REPORT", initials="VS", logo="")
    pages = build_compare_pages(A, B, notes=())
    total = len(pages)
    pages = [re.sub(r"Page \d+ / \d+", f"Page {i+1} / {total}", pg) for i, pg in enumerate(pages)]
    doc = (f"<!doctype html><html><head><meta charset='utf-8'><style>{M_.font_css()}{C.CSS}{C.NEWCSS}{TCSS}{CSS2}{TPCSS}{CMPCSS}</style></head>"
           f"<body>{''.join(pages)}</body></html>")
    if a.keep_html:
        open(a.keep_html, "w", encoding="utf-8").write(doc)
    os.makedirs(os.path.dirname(os.path.abspath(a.output)), exist_ok=True)
    M_.make_pdf(doc, os.path.abspath(a.output))
    M_.EXPECTED_PAGES = total
    size = M_.check_pdf(a.output)
    print(f"OK {total} pages {size[0]}x{size[1]} pt, {os.path.getsize(a.output)//1024} KB")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
