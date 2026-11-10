"""Downloads player photos / team logo and returns small base64 data URIs. Any failure returns None (placeholder is shown)."""
import base64, io
import requests
from PIL import Image, ImageOps

MAX_BYTES = 8 * 1024 * 1024


def fetch_data_uri(url, size=(360, 300)):
    if not url:
        return None
    try:
        r = requests.get(url, timeout=20, stream=True)
        r.raise_for_status()
        data = b""
        for chunk in r.iter_content(65536):
            data += chunk
            if len(data) > MAX_BYTES:
                return None
        im = Image.open(io.BytesIO(data))
        im = ImageOps.exif_transpose(im).convert("RGB")
        im = ImageOps.fit(im, size, method=Image.LANCZOS, centering=(0.5, 0.25))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=86)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception as e:  # noqa: BLE001 - a bad photo must never break the report
        print(f"[warn] could not load image {url}: {e}")
        return None


def fetch_logo_uri(url):
    if not url:
        return None
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        im = Image.open(io.BytesIO(r.content)).convert("RGBA")
        im.thumbnail((300, 300))
        buf = io.BytesIO()
        im.save(buf, "PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception as e:  # noqa: BLE001
        print(f"[warn] could not load logo {url}: {e}")
        return None
