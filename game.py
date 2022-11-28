import constants as cst
import random as rd


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

    def __str__(self):
        return f' {self.team[0]} Ord '


class Costaud(RugbyPlayer):
    """Define a 'costaud' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, cst.COSTAUD_MAX_MOVE, cst.COSTAUD_ATT_BONUS, cst.COSTAUD_DEF_BONUS)

    def __str__(self):
        return f' {self.team[0]} Cos '


class Dur(RugbyPlayer):
    """Define a 'dur' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, cst.DUR_MAX_MOVE, cst.DUR_ATT_BONUS, cst.DUR_DEF_BONUS)

    def __str__(self):
        return f' {self.team[0]} Dur '


class Rapide(RugbyPlayer):
    """Define a 'rapide' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, cst.RAPIDE_MAX_MOVE, cst.RAPIDE_ATT_BONUS, cst.RAPIDE_DEF_BONUS)

    def __str__(self):
        return f' {self.team[0]} Rap '


class Fute(RugbyPlayer):
    """Define a 'fute' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, cst.FUTE_MAX_MOVE, cst.FUTE_ATT_BONUS, cst.FUTE_DEF_BONUS)

    def __str__(self):
        return f' {self.team[0]} Fut '


class Square:
    """
    Contain the information about a square of the board:
        - if the ball is on this square (bool ball);
        - if a player is on this square (RugbyPlayer player, None if not).
    """

    def __init__(self):
        self._ball = False
        self._player = None

    def __str__(self):
        if self.ball:
            if self.player is None:
                return '   B   '
            return str(self.player[1:5] + ' B')
        if self.player is None:
            return '   *   '
        return str(self.player)

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
        return self._squares[self.length * y + x]

    def __call__(self, p):
        return self.square(p[0], p[1])

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
    def __init__(self, random=False):
        self._board=Board()
        self.selected_case1=None #could represent the rugby player who throws the ball
        self.selected_case2=None
        # Players initialization
        if random:
            self.random_placing()
        else:
            self.input_placing()
        # Ball initialization
        self._board._squares[self.board.length * rd.randint(1, self.board.width - 2) + self.board.length//2].has_ball()

    @property
    def board(self):
        """Return the field length."""
        return self._board

    def random_placing(self):
        """Place the players randomly in the legal cases."""

        # Red team
        n = 6           # Remaining players to place
        while n > 0:
            x = rd.randint(1, 2)
            y = rd.randint(0, self.board.width - 1)
            if self.board([x, y]).player is None:
                if n == 6 or n == 5:
                    self._board.put_player(Ordinaire('red'), x, y)
                elif n == 4:
                    self._board.put_player(Costaud('red'), x, y)
                elif n == 3:
                    self._board.put_player(Dur('red'), x, y)
                elif n == 2:
                    self._board.put_player(Rapide('red'), x, y)
                else:
                    self._board.put_player(Fute('red'), x, y)
                n -= 1

        # Blue team
        n = 6           # Remaining players to place
        while n > 0:
            x = rd.randint(self.board.length - 3, self.board.length - 2)
            y = rd.randint(0, self.board.width - 1)
            if self.board([x, y]).player is None:
                if n == 6 or n == 5:
                    self._board.put_player(Ordinaire('blue'), x, y)
                elif n == 4:
                    self._board.put_player(Costaud('blue'), x, y)
                elif n == 3:
                    self._board.put_player(Dur('blue'), x, y)
                elif n == 2:
                    self._board.put_player(Rapide('blue'), x, y)
                else:
                    self._board.put_player(Fute('blue'), x, y)
                n -= 1

    def input_placing(self):
        """Place the players according to the inputs."""

        colors = ['red', 'blue']
        team = 0        # Choosing team (0='red' 1='blue')
        x_start = [1, self.board.length - 3]
        x_end = [2, self.board.length - 2]
        n = 6           # Remaining players to place
        while n > 0:
            x = int(input(f'{colors[team]} team choose {cst.PLAYERS_TYPES_LIST[6 - n]} player column between '
                          f'{x_start[team]} and {x_end[team]} : '))
            assert x_start[team] <= x <= x_end[team], 'T\'es con ou quoi ?'
            y = int(input(f'{colors[team]} team choose {cst.PLAYERS_TYPES_LIST[6 - n]} player row between 0 and '
                      f'{self.board.width - 1} : '))
            assert 0 <= y <= self.board.width - 1, 'T\'es con ou quoi ?'

            if self.board([x, y]).player is None:
                if n == 6 or n == 5:
                    self._board.put_player(Ordinaire(colors[team]), x, y)
                elif n == 4:
                    self._board.put_player(Costaud(colors[team]), x, y)
                elif n == 3:
                    self._board.put_player(Dur(colors[team]), x, y)
                elif n == 2:
                    self._board.put_player(Rapide(colors[team]), x, y)
                else:
                    self._board.put_player(Fute(colors[team]), x, y)
                if team == 0:
                    team += 1
                else:
                    team = 0
                    n -= 1
            else:
                print('Unavailable placement.')





def test_placing():
    game = Game()

    for y in range(game.board.width - 1, -1, -1):
        res = ''
        for x in range(game.board.length):
            res += str(game.board([x, y]))
        print(res)

    pass


def test_move_player():
    player = Fute('red')
    board = Board()
    x = 6
    y = 2
    x2 = 9
    y2 = 4

    board.put_player(player, x, y)

    board.move_player(x, y, x2, y2)

    assert board.square(x, y).player is None

    assert isinstance(board.square(x2, y2).player, Fute)

    pass






