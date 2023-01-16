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
        for y in range(self.height):
            for x in range(self.width):
                self._squares.append(Square(x, y))

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

    def square(self, x, y):
        """Return the square of coordinates x and y."""
        return self._squares[self.width * y + x]

    def __call__(self, p):
        return self.square(p[0], p[1])

    def put_ball(self, x, y):
        """Put the ball in the (x,y) square."""
        self._squares[self.width * y + x].set_ball(True)

    def put_player(self, player, x, y):
        """Put the argument player in the (x,y) square."""
        self._squares[self.width * y + x].set_player(player)

    def clear_selected(self):
        for square in self._squares:
            square.set_selected(False)

    def clear_available(self):
        for square in self._squares:
            square.set_available(False)

    def nb_players(self, team):
        nb_players = 0
        for square in self.squares:
            if square.player is not None:
                if square.player.team == team:
                    nb_players += 1
        return nb_players

    def move_ball(self, x1, y1, x2, y2):
        """Move the ball from (x1,y1) to (x2,y2)."""
        self._squares[self.width * y1 + x1].set_ball(False)
        self._squares[self.width * y2 + x2].set_ball(True)

    def move_player(self, x1, y1, x2, y2):
        """Move the player from (x1,y1) to (x2,y2)."""
        player = self._squares[self.width * y1 + x1].player
        self._squares[self.width * y1 + x1].set_player(None)
        self._squares[self.width * y2 + x2].set_player(player)
