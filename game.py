import random


# Constants
BOARD_LENGTH = 13
BOARD_WIDTH = 8

ORDINAIRE_MAX_MOVE = 3
ORDINAIRE_ATT_BONUS = 0
ORDINAIRE_DEF_BONUS = 0

COSTAUD_MAX_MOVE = 2
COSTAUD_ATT_BONUS = 2
COSTAUD_DEF_BONUS = 1

DUR_MAX_MOVE = 3
DUR_ATT_BONUS = 1
DUR_DEF_BONUS = 0

RAPIDE_MAX_MOVE = 4
RAPIDE_ATT_BONUS = -1
RAPIDE_DEF_BONUS = -1

FUTE_MAX_MOVE = 3
FUTE_ATT_BONUS = 0
FUTE_DEF_BONUS = 1


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
        self._is_stunt = False
        self._max_move = max_move
        self._att_bonus = att_bonus
        self._def_bonus = def_bonus

    @property
    def team(self):
        """Return the team color of the player."""
        return self._team

    @property
    def is_stunt(self):
        """Return the stunning state of the player."""
        return self._is_stunt

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


class Ordinaire(RugbyPlayer):
    """Define an 'ordinaire' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, ORDINAIRE_MAX_MOVE, ORDINAIRE_ATT_BONUS, ORDINAIRE_DEF_BONUS)


class Costaud(RugbyPlayer):
    """Define a 'costaud' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, COSTAUD_MAX_MOVE, COSTAUD_ATT_BONUS, COSTAUD_DEF_BONUS)


class Dur(RugbyPlayer):
    """Define a 'dur' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, DUR_MAX_MOVE, DUR_ATT_BONUS, DUR_DEF_BONUS)


class Rapide(RugbyPlayer):
    """Define a 'rapide' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, RAPIDE_MAX_MOVE, RAPIDE_ATT_BONUS, RAPIDE_DEF_BONUS)


class Fute(RugbyPlayer):
    """Define a 'fute' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, FUTE_MAX_MOVE, FUTE_ATT_BONUS, FUTE_DEF_BONUS)


class Square:
    """
    Contain the information about a square of the board:
        - its position (int x and int y);
        - if the ball is on this square (bool ball);
        - if a player is on this square (RugbyPlayer player, None if not).
    """

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._ball = False
        self._player = None

    @property
    def x(self):
        """Return the x position of the square."""
        return self._x

    @property
    def y(self):
        """Return the y position of the square."""
        return self._y

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
        """A player leaves this square, _player turns into None."""
        self._player = None


class Board:
    """
    Contain the structure of the field:
        - the length (int length) and the width (int width);
        - the squares of the field.
    """

    def __init__(self):
        self._length = BOARD_LENGTH
        self._width = BOARD_WIDTH
        self._squares = []
        for y in range(self.width):
            for x in range(self.length):
                self._squares.append(Square(x, y))

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
        return self._squares[self.length * y + x]
    def __call__(self,p):
        return self.square(p[0],p[1])


# Maybe unnecessary
class RugbyTeam:
    """Contain the information about a team of RugbyPlayers."""

    def __init__(self, board, color):
        assert (color == 'red' or color == 'blue'), f'{color} is not a correct color.'
        self._color = color

    pass


class Action:
    def __init__(self):
        pass
    pass


#-Déplacement -Passe -> interception => Duel -coup de pied à suivre -Marquer un essai -Plaquage (parfait) => Duel -Forcer le passage => Duel
# red à gauche blue à droite
 #essai
class Pass(Action):
    def __init__(self):
        super().__init__()

    def is_possible(self,game):
        case1=game.selected_case1
        case2=game.selected_case2
        if case1.player is not None and case2.player is not None:
            if case1.ball==True:
                if case1.player.team==case2.player.team:
                    if abs(case1.y-case2.y)<3:
                        if (case2.x < case1.x and case1.x-case2.x<=2  and case1.player.team=="red") or (case1.x < case2.x and case2.x-case1.x<=2 and case2.player.team=='blue'):
                            return True
        return False

    def play(self,game):
        #if not(is_possible(game)) : raise Exception("can't throw")
        #if truc : interception
        game.selected_case1.ball = False
        game.selected_case2.ball = True

class Duel(Action):
    def __init__(self):
        super().__init__()

    def play(self,game):
        #tirer carte1
        #tirer carte2
        #if carte1>carte2:
        #   return 'red'
        #else:
        #   return 'blue'
        pass

    pass
class BallKick(Action):
    def __init__(self):
        super().__init__()

    def is_possible(self,game):
        case1=game.selected_case1
        case2=game.selected_case2
        if case1.player is not None:
            if case1.ball==True:
                    if abs(case1.y-case2.y)<=3:
                        if (case2.x > case1.x and case2.x<=3 +case1.x  and case1.player.team=="red") or (case1.x > case2.x and case1.x<=3+case2.x and case2.player.team=='blue'):
                            return True
        return False

    def play(self,game):
        game.selected_case1.ball = False
        game.selected_case2.ball = True
    pass
class Plaquage(Action):
    def __init__(self):
        super().__init__()
    pass

#essai
class Game:
    def __init__(self):
        self._board=Board()
        self.selected_case1=None #could represent the rugby player who throws the ball
        self.selected_case2=None

    @property
    def board(self):
        """Return the field length."""
        return self._board















