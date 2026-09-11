import os

import requests

print(os.getcwd())
from business_object.game import Game
from business_object.player import Player


class GameClient:
    def get_games(self) -> list[Game]:
        try:
            r = requests.get(url="http://localhost:5555/")
            r.raise_for_status()
            raw_json = r.json()

            games = []

            for elt in raw_json:
                # Create an object
                g = Game(
                    player1=Player(username=elt["players_list"][0], elo=None, email=None),
                    player2=Player(username=elt["players_list"][1], elo=None, email=None),
                    game_mode=elt["mode_type"],
                    winner=Player(username=elt["winner_name"], elo=None, email=None),
                    description=elt["details"],
                    id_game=elt["id"],
                    timestamp=elt["duration_seconds"],
                )

                # If it succeed, add to the list
                if g:
                    games.append(g)

            return games
        except Exception as e:
            print(f"erreur : {e}")
            return None
