"""
file containing all the classes defined in the players folger
"""

from constants import PlayerType, Teams
from players.clever import Clever
from players.fast import Fast
from players.ordinary import Ordinary
from players.rugby_player import RugbyPlayer
from players.strong import Strong
from players.tough import Tough

# List of the RugbyPlayer subclasses in the same order as the enum defined in constants.py
RUGBY_PLAYERS = [Ordinary, Clever, Strong, Tough, Fast]

assert all(
    [
        index == RUGBY_PLAYERS[index](Teams.RED).type.value
        for index in range(len(RUGBY_PLAYERS))
    ]
)
