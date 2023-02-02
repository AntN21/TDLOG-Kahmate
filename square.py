"""
File containing all the information of the Square class
"""


class Square:
    """
    Contain the information about a square of the board:
        - if the ball is on this square (bool ball);
        - if a player is on this square (RugbyPlayer player, None if not).
        - if it is available for a move or not
        - if it is selected
    """

    def __init__(self, pos_x, pos_y):
        self._x = pos_x
        self._y = pos_y
        self._ball = False
        self._player = None
        self._available = False
        self._selected = False

    def __str__(self):
        if self.player is None:
            return "   *   "
        return str(self.player)

    @property
    def pos_x(self):
        """Returns the x coordinate of the square"""
        return self._x

    @property
    def pos_y(self):
        """Returns the y coordinate of the square"""
        return self._y

    def get_position(self):
        """Returns a tuple with the position of the square"""
        return tuple((self._x, self._y))

    @property
    def ball(self):
        """Return True if the ball is on the square and False if not."""
        return self._ball

    @property
    def player(self):
        """Return the RugbyPlayer on the square, None if there is none."""
        return self._player

    @property
    def available(self):
        """Return True if the square is available for a move"""
        return self._available

    @property
    def selected(self):
        """Returns if the square is available"""
        return self._selected

    def set_ball(self, ball):
        """Set if the ball is on the square."""
        self._ball = ball

    def set_player(self, player):
        """Set the player of the square (None to leave it empty)"""
        self._player = player

    def set_available(self, available):
        """Sets the square as available"""
        self._available = available

    def set_selected(self, selected):
        """Sets the square as selected"""
        self._selected = selected

    def remove_player(self):
        """
        A player leaves this square, _player turns into None.
        Return the player who left.
        """
        player = self.player
        self._player = None
        return player

    def l1_distance(self, square2):
        """Returns the distance from other square (without diagonals)"""
        return abs(self.pos_x - square2.x) + abs(self.pos_y - square2.y)
