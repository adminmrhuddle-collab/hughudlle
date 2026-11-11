"""Single-player PDF report. Usage: python pdf_engine/player_main.py --input work/request.json --output work/report.pdf
Request shape: {"team": {"id","name","logoUrl?"}, "player": {...same fields as a team-report player..., "dob", "dominantHand", "level"}}"""
import argparse, base64, html, json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import components as C                      # noqa: E402
from player_pages import build_player_pages  # noqa: E402
from player_widgets import PCSS              # noqa: E402
from validation import is_hf_url, photo_url  # noqa: E402
from images import fetch_data_uri, fetch_logo_uri  # noqa: E402
import main as M                             # noqa: E402  (font_css, make_pdf)

EXPECTED_PAGES = 4


def validate_player(req):
    if not isinstance(req, dict):
        raise ValueError("Request must be a JSON object")
    team, p = req.get("team"), req.get("player")
    if not isinstance(team, dict) or not team.get("id"):
        raise ValueError("team.id is required")
    if not isinstance(p, dict) or not p.get("id"):
        raise ValueError("player.id is required")
    url = photo_url(p)
    if url and not is_hf_url(url):
        raise ValueError("player photo URL must be an https huggingface.co link")
    if team.get("logoUrl") and not is_hf_url(team["logoUrl"]):
        raise ValueError("team.logoUrl must be an https huggingface.co link")
    return req


def player_aliases(p):
    """Accept the common alternative key names used by the app."""
    alias = {"dob": ("dob", "dateOfBirth", "birthDate"), "dominantHand": ("dominantHand", "hand", "dmHand"),
             "level": ("level", "playerLevel", "pLevel"), "verticalJump": ("verticalJump", "jumpAbility", "jumpAb"), "dash40": ("dash40", "speed40", "spd40yd")}
    for k, names in alias.items():
        for n in names:
            if p.get(n) not in (None, ""):
                p[k] = p[n]
                break
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--keep-html", default=None)
    ap.add_argument("--photo-file", default=None, help="debug: use a local image instead of downloading the photo")
    a = ap.parse_args()
    req = validate_player(json.load(open(a.input, encoding="utf-8")))
    team, p = req["team"], player_aliases(req["player"])
    if a.photo_file:
        p["photo_data_uri"] = "data:image/jpeg;base64," + base64.b64encode(open(a.photo_file, "rb").read()).decode()
    else:
        p["photo_data_uri"] = fetch_data_uri(photo_url(p), size=(480, 600))
    name = str(team.get("name") or "Team").strip()
    C.BRAND.update(name=html.escape(name.upper()[:34]), sub="FLAG FOOTBALL TEAM", initials=html.escape("".join(w[0] for w in name.split()[:2]).upper() or "T"),
                   logo=fetch_logo_uri(team.get("logoUrl")) or "")
    pages = [pg.replace("/ 7</div>", f"/ {EXPECTED_PAGES}</div>") for pg in build_player_pages(p, team)]
    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{M.font_css()}{C.CSS}{C.NEWCSS}{PCSS}</style></head><body>{''.join(pages)}</body></html>"
    if a.keep_html:
        open(a.keep_html, "w", encoding="utf-8").write(doc)
    os.makedirs(os.path.dirname(os.path.abspath(a.output)), exist_ok=True)
    M.make_pdf(doc, os.path.abspath(a.output))
    M.EXPECTED_PAGES = EXPECTED_PAGES
    size = M.check_pdf(a.output)
    print(f"OK {EXPECTED_PAGES} pages {size[0]}x{size[1]} pt, {os.path.getsize(a.output)//1024} KB")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
