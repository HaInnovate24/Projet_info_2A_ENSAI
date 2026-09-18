from business_object.game import Game
from dao.game_dao import GameDAO
from service.game_service import GameService
from utils.env_variables import display_values, load_environment_variables
from utils.log_utils import initialize_logs

# uv run --project backend python backend/src/sandbox.py


# Initialization
initialize_logs("Webservice")

load_environment_variables()
display_values()


g = GameService().play(3, 5, "coinflip", choice="tails")
print(g)

print(f"{g.player1.username} : new elo -> {g.player1.elo}")
print(f"{g.player2.username} : new elo -> {g.player2.elo}")

g2 = GameService().play(3, 5, "dice")
print(g2)

print(f"{g2.player1.username} : new elo -> {g2.player1.elo}")
print(f"{g2.player2.username} : new elo -> {g2.player2.elo}")


p1 = g2.player1
p2 = g2.player2
game = Game(
    player1=p1,
    player2=p2,
    game_mode="coinflip",
    winner=p1,
    description="SOme deqsc",
    timestamp=g2.timestamp,
)

id = GameDAO().create(game)
print(id)
game2 = GameDAO().find_by_id(game.id_game)
