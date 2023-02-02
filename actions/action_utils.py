"""Some methods used by different actions"""
import math
from constants import Teams


def forward(team):
    """Indicates wich direction is forward"""
    return 1 if team == Teams.RED.value else -1


def path_exists(path_length, board, position1, position2):
    """Check that a path exists between two positions given a player's status"""
    return tuple(position2) in accessibles_cases(path_length, board, position1)


def inbound(board, pos):
    """Checks if a position is inside the board"""
    return 0 <= pos[0] < board.width and 0 <= pos[1] < board.height


def get_neighbours(pos):
    """Returns the 4 squares next to the current position"""
    neighbours = []
    for angle in [0, math.pi / 2, math.pi, -math.pi / 2]:
        neighbours.append(
            [pos[0] + int(math.cos(angle)), pos[1] + int(math.sin(angle))]
        )
    return neighbours


def accessibles_cases(path_length, board, position1):
    """
    Gets the set of all accessible cases from a position and a given amount of
    movements.
    """
    acc_cases = set(tuple(i) for i in [position1])
    new_cases = []
    for i in range(path_length):
        for new_case in new_cases:
            acc_cases.add(new_case)
        new_cases = []
        for case in acc_cases:
            for n_case in get_neighbours(case):
                if inbound(board, n_case):
                    player = board(n_case).player
                    if player is None or player.get_just_lost():
                        new_cases.append(tuple(n_case))
    return new_cases
