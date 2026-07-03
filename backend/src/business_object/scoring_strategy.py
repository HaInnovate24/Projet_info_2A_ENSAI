import os


class ScoringStrategy:
    @classmethod
    def expected_score(cls, elo1, elo2):
        """Calculates the expected score (probability of winning) using the Elo formula.
        Args:
            elo1 (float): The current Elo rating of player 1.
            elo2 (float): The current Elo rating of player 2.

        Returns:
            float: The expected score for player 1 (between 0 and 1).
        """
        return 1 / (1 + 10 ** ((elo2 - elo1) / 400))

    @classmethod
    def compute_elo(cls, elo1, elo2, win1):
        """Computes the new Elo ratings for two players after a match.
        Args:
            elo1 (int): Current Elo of player 1.
            elo2 (int): Current Elo of player 2.
            win1 (bool): True if player 1 won, False if player 2 won.
        Returns:
            tuple[int, int]: A tuple containing (new_elo1, new_elo2).
        """
        K_FACTOR = int(os.environ["ELO_K_FACTOR"])

        s1, s2 = win1 * 1, 1 - win1 * 1

        new_elo1 = round(elo1 + K_FACTOR * (s1 - cls.expected_score(elo1, elo2)))
        new_elo2 = round(elo2 + K_FACTOR * (s2 - cls.expected_score(elo2, elo1)))

        return new_elo1, new_elo2

    @classmethod
    def compute(cls, game):
        """Calculates and persists the new Elo ratings for both players.
        No update if it is a Draw.
        Args:
            Game
        """
        if not game.winner:
            return

        player1 = game.player1
        player2 = game.player2

        player1.elo, player2.elo = cls.compute_elo(player1.elo, player2.elo, player1 == game.winner)
