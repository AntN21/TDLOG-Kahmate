"""
Clever player class file
"""
from players.rugby_player import RugbyPlayer
from constants import CLEVER_ATT_BONUS, CLEVER_DEF_BONUS, CLEVER_MAX_MOVE, PlayerType


class Clever(RugbyPlayer):
    """Define a 'Clever' player with its characteristics."""

    def __init__(self, team):
        super().__init__(
            PlayerType.CLEVER, team, CLEVER_MAX_MOVE, CLEVER_ATT_BONUS, CLEVER_DEF_BONUS
        )
