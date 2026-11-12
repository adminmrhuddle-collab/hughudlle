"""Team statistics PDF report. Usage: python pdf_engine/team_main.py --input work/request.json --output work/report.pdf
Request: {"team": {...}, "stats": {...team totals...}, "matches": [...], "players": [...]}  (see CODEX_INSTRUCTIONS_TEAM_STATS.md)"""
import argparse, base64, html, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import components as C                        # noqa: E402
import main as M_                             # noqa: E402  (font_css, make_pdf, check_pdf)
from team_data import normalise               # noqa: E402
from team_pages import build_team_pages       # noqa: E402
from team_widgets import TCSS, CSS2, TPCSS    # noqa: E402
from validation import is_hf_url, photo_url   # noqa: E402
from images import fetch_data_uri, fetch_logo_uri  # noqa: E402


def validate_team(req):
    if not isinstance(req, dict):
        raise ValueError("Request must be a JSON object")
    team = req.get("team")
    if not isinstance(team, dict) or not team.get("id"):
        raise ValueError("team.id is required")
    if not (req.get("stats") or req.get("teamStats") or req.get("matches") or req.get("players")):
        raise ValueError("Provide at least one of: stats, matches, players")
    for u in (team.get("logoUrl"), team.get("bannerUrl")):
        if u and not is_hf_url(u):
            raise ValueError("team logo/banner URL must be an https huggingface.co link")
    for p in req.get("players") or []:
        u = photo_url(p) if isinstance(p, dict) else None
        if u and not is_hf_url(u):
            raise ValueError("player photo URL must be an https huggingface.co link")
    return req


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--keep-html", default=None)
    ap.add_argument("--banner-file", default=None, help="debug: local image used as the banner")
    a = ap.parse_args()
    req = validate_team(json.load(open(a.input, encoding="utf-8")))
    team = req["team"]
    T, M, P, notes = normalise(req)

    # photos only for the players who will be shown with a picture (top 5 by impact)
    by_id = {str(p.get("id")): p for p in req.get("players") or [] if isinstance(p, dict)}
    for p in sorted(P, key=lambda p: -p["impact"])[:5]:
        src = by_id.get(str(p["id"]))
        p["photo"] = fetch_data_uri(photo_url(src), size=(360, 450)) if src else None
    banner = None
    if a.banner_file:
        banner = "data:image/jpeg;base64," + base64.b64encode(open(a.banner_file, "rb").read()).decode()
    elif team.get("bannerUrl"):
        banner = fetch_data_uri(team["bannerUrl"], size=(980, 340))

    name = str(team.get("name") or "Team").strip()
    C.BRAND.update(name=html.escape(name.upper()[:34]), sub="FLAG FOOTBALL TEAM", initials=html.escape("".join(w[0] for w in name.split()[:2]).upper() or "T"),
                   logo=fetch_logo_uri(team.get("logoUrl")) or "")
    pages = build_team_pages(T, M, P, notes=notes, banner_uri=banner)
    total = len(pages)
    pages = [re.sub(r"Page \d+ / \d+", f"Page {i+1} / {total}", pg) for i, pg in enumerate(pages)]
    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{M_.font_css()}{C.CSS}{C.NEWCSS}{TCSS}{CSS2}{TPCSS}</style></head><body>{''.join(pages)}</body></html>"
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
