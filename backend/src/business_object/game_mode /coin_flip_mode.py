import secrets

from business_object.game_mode.game_mode import GameMode
from fastapi import HTTPException

from business_object.game import Game
from business_object.player import Player
from dao.player_dao import PlayerDao


class CoinFlipMode(GameMode):
    def play(self, p1: Player, p2: Player, choice="heads") -> Game:
        """Executes a single round of a coin-flip game between two players.
        Args:
            id_player (int): The unique identifier of the first player.
            id_opponent (int): The unique identifier of the opponent.
            choice (str, optional): The player's choice ('heads' or 'tails'). Defaults to "heads".
        Returns:
            dict: A dictionary containing the match details and new elo
        Raises:
            HTTPException: 400 if the two players are the same.
            HTTPException: 404 if one or both players are not found in the database.
        """
        if p1.id_player == p2.id_player:
            raise HTTPException(status_code=400, detail="Two different players required")

        if not p1 or not p2:
            raise HTTPException(status_code=404, detail="Player not found")

        result = secrets.choice(["heads", "tails"])
        winner = p1 if result == choice else p2

        self.update_player_ratings(p1, p2, winner)

        PlayerDao().update(p1)
        PlayerDao().update(p2)

        return winner
