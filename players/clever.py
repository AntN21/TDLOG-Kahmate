from players.rugbyPlayer import RugbyPlayer
from constants import CLEVER_ATT_BONUS, CLEVER_DEF_BONUS, CLEVER_MAX_MOVE

class Clever(RugbyPlayer):
    """Define a 'Clever' player with its characteristics."""

    def __init__(self, team):
        super().__init__(
            "clever", team, CLEVER_MAX_MOVE, CLEVER_ATT_BONUS, CLEVER_DEF_BONUS
        )

    def __str__(self):
        return f"clever_{self.team}"
