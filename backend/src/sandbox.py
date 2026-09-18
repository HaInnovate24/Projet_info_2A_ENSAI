# uv run --project backend python backend/src/sandbox.py
from business_object.game import Game
from business_object.player import Player
from dao.game_dao import GameDao
from utils.env_variables import load_environment_variables

load_environment_variables()  # Required to load the variables needed (env) to connect to the database

p1 = Player(username="T", elo=1234, email="T@gmail.com")
p2 = Player(username="P", elo=234, email="P@gmail.com")
game = Game(
    player1=p1,
    player2=p2,
    game_mode="dice",
    winner=p1,
    description="5 v 2",
    timestamp=2026 - 10 - 20,
)

id = GameDao().create(game)
print(id)
game2 = GameDao().find_by_id(id)
