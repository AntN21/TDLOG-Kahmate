"""
Strong player class file
"""
from players.rugby_player import RugbyPlayer
from constants import STRONG_ATT_BONUS, STRONG_DEF_BONUS, STRONG_MAX_MOVE


class Strong(RugbyPlayer):
    """Define a 'Strong' player with its characteristics."""

    def __init__(self, team):
        super().__init__(
            "strong", team, STRONG_MAX_MOVE, STRONG_ATT_BONUS, STRONG_DEF_BONUS
        )
