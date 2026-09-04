

from game_mode.py import GameMode

from coinflip_mode.py import CoinFlipMode
from dice_mode.py import DiceMode


class GameModeFactory:
    @classmethod
    def get_mode(cls, game_mode: str) -> GameMode:
        """
        Returns the corresponding GameMode object.
        Args:
            game_mode (str): The identifier of the game mode (e.g., 'coinflip', 'dice').
        Returns:
            GameMode: An instance of a class implementing GameMode.
        Raises:
            ValueError: If the requested game_mode is not supported.
        """

        if isinstance(game_mode, str):
            if (game_mode == "coinflip"):
                cls.game_mode = CoinFlipMode

            elif (game_mode == "dice"):
                cls.game_mode = DiceMode
            else:
                raise ValueError("The game must be coinflip or dice")
        else:
            raise TypeError("The game_mode must be of type str")

        return cls.game_mode
