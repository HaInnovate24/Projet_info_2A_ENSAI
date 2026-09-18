from business_object.game import Game
from dao.db_connection import DBConnection
from dao.player_dao import PlayerDao
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class GameDAO(metaclass=Singleton):
    @log
    def create(self, game: Game) -> bool:
        """ """
        res = None
        try:
            with DBConnection().connection as connexion:
                with connexion.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO game(id_player1,id_player2,game_mode,id_winner,detail,timestamp) VALUES"
                        "(%(id_player1)s,%(id_player2)s,%(game_mode)s,%(id_winner)s,%(detail)s,%(timestamp)s)"
                        "RETURNING id_game",
                        {
                            "id_player1": game.player1.id_player,
                            "id_player2": game.player2.id_player,
                            "game_mode": game.game_mode,
                            "detail": game.description,
                            "id_winner": game.winner.id_player,
                            "timestamp": game.timestamp,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            game.id_game = res["id_game"]
            created = True

        return created

    @log
    def find_by_id(self, id_game: int) -> Game:
        """ """
        res = None
        try:
            with DBConnection().connection as connexion:
                with connexion.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM game                       "
                        " WHERE id_game = %(id_game)s;   ",
                        {"id_game": id_game},
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logger.error(e)
            raise
        game = None
        if res:
            p1 = PlayerDao().find_by_id(res["id_player1"])
            p2 = PlayerDao().find_by_id(res["id_player2"])
            winner = PlayerDao().find_by_id(res["id_winner"])
            game = Game(
                player1=p1,
                player2=p2,
                game_mode=res["game_mode"],
                winner=winner,
                description=res["detail"],
                timestamp=res["timestamp"],
                id_game=res["id_game"],
            )
        return game

    @log
    def find_all_by_player(self, id_player: int, game_mode: str | None = None) -> list[Game]:
        """Return all games of a player, optionally filtered by game mode."""
        res = None

        try:
            with DBConnection().connection as connexion:
                with connexion.cursor() as cursor:
                    query = """
                        SELECT g.*
                        FROM game g
                        WHERE %(id_player)s IN (g.id_player1, g.id_player2)
                    """

                    params = {
                        "id_player": id_player,
                    }

                    if game_mode is not None:
                        query += " AND g.game_mode = %(game_mode)s"
                        params["game_mode"] = game_mode

                    query += ";"

                    cursor.execute(query, params)
                    res = cursor.fetchall()

        except Exception as e:
            logger.error(e)
            raise

        games_list = []

        if res:
            for row in res:
                p1 = PlayerDao().find_by_id(row["id_player1"])
                p2 = PlayerDao().find_by_id(row["id_player2"])
                winner = PlayerDao().find_by_id(row["id_winner"])

                game = Game(
                    player1=p1,
                    player2=p2,
                    game_mode=row["game_mode"],
                    winner=winner,
                    description=row["detail"],
                    timestamp=row["timestamp"],
                    id_game=row["id_game"],
                )

                games_list.append(game)

        return games_list
