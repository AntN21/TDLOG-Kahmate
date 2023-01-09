from players.rugbyPlayer import RugbyPlayer
from constants import TOUGH_ATT_BONUS, TOUGH_DEF_BONUS, TOUGH_MAX_MOVE 

class Tough(RugbyPlayer):
    """Define a 'Tough' player with its characteristics."""

    def __init__(self, team):
        super().__init__("tough", team, TOUGH_MAX_MOVE, TOUGH_ATT_BONUS, TOUGH_DEF_BONUS)
