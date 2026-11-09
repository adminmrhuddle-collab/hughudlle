from io import BytesIO
from urllib.parse import urlparse
import requests
from PIL import Image as PilImage
from config import ALLOWED_IMAGE_HOSTS

def player_photo(url):
    """Return a safely decoded portrait image, or None when it is unavailable."""
    if not url or urlparse(url).hostname not in ALLOWED_IMAGE_HOSTS: return None
    try:
        response = requests.get(url, timeout=12)
        response.raise_for_status()
        image = PilImage.open(BytesIO(response.content)).convert('RGB')
        image.thumbnail((480, 720))
        out = BytesIO(); image.save(out, format='JPEG', quality=88); out.seek(0)
        return out
    except (requests.RequestException, OSError):
        return None
