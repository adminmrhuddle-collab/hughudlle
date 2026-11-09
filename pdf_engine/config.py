from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGE_WIDTH = 1024
PAGE_HEIGHT = 1536
# A free-form 2:3 design canvas.  It deliberately does not use A4, so the
# report keeps the intended visual scale in phone PDF viewers.
REPORT_SCALE = 1.72
NAVY = '#14264f'
RED = '#d0021b'
INK = '#18253f'
LINE = '#cdd7e7'
PLAYER_COLORS = ['#d80d26', '#1f71d5', '#309a35', '#f57c0f', '#7023a4']
ALLOWED_IMAGE_HOSTS = ('huggingface.co', 'hf.co')
MAX_PLAYERS = 5
