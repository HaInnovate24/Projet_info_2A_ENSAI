import requests

from business_object.game import Game
from business_object.player import Player


class GameClient:
    def __init__(self, url="http://127.0.0.1:5555"):
        self.url = url
        self.data = None

    def get_games(self) -> list[Game]:
        #      player1: Player,
        # player2: Player,
        # game_mode: str,
        # winner: Player | None,
        # description: str,
        # timestamp: datetime,
        # id_game: int = None,
        try:
            r = requests.get(self.url)
            r.raise_for_status()

            json_data = r.json()

            data = []
            for d in json_data:
                players = d.get("players_list")
                data.append(
                    Game(
                        player1=Player(username=players[0], elo=None, email=None),
                        player2=Player(username=players[1], elo=None, email=None),
                        game_mode=d.get("mode_type"),
                        winner=Player(username=d.get("winner_name"), elo=None, email=None),
                        description=d.get("details"),
                        timestamp=d.get("duration_seconds"),
                        id_game=d.get("id"),
                    )
                )

            return data

        except Exception:
            print("Il y a un soucis !!")
            return None
