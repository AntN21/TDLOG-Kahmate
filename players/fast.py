from players.rugbyPlayer import RugbyPlayer
from constants import FAST_ATT_BONUS, FAST_DEF_BONUS, FAST_MAX_MOVE

class Fast(RugbyPlayer):
    """Define a 'Fast' player with its characteristics."""

    def __init__(self, team):
        super().__init__(
            "fast", team, FAST_MAX_MOVE, FAST_ATT_BONUS, FAST_DEF_BONUS
        )
