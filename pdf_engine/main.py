"""Team PDF report engine.  Usage: python pdf_engine/main.py --input work/request.json --output work/report.pdf"""
import argparse, html, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import components as C            # noqa: E402
from pages import build_pages     # noqa: E402
from validation import validate, photo_url   # noqa: E402
from images import fetch_data_uri, fetch_logo_uri  # noqa: E402

PAGE_W, PAGE_H = 1024, 1536
EXPECTED_PAGES = 7


def font_css():
    faces = []
    for weight, name in [(400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold"), (800, "ExtraBold"), (900, "Black")]:
        for style, suffix in (("normal", ""), ("italic", "Italic")):
            f = HERE / "fonts" / (f"Inter-{name}{suffix}.otf" if not (name == "Regular" and suffix) else "Inter-Italic.otf")
            if f.exists():
                faces.append(f"@font-face{{font-family:'Inter';font-weight:{weight};font-style:{style};src:url('{f.as_uri()}')}}")
    return "".join(faces)


def find_chrome():
    for c in (os.environ.get("CHROME_BIN"), "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        if c and shutil.which(c):
            return shutil.which(c)
    raise RuntimeError("Chrome/Chromium was not found on this machine")


def make_pdf(html_text, out_path):
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "report.html"
        src.write_text(html_text, encoding="utf-8")
        cmd = [find_chrome(), "--headless", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage", "--no-pdf-header-footer",
               f"--print-to-pdf={out_path}", src.as_uri()]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if r.returncode != 0:
            raise RuntimeError(f"Chrome failed: {r.stderr[-500:]}")


def check_pdf(path):
    from pypdf import PdfReader
    if not os.path.exists(path) or os.path.getsize(path) < 50_000:
        raise RuntimeError("Generated PDF is missing or abnormally small")
    rd = PdfReader(path)
    if len(rd.pages) != EXPECTED_PAGES:
        raise RuntimeError(f"Expected {EXPECTED_PAGES} pages, got {len(rd.pages)}")
    sizes = {(round(float(p.mediabox.width)), round(float(p.mediabox.height))) for p in rd.pages}
    if len(sizes) != 1:
        raise RuntimeError(f"Pages have different sizes: {sizes}")
    return sizes.pop()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--keep-html", default=None, help="optional path to also save the intermediate HTML (debugging)")
    a = ap.parse_args()

    req = validate(json.load(open(a.input, encoding="utf-8")))
    team = req["team"]; players = req["players"]
    for p in players:
        p["photo_data_uri"] = fetch_data_uri(photo_url(p))
    name = str(team.get("name") or "Team").strip()
    initials = "".join(w[0] for w in name.split()[:2]).upper() or "T"
    C.BRAND.update(name=html.escape(name.upper()[:34]), sub="FLAG FOOTBALL TEAM", initials=html.escape(initials), logo=fetch_logo_uri(team.get("logoUrl")) or "")

    pages = build_pages(players, team)
    doc = (f"<!doctype html><html><head><meta charset='utf-8'><style>{font_css()}{C.CSS}{C.NEWCSS}</style></head><body>{''.join(pages)}</body></html>")
    if a.keep_html:
        open(a.keep_html, "w", encoding="utf-8").write(doc)
    os.makedirs(os.path.dirname(os.path.abspath(a.output)), exist_ok=True)
    make_pdf(doc, os.path.abspath(a.output))
    size = check_pdf(a.output)
    print(f"OK {EXPECTED_PAGES} pages {size[0]}x{size[1]} pt, {os.path.getsize(a.output)//1024} KB")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
