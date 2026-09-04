
from abc import ABC, abstractmethod

from game.py import Game
from player.py import Player


class GameMode(ABC):

    @abstractmethod
    def play(p1: Player, p2: Player) -> Game:
        pass
