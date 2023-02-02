"""
Ordinary player class file
"""
from players.rugby_player import RugbyPlayer
from constants import ORDINARY_ATT_BONUS, ORDINARY_DEF_BONUS, ORDINARY_MAX_MOVE


class Ordinary(RugbyPlayer):
    """Define an 'Ordinary' player with its characteristics."""

    def __init__(self, team):
        super().__init__(
            "ordinary",
            team,
            ORDINARY_MAX_MOVE,
            ORDINARY_ATT_BONUS,
            ORDINARY_DEF_BONUS,
        )
