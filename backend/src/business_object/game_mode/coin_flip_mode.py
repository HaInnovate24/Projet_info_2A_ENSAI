import secrets

from fastapi import HTTPException

from business_object.game import Game
from business_object.game_mode.game_mode import GameMode
from business_object.player import Player


class CoinFlipMode(GameMode):
    def play(self, p1: Player, p2: Player, choice="heads") -> Game:
        """Executes a single round of a coin-flip game between two players.
        Args:
            p1 (Player): the first player.
            p2 (Player):  the opponent.
            choice (str, optional): The player's choice ('heads' or 'tails'). Defaults to "heads".
        Returns:
            dict: A winner
        Raises:
            HTTPException: 400 if the two players are the same.
        """
        if p1.id_player == p2.id_player:
            raise HTTPException(status_code=400, detail="Two different players required")

        result = secrets.choice(["heads", "tails"])
        winner = p1 if result == choice else p2

        return winner
