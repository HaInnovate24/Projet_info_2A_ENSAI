from business_object.game import Game
from dao.db_connection import DBConnection
from dao.player_dao import PlayerDAO
from utils.log_utils import get_logger
from utils.singleton import Singleton

logger = get_logger(__name__)


class GameDAO(metaclass=Singleton):
    def create(self, game: Game) -> bool:
        try:
            # Step 1: We get the connection using the DBConnection class.
            with DBConnection().connection as connection:
                # Step 2: From the connection, we create a cursor for the query.
                with connection.cursor() as cursor:
                    # Step 3: We execute our SQL query.
                    query = (
                        "INSERT INTO project.game(id_player1, id_player2, game_mode, id_winner, detail)"
                        "VALUES %s, %s, %s, %s, %s);"
                    )

                    data = (
                        game.player_2.id_player,
                        game.player_2.id_player,
                        game.game_mode,
                        game.winner.id_player,
                        game.description,
                    )

                    cursor.execute(query, data)

                    # Step 4: We store the query result.
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            # Step 5: We format the results into the desired shape (object, list...).
            game.id_game = res["id_game"]
            created = True

        return created

    def find_by_id(self, id_game):
        """Find a game by their id.
        Args:
            id_game (int): The ID of the game to find
        Returns:
            Game matching the given id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
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
            game = Game(
                id_game=res["id_game"],
                player1=PlayerDAO.find_by_id(res["id_player1"]),
                player2=PlayerDAO.find_by_id(res["id_player2"]),
                game_mode=res["game_mode"],
                winner=PlayerDAO.find_by_id(res["id_winner"]),
                description=res["detail"],
                timestamp=res["timestamp"],
            )

        return game
