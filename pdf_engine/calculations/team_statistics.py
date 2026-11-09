def n(value):
    try: return float(value or 0)
    except (ValueError, TypeError): return 0.0

def stat(player, name): return n((player.get('stats') or {}).get(name))
def total(players, name): return sum(stat(p, name) for p in players)
def average(players, name): return total(players, name) / len(players) if players else 0
def pct(a, b): return 0 if not b else round(a / b * 100, 1)
def overall(player):
    return stat(player,'passingYards') + stat(player,'receivingYards') + stat(player,'rushingYards') + stat(player,'flagsPulled')*5 + stat(player,'sacks')*8 + stat(player,'passBreakups')*4
