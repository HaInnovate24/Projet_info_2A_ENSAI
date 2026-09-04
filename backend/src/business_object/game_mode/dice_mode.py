
from abc import ABC


from game_mode.py import GameMode
from player.py import Player
from game.py import Game


class DiceMode(GameMode):

    def play(p1: Player, p2: Player) -> Game:
        d1 = secrets.choice(range(1, 7))
        d2 = secrets.choice(range(1, 7))
        if d1 > d2:
            winner = p1
        elif d1 < d2:
            winner = p2
        else:
            winner = None
