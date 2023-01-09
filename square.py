class Square:
    """
    Contain the information about a square of the board:
        - if the ball is on this square (bool ball);
        - if a player is on this square (RugbyPlayer player, None if not).
        - if it is available for a move or not
    """

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._ball = False
        self._player = None
        self._selected = False
        self._available = False

    def __str__(self):
        if self.player is None:
            return "   *   "
        return str(self.player)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def get_position(self):
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
    def selected(self):
        return self._selected
    
    @property
    def available(self):
        """Return True if the square is available for a move, False if not."""
        return self._available

    def set_ball(self, ball):
        """Set if the ball is on the square."""
        self._ball = ball

    def set_player(self, player):
        """A player comes on this square, _player takes the values of this player."""
        self._player = player

    def set_selected(self, selected):
        self._selected = selected

    def set_available(self, available):
        """The square is highlighted"""
        self._available = available

    def has_not_player(self):
        """
        A player leaves this square, _player turns into None.
        Return the player who left.
        """
        player = self.player
        self._player = None
        return player

    def l1_distance(self, square2):
        return abs(self.x - square2.x) + abs(self.y - square2.y)
