"""
File containing the Board class information
"""
from constants import BOARD_HEIGHT, BOARD_WIDTH
from square import Square


class Board:
    """
    Contain the structure of the field:
        - the length (int length) and the width (int width);
        - the squares of the field.
    """

    def __init__(self):
        self._width = BOARD_WIDTH
        self._height = BOARD_HEIGHT
        self._squares = []
        for row in range(self.height):
            for col in range(self.width):
                self._squares.append(Square(col, row))

    @property
    def width(self):
        """Return the field's width."""
        return self._width

    @property
    def height(self):
        """Return the field's height."""
        return self._height

    @property
    def squares(self):
        """Return the list of the squares."""
        return self._squares

    def square(self, pos_x, pos_y):
        """Return the square of coordinates x and y."""
        return self._squares[self.width * pos_y + pos_x]

    def __call__(self, pos):
        return self.square(pos[0], pos[1])

    def put_ball(self, pos_x, pos_y):
        """Put the ball in the (x,y) square."""
        self._squares[self.width * pos_y + pos_x].set_ball(True)

    def put_player(self, player, pos_x, pos_y):
        """Put the argument player in the (x,y) square."""
        self._squares[self.width * pos_y + pos_x].set_player(player)

    def clear_selected(self):
        """Sets all squares to be not selected"""
        for square in self._squares:
            square.set_selected(False)

    def clear_available(self):
        """Sets all squares to be not available"""
        for square in self._squares:
            square.set_available(False)

    def move_ball(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """Move the ball from (x1,y1) to (x2,y2)."""
        self._squares[self.width * pos_y1 + pos_x1].set_ball(False)
        self._squares[self.width * pos_y2 + pos_x2].set_ball(True)

    def move_player(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """Move the player from (x1,y1) to (x2,y2)."""
        player = self._squares[self.width * pos_y1 + pos_x1].player
        self._squares[self.width * pos_y1 + pos_x1].set_player(None)
        self._squares[self.width * pos_y2 + pos_x2].set_player(player)
