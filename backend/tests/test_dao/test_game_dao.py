import os
from datetime import datetime
from unittest.mock import patch

import psycopg2
import pytest

from business_object.game import Game
from dao.game_dao import GameDAO
from dao.player_dao import PlayerDao
from utils.reset_database import ResetDatabase


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialize test data"""
    with patch.dict(os.environ, {"SCHEMA": "project_test_dao"}):
        ResetDatabase().run(test_dao=True)
        yield


def test_find_by_id_existing():
    """Find a game by an existing id"""

    # GIVEN
    id_game = 1

    # WHEN
    game = GameDAO().find_by_id(id_game)

    # THEN
    assert game is not None
    assert isinstance(game, Game)
    assert game.id_game == id_game


def test_find_by_id_non_existing():
    """Find a game by a non-existing id"""

    # GIVEN
    id_game = 9999999999999

    # WHEN
    game = GameDAO().find_by_id(id_game)

    # THEN
    assert game is None


def test_create_ok():
    """Successfully create a Game"""

    # GIVEN
    player1 = PlayerDao().find_by_id(998)
    player2 = PlayerDao().find_by_id(999)

    assert player1 is not None
    assert player2 is not None

    game = Game(
        player1=player1,
        player2=player2,
        game_mode="dice",
        winner=player1,
        description="Rolls: player1 5 vs player2 2",
        timestamp=datetime.now(),
    )

    # WHEN
    creation_ok = GameDAO().create(game)

    # THEN
    assert creation_ok
    assert game.id_game is not None


def test_create_ko():
    """Fail to create a Game with invalid data"""

    # GIVEN
    player1 = PlayerDao().find_by_id(998)
    player2 = PlayerDao().find_by_id(999)

    assert player1 is not None
    assert player2 is not None

    game = Game(
        player1=player1,
        player2=player2,
        game_mode=123,
        winner=player1,
        description="Invalid game",
        timestamp=datetime.now(),
    )

    # WHEN / THEN
    with pytest.raises(psycopg2.Error):
        GameDAO().create(game)


def test_find_all_by_player():
    """Find all games of a player"""

    # GIVEN
    id_player = 998

    # WHEN
    games = GameDAO().find_all_by_player(id_player)

    # THEN
    assert isinstance(games, list)

    for game in games:
        assert isinstance(game, Game)
        assert game.player1.id_player == id_player or game.player2.id_player == id_player


def test_find_all_by_player_with_game_mode():
    """Find all games of a player with a game mode filter"""

    # GIVEN
    id_player = 998
    game_mode = "dice"

    # WHEN
    games = GameDAO().find_all_by_player(id_player, game_mode)

    # THEN
    assert isinstance(games, list)

    for game in games:
        assert isinstance(game, Game)
        assert game.player1.id_player == id_player or game.player2.id_player == id_player
        assert game.game_mode == game_mode


def test_find_all_by_player_non_existing():
    """Find all games of a non-existing player"""

    # GIVEN
    id_player = 9999999999999

    # WHEN
    games = GameDAO().find_all_by_player(id_player)

    # THEN
    assert isinstance(games, list)
    assert len(games) == 0


def test_find_all_by_player_non_existing_game_mode():
    """Find all games with a non-existing game mode"""

    # GIVEN
    id_player = 998
    game_mode = "this_mode_does_not_exist"

    # WHEN
    games = GameDAO().find_all_by_player(id_player, game_mode)

    # THEN
    assert isinstance(games, list)
    assert len(games) == 0
