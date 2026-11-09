from urllib.parse import urlparse
from config import ALLOWED_IMAGE_HOSTS, MAX_PLAYERS

def require_report(payload):
    if not isinstance(payload, dict): raise ValueError('Report payload must be an object.')
    team = payload.get('team') or {}
    players = payload.get('players') or []
    if not isinstance(team, dict) or not str(team.get('id', '')).strip(): raise ValueError('team.id is required.')
    if len(players) != MAX_PLAYERS: raise ValueError('Exactly five players are required.')
    for i, player in enumerate(players):
        if not isinstance(player, dict) or not str(player.get('id', '')).strip(): raise ValueError(f'players[{i}].id is required.')
        url = str(player.get('photoUrl') or '')
        if url and urlparse(url).hostname not in ALLOWED_IMAGE_HOSTS: raise ValueError('Only Hugging Face image URLs are allowed.')
    return team, players
