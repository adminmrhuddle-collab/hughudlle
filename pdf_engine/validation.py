"""Request validation. Raises ValueError with a clear message for anything the report must not accept."""
from urllib.parse import urlparse

PHOTO_KEYS = ("photoUrl", "photoURL", "photo", "imageUrl", "imageURL", "profileImage", "profileImageUrl", "avatarUrl", "avatar")
ALLOWED_HOSTS = ("huggingface.co",)


def is_hf_url(url):
    try:
        u = urlparse(str(url))
    except Exception:
        return False
    return u.scheme == "https" and (u.hostname or "") in ALLOWED_HOSTS


def photo_url(player):
    for k in PHOTO_KEYS:
        if player.get(k):
            return player[k]
    return None


def validate(req):
    if not isinstance(req, dict):
        raise ValueError("Request must be a JSON object")
    team = req.get("team")
    if not isinstance(team, dict) or not team.get("id"):
        raise ValueError("team.id is required")
    players = req.get("players")
    if not isinstance(players, list) or len(players) != 5:
        raise ValueError("Exactly 5 players are required")
    seen = set()
    for i, p in enumerate(players):
        if not isinstance(p, dict) or not p.get("id"):
            raise ValueError(f"players[{i}].id is required")
        if p["id"] in seen:
            raise ValueError(f"Duplicate player id: {p['id']}")
        seen.add(p["id"])
        url = photo_url(p)
        if url and not is_hf_url(url):
            raise ValueError(f"players[{i}] photo URL must be an https huggingface.co link")
    logo = team.get("logoUrl")
    if logo and not is_hf_url(logo):
        raise ValueError("team.logoUrl must be an https huggingface.co link")
    return req
