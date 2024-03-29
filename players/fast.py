"""
Fast player class file
"""
from players.rugby_player import RugbyPlayer
from constants import FAST_ATT_BONUS, FAST_DEF_BONUS, FAST_MAX_MOVE, PlayerType


class Fast(RugbyPlayer):
    """Define a 'Fast' player with its characteristics."""

    def __init__(self, team):
        super().__init__(
            PlayerType.FAST, team, FAST_MAX_MOVE, FAST_ATT_BONUS, FAST_DEF_BONUS
        )
