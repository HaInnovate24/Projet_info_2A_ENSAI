from business_object.player import Player


class Game:
    def __init__(
        self,
        player1: Player,
        player2: Player,
        game_mode,
        winner: Player | None,
        description: str | None,
        timestamp,
    ):
        self.id_game = None
        self.player1 = player1
        self.player2 = player2
        self.game_mode = game_mode
        self.winner = winner
        self.description = description
        self.timestamp = timestamp

    def __str__(self):
        if self.winner:
            return f"{self.game_mode} entre {self.player1.username} et {self.player2.username}. Gagnante: {self.winner.username} "
        else:
            return f"{self.game_mode} entre {self.player1.username} et {self.player2.username}. Pas encore de gagnante "
