import math
import random as rd
import copy
from constants import MOVE, PASS, PLACKAGE, FORCED_PASSAGE, BALL_KICK


class Action:
    """
    Represent th differents actions.
    It has two parameters which are lists of 2 ints representing squares:
        -position1 represents the square from which the action is done
        -position2 represents the square targeted by the action
    """

    def __init__(self, position1, position2):
        self._position1 = position1
        self._position2 = position2

    @property
    def position1(self):
        """Return the position of origin"""
        return self._position1

    @property
    def position2(self):
        """Return the targeted position"""
        return self._position2

    def toJSON(self):
        res = {}
        res["position_1"] = self.position1
        res["position_2"] = self.position2
        return res


# -Déplacement -Passe -> interception => Duel -coup de pied à suivre -Marquer un essai -Plaquage (parfait) => Duel -Forcer le passage => Duel
# red à gauche blue à droite #

# other file ?
def front(team):
    return 1 if team == "red" else -1


class Pass(Action):
    """Represent the action of pass."""

    def is_possible(self, game):
        case1 = game.board(self.position1)
        case2 = game.board(self.position2)
        if case1.ball and case1.player is not None and case2.player is not None:
            if (
                case1.player.team == case2.player.team
                and case1.player.team == game.team_playing
            ):
                if (
                    abs(case1.y - case2.y) < 3
                    and 0 < front(game.team_playing) * (case1.x - case2.x) <= 2
                ):
                    return True

        return False

    def play(self, game):
        if not (self.is_possible(game)):
            raise Exception("can't throw")
        game.board.move_ball( self.position1[0], self.position1[1], self.position2[0], self.position2[1])
        return game.board


# other file ? in game class ?
def defender(attacker):
    if attacker == "red":
        return "blue"
    elif attacker == "blue":
        return "red"
    else:
        return "error"


class Duel(Action):
    """Represent a duel"""

    def __init__(self, position1, position2, step=0):
        super().__init__(position1, position2)
        self.attacker_choice = None
        self.defender_choice = None
        self.step = step

    def choose_card(self, game, card, team):
        if team == game.board(self.position1).player.team:
            self.attacker_choice = card
        else:
            self.defender_choice = card

    def is_ready(self):
        return self.attacker_choice is not None and self.defender_choice is not None

    def play(self, game):
        # TODO: HERE MAKING "POP" is not correct, you empty the list. Fix this bug
        attacker = game.board(self.position1).player.team
        assert attacker == game.team_playing
        card1, card2 = self.attacker_choice, self.defender_choice
        game.teams[attacker].cards.remove(self.attacker_choice)
        game.teams[defender(attacker)].cards.remove(self.defender_choice)
        if len(game.teams[attacker].cards) == 0:
            game.teams[attacker].cards = list(range(1, 6 + 1))
            game.teams[defender(attacker)].cards = list(range(1, 6 + 1))
        player1 = game.board(self.position1).player
        player2 = game.board(self.position2).player
        score_att = card1 + player1.att_bonus
        score_def = card2 + player2.def_bonus
        if score_att > score_def:
            return (attacker, score_att, score_def)
        elif score_def > score_att:
            return (defender(attacker), score_def, score_att)
        else:
            if self.step >= 0:
                return None
            else:
                return (defender(attacker), score_def, score_att)

def in_front(board,position):
    team=board(position).player.team
    for x in range(position[0]+front(team),max(0,board.width*front(team)),front(team)):
        for y in range(board.height):
            if board.square(x,y).player is not None:
                if board.square(x,y).player.team==team:
                    return False
    return True

class BallKick(Action):
    """Represent a ballkick"""

    def is_possible(self, game):
        square1 = game.board(self.position1)
        player = square1.player
        if (
            square1.player is not None
            and square1.ball
            and player.team == game.team_playing
        ):
            # TODO: We need to check that he is the player in front!!!
            if in_front(game.board,self.position1):
                if abs(self.position2[1]-self.position1[1]) <= 3:
                    if (self.position2[0]-self.position1[0])*front(player.team) <=3 and (self.position2[0]-self.position1[0])*front(player.team) >=1:
                        return True
        return False

    def play(self, game):
        game.board.move_ball(
            self.position1[0], self.position1[1], self.position2[0], self.position2[1]
        )
        return game.board


class Plaquage(Action):
    def is_possible(self, game):
        if (
            game.board(self.position1).player is not None
            and game.board(self.position2).player is not None
        ):
            player1 = game.board(self.position1).player
            player2 = game.board(self.position2).player
            if (
                game.board(self.position2).ball
                and not player1.stunned
                and player1.team != player2.team
            ):
                if self.position2 in neighbours(self.position1):
                    return True
        return False

    def play(self, game):
        if game.duel is None:
            return Duel(self.position1, self.position2)
        res = game.duel.play(game)
        if res is None:
            return Duel(self.position1, self.position2, -1)
        attacker = game.team_playing
        if res[0] == attacker:
            if res[1] - res[2] >= 2:
                p_ball = self.position1
            else:
                p_ball = [self.position2[0] + front(attacker), self.position2[1]]
                if p_ball[0] < 0 or p_ball[0] > game.board.width:
                    delta_y = self.position2[0] - self.position1[0]
                    if delta_y != 0:
                        if (
                            p_ball[1] + delta_y < game.board.height
                            and p_ball[1] + delta_y >= 0
                        ):
                            p_ball[1] += delta_y
                        else:
                            p_ball[0] -= 2 * front(attacker)
                    else:
                        # choice
                        Lp = [
                            [self.position2[0], self.position2[1] + 1],
                            [self.position2[0], self.position2[1] - 1],
                        ]
                        Lp = [p for p in Lp if p[1] >= 0 and p[1] < game.board.height]
                        p_ball = rd.choice(Lp)
            game.board.move_ball(
                self.position2[0], self.position2[1], p_ball[0], p_ball[1]
            )
            game.board(self.position2).player.set_stunned()
        else:
            game.board(self.position1).player.set_stunned()

        return game.board


# In English
class PassageEnForce(Action):
    def is_possible(self, game):
        if (
            game.board(self.position1).player is not None
            and game.board(self.position2).player
        ):
            player1 = game.board(self.position1).player
            player2 = game.board(self.position2).player
            if player1.team != player2.team:
                if player1.available_moves>1 and game.board(self.position1).ball:
                    if self.position2 in neighbours(self.position1):
                        return True
        return False

    def play(self, game):
        if game.duel is None:
            return Duel(self.position1, self.position2)
        res = game.duel.play(game)
        if res is None:
            return Duel(self.position1, self.position2, -1)
        winner = res[0]
        attacker = game.team_playing
        if winner == attacker:
            game.board(self.position2).player.set_stunned()
            game.board(self.position2).player.lost()
        else:
            game.board(self.position1).player.set_stunned()
            p_ball = [self.position1[0] + front(defender), self.position1[1]]
            game.board.move_ball(
                self.position1[0], self.position1[1], p_ball[0], p_ball[1]
            )
        return game.board


class Move(Action):
    # TODO: It should diminish the player's available moves, and check if it is stunned and can move
    # (Fix this for all actions, because there is no check for stunned players, and add the 2 moves per
    # turn)
    def play(self, game):
        player = game.board.square(self.position1[0], self.position1[1]).player
        if player not in game.teams[game.team_playing].players_moved:
            game.teams[game.team_playing].players_moved.append(player)
        player.available_moves -= abs(self.position1[0] - self.position2[0]) + abs(
            self.position1[1] - self.position2[1]
        )

        if game.board(self.position1).ball:
            game.board.move_ball(
                self.position1[0],
                self.position1[1],
                self.position2[0],
                self.position2[1],
            )
        game.board.move_player(
            self.position1[0], self.position1[1], self.position2[0], self.position2[1]
        )

        return game.board

    def is_possible(self, game):
        player = game.board(self.position1).player
        has_ball = game.board(self.position1).ball
        if player is not None:
            if player.team == game.team_playing:
                if (
                    player in game.teams[game.team_playing].players_moved
                    or len(game.teams[game.team_playing].players_moved) < 2
                ):
                    if not (player.stunned) and player.available_moves > 0:
                        if path_exists(
                            player.available_moves,
                            player.team,
                            game.board,
                            self.position1,
                            self.position2,
                        ):
                            (goal, back) = (game.board.width-1, 0) if game.team_playing == "red" else (0, game.board.width-1)
                            if (
                                game.board(self.position2).player is None
                                and not self.position2[0] == back
                                and (
                                    (self.position2[0] == goal and has_ball)
                                    or not self.position2[0] == goal
                                )
                            ):
                                return True
        return False


def path_exists(path_length, team, board, position1, position2):
    return tuple(position2) in accessibles_cases(path_length, team, board, position1)


def inbound(board, pos):
    return 0 <= pos[0] < board.width and 0 <= pos[1] < board.height


class Actions:
    def __init__(self, length, width):
        self.all_moves = {}

        self.length = length
        self.width = width
        self.actions = [Plaquage, PassageEnForce, Pass, BallKick, Move]
        self.action_names = [PLACKAGE, FORCED_PASSAGE, PASS, BALL_KICK, MOVE]

        for index, key in enumerate(self.actions):
            self.all_moves[self.action_names[index]] = [
                [[] for i in range(length)] for j in range(width)
            ]
            for i1 in range(length):
                for j1 in range(width):
                    for i2 in range(length):
                        for j2 in range(width):
                            self.all_moves[self.action_names[index]][j1][i1].append(
                                key([i1, j1], [i2, j2])
                            )
        self.possible_moves = copy.copy(self.all_moves)

    def update(self, game):
        for index, key in enumerate(self.actions):
            self.possible_moves[self.action_names[index]] = [
                [[] for i in range(self.length)] for j in range(self.width)
            ]
            for i1 in range(self.length):
                for j1 in range(self.width):
                    for action in self.all_moves[self.action_names[index]][j1][i1]:
                        if action.is_possible(game):
                            self.possible_moves[self.action_names[index]][j1][
                                i1
                            ].append(action)


def neighbours(case):
    res = []
    for angle in [0, math.pi / 2, math.pi, -math.pi / 2]:
        res.append([case[0] + int(math.cos(angle)), case[1] + int(math.sin(angle))])
    return res


def accessibles_cases(path_length, team, board, position1):
    # TODO: This function does not work correctly some times, find the bugs
    acc_cases = set(tuple(i) for i in [position1])
    new_cases = []
    for iter in range(path_length):
        for new_case in new_cases:
            acc_cases.add(new_case)
        new_cases = []
        for case in acc_cases:
            for n_case in neighbours(case):
                if inbound(board, n_case):
                    player = board(n_case).player
                    if player is None or player.has_just_lost():
                        new_cases.append(tuple(n_case))
    return new_cases
