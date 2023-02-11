"""
Functions shared among some python test files
"""

import random as r

r.seed(1)


def get_random_coordinates(board):
    """Gets a random pair of coordinates to test a function"""
    x_square = r.randint(0, board.width - 1)
    y_square = r.randint(0, board.height - 1)
    return x_square, y_square
