import unittest
from datetime import datetime
from unittest.mock import patch

from business_object.game import Game
from business_object.player import Player
from service.game_service import GameService


class TestFindAllByPlayer(unittest.TestCase):
    def setUp(self):
        # Joueurs de test
        self.maurice = Player(
            username="maurice",
            elo=1136,
            email="maurice@test.com",
            id_player=1,
        )

        self.miguel = Player(
            username="miguel",
            elo=1164,
            email="miguel@test.com",
            id_player=2,
        )

        self.alice = Player(
            username="alice",
            elo=1200,
            email="alice@test.com",
            id_player=3,
        )

        # Parties de test
        self.game1 = Game(
            player1=self.maurice,
            player2=self.miguel,
            game_mode="dice",
            winner=self.maurice,
            description="Rolls: maurice 4 vs 1 miguel",
            timestamp=datetime.now(),
            id_game=1,
        )

        self.game2 = Game(
            player1=self.maurice,
            player2=self.alice,
            game_mode="dice",
            winner=self.alice,
            description="Rolls: maurice 2 vs 5 alice",
            timestamp=datetime.now(),
            id_game=2,
        )

        self.game3 = Game(
            player1=self.miguel,
            player2=self.maurice,
            game_mode="classic",
            winner=self.miguel,
            description="Miguel wins",
            timestamp=datetime.now(),
            id_game=3,
        )

        self.game4 = Game(
            player1=self.maurice,
            player2=self.alice,
            game_mode="classic",
            winner=None,
            description="Draw",
            timestamp=datetime.now(),
            id_game=4,
        )

        self.service = GameService()

    @patch("service.game_service.GameDAO")
    def test_find_all_by_player_without_game_mode(self, mock_game_dao):
        """
        Sans game_mode :
        on doit appeler le DAO uniquement avec id_player.
        """

        mock_game_dao.return_value.find_all_by_player.return_value = [
            self.game1,
            self.game2,
            self.game3,
            self.game4,
        ]

        result = self.service.find_all_by_player(1)

        # Vérifie le résultat
        self.assertEqual(len(result), 4)

        # Vérifie que le DAO a été appelé sans game_mode
        mock_game_dao.return_value.find_all_by_player.assert_called_once_with(1)

    @patch("service.game_service.GameDAO")
    def test_find_all_by_player_with_dice(self, mock_game_dao):
        """
        Avec game_mode='dice' :
        on doit appeler le DAO avec id_player et game_mode.
        """

        mock_game_dao.return_value.find_all_by_player.return_value = [
            self.game1,
            self.game2,
        ]

        result = self.service.find_all_by_player(1, "dice")

        # Vérifie le résultat
        self.assertEqual(len(result), 2)

        # Vérifie que les deux jeux sont bien des jeux dice
        for game in result:
            self.assertEqual(game.game_mode, "dice")

        # Vérifie l'appel au DAO
        mock_game_dao.return_value.find_all_by_player.assert_called_once_with(
            1,
            "dice",
        )

    @patch("service.game_service.GameDAO")
    def test_find_all_by_player_with_classic(self, mock_game_dao):
        """
        Avec game_mode='classic' :
        on doit appeler le DAO avec id_player et game_mode.
        """

        mock_game_dao.return_value.find_all_by_player.return_value = [
            self.game3,
            self.game4,
        ]

        result = self.service.find_all_by_player(1, "classic")

        # Vérifie le résultat
        self.assertEqual(len(result), 2)

        # Vérifie que les jeux sont bien en mode classic
        for game in result:
            self.assertEqual(game.game_mode, "classic")

        # Vérifie l'appel au DAO
        mock_game_dao.return_value.find_all_by_player.assert_called_once_with(
            1,
            "classic",
        )

    @patch("service.game_service.GameDAO")
    def test_find_all_by_player_empty(self, mock_game_dao):
        """
        Si aucun jeu n'est trouvé, la méthode doit retourner une liste vide.
        """

        mock_game_dao.return_value.find_all_by_player.return_value = []

        result = self.service.find_all_by_player(1)

        self.assertEqual(result, [])

        mock_game_dao.return_value.find_all_by_player.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
