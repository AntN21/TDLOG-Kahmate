from enum import Enum

# Board characteristics
BOARD_WIDTH = 13
BOARD_HEIGHT = 8

# 'ordinary' player characteristics
ORDINARY_MAX_MOVE = 3
ORDINARY_ATT_BONUS = 0
ORDINARY_DEF_BONUS = 0

# 'strong' player characteristics
STRONG_MAX_MOVE = 2
STRONG_ATT_BONUS = 2
STRONG_DEF_BONUS = 1

# 'tough' player characteristics
TOUGH_MAX_MOVE = 3
TOUGH_ATT_BONUS = 1
TOUGH_DEF_BONUS = 0

# 'fast' player characteristics
FAST_MAX_MOVE = 4
FAST_ATT_BONUS = -1
FAST_DEF_BONUS = -1

# 'clever' player characteristics
CLEVER_MAX_MOVE = 3
CLEVER_ATT_BONUS = 0
CLEVER_DEF_BONUS = 1


# Teams
RED_TEAM = "red"
BLUE_TEAM = "blue"

# Actions
MOVE = "Move"
PASS = "Pass"
BALL_KICK = "BallKick"
PLACKAGE = "Plackage"
FORCED_PASSAGE = "ForcedPassage"
