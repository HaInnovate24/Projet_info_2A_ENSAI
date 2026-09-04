import secrets

from business_object.game import Game
from business_object.game_mode.game_mode import GameMode
from business_object.player import Player


class DiceMode(GameMode):
    def play(self, p1: Player, p2: Player) -> Game:
        d1 = secrets.choice(range(1, 7))
        d2 = secrets.choice(range(1, 7))
        if d1 > d2:
            winner = p1
        elif d1 < d2:
            winner = p2
        else:
            winner = None

        return winner
