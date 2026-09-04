
from datetime import datetime

from player.py import Player


class Game:
    def __init__(self, player1: Player, player2: Player, game_mode: str, winner: Player, description: str, timestamp: datetime):

        self.id_game = None

        if isinstance(winner, Player | None):
            self.winner = winner
        else:
            raise TypeError("The winner must be of type Player or None")

        if isinstance(player1, Player):
            self.player1 = player1
        else:
            raise TypeError("The player1 must be of type Player")

        if isinstance(player2, Player):
            self.player2 = player2
        else:
            raise TypeError("The player2 must be of type Player")

        if isinstance(game_mode, str):
            if (game_mode == "coinflip") or (game_mode == "dice"):
                self.game_mode = game_mode
            else:
                raise ValueError("The game must be coinflip or dice")
        else:
            raise TypeError("The game_mode must be of type str")

        if isinstance(description, str):
            self.description = description
        else:
            raise TypeError("The description must be of type str")

    def __str__(self):
        return f"{self.game_mode} between {self.player1} and {self.player2}. Winner : {self.winner}."
