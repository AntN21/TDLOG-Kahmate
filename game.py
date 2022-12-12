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
        assert team == "red" or team == "blue", f"{team} is not a correct team color."
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
        assert (
            n <= self.available_moves
        ), "The player has not enough available moves to go that far."
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
        super().__init__(
            team,
            cst.ORDINAIRE_MAX_MOVE,
            cst.ORDINAIRE_ATT_BONUS,
            cst.ORDINAIRE_DEF_BONUS,
        )


class Costaud(RugbyPlayer):
    """Define a 'costaud' player with its characteristics."""

    def __init__(self, team):
        super().__init__(
            team, cst.COSTAUD_MAX_MOVE, cst.COSTAUD_ATT_BONUS, cst.COSTAUD_DEF_BONUS
        )


class Dur(RugbyPlayer):
    """Define a 'dur' player with its characteristics."""

    def __init__(self, team):
        super().__init__(team, cst.DUR_MAX_MOVE, cst.DUR_ATT_BONUS, cst.DUR_DEF_BONUS)


class Rapide(RugbyPlayer):
    """Define a 'rapide' player with its characteristics."""

    def __init__(self, team):
        super().__init__(
            team, cst.RAPIDE_MAX_MOVE, cst.RAPIDE_ATT_BONUS, cst.RAPIDE_DEF_BONUS
        )


class Fute(RugbyPlayer):
    """Define a 'fute' player with its characteristics."""

    def __init__(self, team):
        super().__init__(
            team, cst.FUTE_MAX_MOVE, cst.FUTE_ATT_BONUS, cst.FUTE_DEF_BONUS
        )


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
        self._squares[self.length * y2 + x2].has_player(
            self._squares[self.length * y1 + x1].has_not_player()
        )


class Action:
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2


# -Déplacement -Passe -> interception => Duel -coup de pied à suivre -Marquer un essai -Plaquage (parfait) => Duel -Forcer le passage => Duel
# red à gauche blue à droite #
def front(team):
    if team == "red":
        return 1
    else:
        return -1


class Pass(Action):
    def is_possible(self, game):
        case1 = game.board(self.p1)
        case2 = game.board(self.p2)
        if case1.player is not None and case2.player is not None:
            if case1.ball == True:
                if case1.player.team == case2.player.team:
                    if abs(case1.y - case2.y) < 3:
                        if (
                            case2.x < case1.x
                            and case1.x - case2.x <= 2
                            and case1.player.team == "red"
                        ) or (
                            case1.x < case2.x
                            and case2.x - case1.x <= 2
                            and case2.player.team == "blue"
                        ):
                            return True
        return False

    def play(self, game):
        # if not(is_possible(game)) : raise Exception("can't throw")
        # if truc : interception
        game.board.move_ball(self.p1[0], self.p1[1], self.p2[0], self.p2[1])


def defender(attacker):
    if attacker == "red":
        return "blue"
    elif attacker == "blue":
        return "red"
    else:
        return "error"


def Duell(game, attacker, AskPlayer=False):
    nbr_cards = len(game.Teams[0].Cards)
    if AskPlayer:
        choix1, choix2 = 1, 1
    else:
        choix1, choix2 = rd.choices(list(range(nbr_cards)))
    carte1, carte2 = game.Teams[0].Cards.pop(choix1), game.Teams[1].Cards.pop(choix2)
    if carte1 > carte2:
        return "red"
    else:
        return "blue"


class Duel(Action):
    def play(self, game, step=0):
        attacker = game.board(self.p1).player.team
        assert attacker == game.team_playing

        nbr_cards = len(game.Teams[0].Cards)
        AskPlayer = False
        if AskPlayer:
            choix1, choix2 = 1, 1
        else:
            choix1, choix2 = rd.choices(list(range(nbr_cards)))
        carte1, carte2 = game.Teams[attacker].Cards.pop(choix1), game.Teams[
            defender(attacker)
        ].Cards.pop(choix2)
        player1 = game.board(self.p1).player
        player2 = game.board(self.p2).player
        score_att = carte1 + player1.att_bonus
        score_def = carte2 + player2.def_bonus
        if score_att > score_def:
            return (attacker, score_att, score_def)
        elif score_def > score_def:
            return (defender(attacker), score_def, score_att)
        else:
            if step >= 0:
                self.play(game, -1)
            else:
                return (defender(attacker), score_def, score_att)

    pass


class BallKick(Action):
    def is_possible(self, game):
        case1 = game.selected_case1
        case2 = game.selected_case2
        if case1.player is not None:
            if case1.ball == True:
                if abs(case1.y - case2.y) <= 3:
                    if (
                        case2.x > case1.x
                        and case2.x <= 3 + case1.x
                        and case1.player.team == "red"
                    ) or (
                        case1.x > case2.x
                        and case1.x <= 3 + case2.x
                        and case2.player.team == "blue"
                    ):
                        return True
        return False

    def play(self, game):
        game.selected_case1.ball = False
        game.selected_case2.ball = True

    pass


class Plaquage(Action):
    def play(self, game):

        duel = Duel(self.p1, self.p2)
        res = duel.play(game)
        attacker = game.team_playing
        if res[0] == attacker:
            if res[1] - res[2] >= 2:
                p_ball = self.p1
            else:
                p_ball = [self.p2[0] + front(attacker), self.p2[1]]
                if p_ball[0] < 0 or p_ball[0] > game.board.length:
                    delta_y = self.p2[0] - self.p1[0]
                    if delta_y != 0:
                        if (
                            p_ball[1] + delta_y < game.board.width
                            and p_ball[1] + delta_y >= 0
                        ):
                            p_ball[1] += delta_y
                        else:
                            p_ball[0] -= 2 * front(attacker)
                    else:
                        # choice
                        Lp = [
                            [self.p2[0], self.p2[1] + 1],
                            [self.p2[0], self.p2[1] - 1],
                        ]
                        Lp = [p for p in Lp if p[1] >= 0 and p[1] < game.board.width]
                        p_ball = rd.choice(Lp)
            game.board.move_ball(self.p2[0], self.p2[1], p_ball[0], p_ball[1])
            game.board(self.p2).player.is_stunned()
        else:
            game.board(self.p1).player.is_stunned()


# essai


class Team:
    def __init__(self, name):
        self._name = name
        self.Cards = list(range(1, 6 + 1))


class Actions:
    def __init__(self, length, width):
        self.All_moves = Init_Actions(length, width)
        self.length = length
        self.width = width
        self.List_actions = [Plaquage, Pass, BallKick]
        self.List_actions_names = ["plaquages", "passes", "ballkicks", "moves"]
        self.possible_moves = self.All_moves

    def update(self):

        for index, key in enumerate(self.List_actions):
            self.possible_moves[self.List_actions_names[index]] = [
                [[] for i in range(self.length)] for j in range(self.width)
            ]
            for i1 in range(self.length):
                for j1 in range(self.width):
                    for i2 in range(self.length):
                        for j2 in range(self.width):
                            for action in self.All_moves[str(key)][j1][i1]:
                                if action.is_possible():
                                    self.possible_moves[self.List_actions_names[index]][
                                        j1
                                    ][i1].append(action)


def Init_Actions(length, width):
    moves_dict = {}
    List_actions = [Plaquage, Pass, BallKick]
    list_action_names = ["plaquages", "passes", "ballkicks", "moves"]
    for index, key in enumerate(List_actions):
        moves_dict[list_action_names[index]] = [
            [[] for i in range(length)] for j in range(width)
        ]

        for i1 in range(length):
            for j1 in range(width):
                for i2 in range(length):
                    for j2 in range(width):
                        moves_dict[list_action_names[index]][j1][i1].append(
                            key([i1, j1], [i2, j2])
                        )
    return moves_dict


class Game:
    def __init__(self):
        self._board = Board()
        self.selected_case1 = (
            None  # could represent the rugby player who throws the ball
        )
        self.selected_case2 = None
        self.Teams = {"red": Team("red"), "blue": Team("blue")}
        self.team_playing = "red"

    @property
    def board(self):
        return self._board

    def play(self):
        # initialisation
        # ...
        win = False
        actions = Actions(self.board.length, self.board.width)
        while win == False:
            for nb_actions in range(2):
                actions.update()
                # choose move
                # make_move

            self.team_playing = defender(self.team_playing)

        pass


def test():
    player = Fute("red")
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
        print("no player")
    print(board.square(x2, y2).player.def_bonus)

    pass


test()
