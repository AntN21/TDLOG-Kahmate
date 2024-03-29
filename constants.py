"""
File with all the game constants
"""
from enum import Enum

# Board characteristics
BOARD_WIDTH = 13  # The width includes both goals
BOARD_HEIGHT = 8


class PlayerType(Enum):
    """
    Enumerator of player type
    """

    ORDINARY = 0
    CLEVER = 1
    STRONG = 2
    TOUGH = 3
    FAST = 4

    def __str__(self):
        return f"{self.name}".lower()


# Ordinary player characteristics
ORDINARY_MAX_MOVE = 3
ORDINARY_ATT_BONUS = 0
ORDINARY_DEF_BONUS = 0

# Strong player characteristics
STRONG_MAX_MOVE = 2
STRONG_ATT_BONUS = 2
STRONG_DEF_BONUS = 1

# Tough player characteristics
TOUGH_MAX_MOVE = 3
TOUGH_ATT_BONUS = 1
TOUGH_DEF_BONUS = 0

# Fast player characteristics
FAST_MAX_MOVE = 4
FAST_ATT_BONUS = -1
FAST_DEF_BONUS = -1

# Clever player characteristics
CLEVER_MAX_MOVE = 3
CLEVER_ATT_BONUS = 0
CLEVER_DEF_BONUS = 1


class Teams(Enum):
    """
    Enumerator of both teams colors
    """

    RED = 0
    BLUE = 1

    def __str__(self):
        return f"{self.name}".lower()

    def other(self, team):
        """Returns the opposite team"""
        if team == Teams.BLUE:
            return Teams.RED
        if team == Teams.RED:
            return Teams.BLUE
        return None


def other(team):
    """Returns the opposite team"""
    if team == Teams.BLUE.value:
        return Teams.RED.value
    if team == Teams.RED.value:
        return Teams.BLUE.value
    return None


def get_goal(team):
    """Get the back of the team's side"""
    return BOARD_WIDTH - 1 if team == Teams.RED else 0


class Actions(Enum):
    """
    Enumerator of all possible actions
    """

    MOVE = "Move"
    PASS = "Pass"
    BALL_KICK = "BallKick"
    TACKLE = "Tackle"
    FORCED_PASSAGE = "ForcedPassage"
