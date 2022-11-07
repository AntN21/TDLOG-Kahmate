import constants as cst


class RugbyPlayer:
    """
    Contain different properties of a rugby player:
        - if he is stunt or not (bool stunt);
        - his number of maximum movements (int max_move);
        - his bonuses for attack (int att_bonus) and defence (int def_bonus);
    """

    def __init__(self, team, max_move, att_bonus, def_bonus):
        assert (team == 'red' or team == 'blue'), f'{team} is not a correct team color.'
        self._team = team
        self._stunned = False
        self._max_move = max_move
        self._att_bonus = att_bonus
        self._def_bonus = def_bonus
        self._available_moves = self.max_move

    @property
    def team(self):
        """Return the team color of the player."""
        return self._team

    @property
    def stunned(self):
        """Return the stunning state of the player."""
        return self._stunned

    @property
    def max_move(self):
        """Return the maximum movements the player can do."""
        return self._max_move

    @property
    def att_bonus(self):
        """Return the attack bonus of the player."""
        return self._att_bonus

    @property
    def def_bonus(self):
        """Return the defense bonus of the player."""
        return self._def_bonus

    @property
    def available_moves(self):
        """Return the number of available moves of the player."""
        return self._available_moves

    def is_stunned(self):
        """Turn the player stunning state into True."""
        self._stunned = True

    def is_not_stunned(self):
        """Turn the player stunning state into False."""
        self._stunned = False

    def move(self, n):
        """Reduce _available_moves of n moves."""
        assert n <= self.available_moves, 'The player has not enough available moves to go that far.'
        self._available_moves -= n

    def reset_moves(self):
        """Reset _available_moves to the maximum number of moves."""
        self._available_moves = self.max_move

    def full_reset(self):
        """Reset the state of the player : stunning state and available moves."""
        self.is_not_stunned()
        self.reset_moves()


class Ordinaire(RugbyPlayer):
    """Define an 'ordinaire' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, cst.ORDINAIRE_MAX_MOVE, cst.ORDINAIRE_ATT_BONUS, cst.ORDINAIRE_DEF_BONUS)


class Costaud(RugbyPlayer):
    """Define a 'costaud' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, cst.COSTAUD_MAX_MOVE, cst.COSTAUD_ATT_BONUS, cst.COSTAUD_DEF_BONUS)


class Dur(RugbyPlayer):
    """Define a 'dur' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, cst.DUR_MAX_MOVE, cst.DUR_ATT_BONUS, cst.DUR_DEF_BONUS)


class Rapide(RugbyPlayer):
    """Define a 'rapide' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, cst.RAPIDE_MAX_MOVE, cst.RAPIDE_ATT_BONUS, cst.RAPIDE_DEF_BONUS)


class Fute(RugbyPlayer):
    """Define a 'fute' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, cst.FUTE_MAX_MOVE, cst.FUTE_ATT_BONUS, cst.FUTE_DEF_BONUS)


class Square:
    """
    Contain the information about a square of the board:
        - if the ball is on this square (bool ball);
        - if a player is on this square (RugbyPlayer player, None if not).
    """

    def __init__(self):
        self._ball = False
        self._player = None

    @property
    def ball(self):
        """Return True if the ball is on the square and False if not."""
        return self._ball

    @property
    def player(self):
        """Return the RugbyPlayer on the square, None if there is none."""
        return self._player

    def has_ball(self):
        """The ball comes on this square, _ball turns into True."""
        self._ball = True

    def has_not_ball(self):
        """The ball leaves this square, _ball turns into False."""
        self._ball = False

    def has_player(self, player):
        """A player comes on this square, _player takes the values of this player."""
        self._player = player

    def has_not_player(self):
        """
        A player leaves this square, _player turns into None.
        Return the player who left.
        """
        player = self.player
        self._player = None
        return player


class Board:
    """
    Contain the structure of the field:
        - the length (int length) and the width (int width);
        - the squares of the field.
    """

    def __init__(self):
        self._length = cst.BOARD_LENGTH
        self._width = cst.BOARD_WIDTH
        self._squares = []
        for y in range(self.width):
            for x in range(self.length):
                self._squares.append(Square())

    @property
    def length(self):
        """Return the field length."""
        return self._length

    @property
    def width(self):
        """Return the field width."""
        return self._width

    @property
    def squares(self):
        """Return the list of the squares."""
        return self._squares

    def square(self, x, y):
        """Return the square of coordinates x and y."""
        return self.squares[self.length * y + x]

    def put_ball(self, x, y):
        """Put the ball in the (x,y) square."""
        self._squares[self.length * y + x].has_ball()

    def put_player(self, player, x, y):
        """Put the ball in the (x,y) square."""
        self._squares[self.length * y + x].has_player(player)

    def move_ball(self, x1, y1, x2, y2):
        """Move the ball from (x1,y1) to (x2,y2)."""
        self._squares[self.length * y1 + x1].has_not_ball()
        self._squares[self.length * y2 + x2].has_ball()

    def move_player(self, x1, y1, x2, y2):
        """Move the player from (x1,y1) to (x2,y2)."""
        self._squares[self.length * y2 + x2].has_player(self._squares[self.length * y1 + x1].has_not_player())


class Action:

    pass





def test():
    player = Fute('red')
    board = Board()
    x = 6
    y = 2
    x2 = 9
    y2 = 4

    board.put_player(player, x, y)

    board.move_player(x, y, x2, y2)

    if board.square(x, y).player is not None:
        print(board.square(x, y).player.def_bonus)
    else:
        print('no player')
    print(board.square(x2, y2).player.def_bonus)

    pass

test()







