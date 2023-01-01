import math
from constants import MOVE, PASS, PLACKAGE, FORCED_PASSAGE, BALL_KICK


"""
class Action:
    def __init__(self, position1, position2):
        self._position1 = position1
        self._position2 = position2

    @property
    def position1(self):
        return self._position1

    @property
    def position2(self):
        return self._position2


# -Déplacement -Passe -> interception => Duel -coup de pied à suivre -Marquer un essai -Plaquage (parfait) => Duel -Forcer le passage => Duel
# red à gauche blue à droite #

# other file ?
def front(team):
    if team == "red":
        return 1
    else:
        return -1

def is_possible(self, game):
        case1 = game.board(self.position1)
        case2 = game.board(self.position2)
        if case1.player is not None and case2.player is not None:
            if case1.ball == True:
                if (
                    case1.player.team == case2.player.team
                    and case1.player.team == game.team_playing
                ):
                    if abs(case1.y - case2.y) < 3:
                        if (
                            0 < front(game.team_playing) * (case1.x - case2.x)
                            and front(game.team_playint) * (case1.x - case2.x - 2) <= 0
                        ):
                            return True
        return False    

def play(self, game):
        if not (self.is_possible(game)):
            raise Exception("can't throw")
        # if truc : interception
        if (
            min(
                abs(self.position1[0] - self.position2[0]),
                abs(self.position1[1] - self.position2[1]),
            )
            > 1
        ):
            inbetween = [
                self.position1[0]
                + (self.position1[0] - self.position2[0])
                / abs(self.position1[0] - self.position2[0]),
                self.position1[1]
                + (self.position1[1] - self.position2[1])
                / abs(self.position1[1] - self.position2[1]),
            ]
            if game.board(inbetween).player.team != game.team_playing:
                duel = Duel(self.position1, inbetween)
                winner = duel.play(game)[0]
                if winner != game.team_playing:
                    game.board.move_ball(
                        self.position1[0], self.position1[1], inbetween[0], inbetween[1]
                    )
                    return "interception"

        game.board.move_ball(
            self.position1[0], self.position1[1], self.position2[0], self.position2[1]
        )    


# other file ? in game class ?
def defender(attacker):
    if attacker == "red":
        return "blue"
    elif attacker == "blue":
        return "red"
    else:
        return "error"


class Duel(Action):
    def play(self, game, step=0):
        attacker = game.board(self.position1).player.team
        assert attacker == game.team_playing

        nbr_cards = len(game.Teams[0].Cards)
        AskPlayer = False
        if AskPlayer:
            (choix1, choix2) = game.controller.get_cards()
        else:
            choix1, choix2 = rd.choices(list(range(nbr_cards)))
        carte1, carte2 = game.Teams[attacker].Cards.pop(choix1), game.Teams[
            defender(attacker)
        ].Cards.pop(choix2)
        player1 = game.board(self.position1).player
        player2 = game.board(self.position2).player
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
        game.board.move_ball(
            self.position1[0], self.position1[1], self.position2[0], self.position2[1]
        )

    pass


class Plaquage(Action):
    def is_possible(self, game):
        if (
            game.board(self.position1).player is not None
            and game.board(self.position2).player
        ):
            player1 = game.board(self.position1).player
            player2 = game.board(self.position2).player
            if player1.team != player2.team:
                if path_exists(
                    player1.available_moves,
                    player1.team,
                    game.board,
                    self.position1,
                    self.position2,
                ):
                    return True
        return False

    def play(self, game):

        duel = Duel(self.position1, self.position2)
        res = duel.play(game)
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
                            p_ball[1] + delta_y < game.board.width
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
                        Lp = [p for p in Lp if p[1] >= 0 and p[1] < game.board.width]
                        p_ball = rd.choice(Lp)
            game.board.move_ball(
                self.position2[0], self.position2[1], p_ball[0], p_ball[1]
            )
            game.board(self.position2).player.is_stunned()
        else:
            game.board(self.position1).player.is_stunned()


class ForcedPassage(Action):
    def is_possible(self, game):
        if (
            game.board(self.position1).player is not None
            and game.board(self.position2).player
        ):
            player1 = game.board(self.position1).player
            player2 = game.board(self.position2).player
            if player1.team != player2.team:
                if path_exists(
                    player1.available_moves - 1,
                    player1.team,
                    game.board,
                    self.position1,
                    self.position2,
                ):
                    return True
        return False

    def play(self, game):
        duel = Duel(self.position1, self.position2)
        winner = duel.play(game)[0]
        attacker = game.team_playing
        if winner == attacker:
            game.board(self.position2).player.is_stunned()
            game.board(self.position2).player.lost()
        else:
            game.board(self.position1).player.is_stunned()


class Move(Action):
    def play(self, game):
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

    def is_possible(self, game):
        player = game.board(self.position1).player
        if player is not None:
            if player.team == game.team_playing:
                if path_exists(
                    player.available_moves,
                    player.team,
                    game.board,
                    self.position1,
                    self.position2,
                ):
                    if game.board(self.position2).player is None:
                        return True
        return False
"""

"""
def path_exists(path_length, team, board, position1, position2):
    return position2 in accessibles_cases(path_length, team, board, position1)

class Actions:
    def __init__(self, length, width):
        self.All_moves = {}

        self.length = length
        self.width = width
        self.actions = [Plaquage, Pass, BallKick]
        self.action_names = ["plaquages", "passes", "ballkicks", "moves"]

        for index, key in enumerate(self.actions):
            self.All_moves[self.action_names[index]] = [
                [[] for i in range(length)] for j in range(width)
            ]

            for i1 in range(length):
                for j1 in range(width):
                    for i2 in range(length):
                        for j2 in range(width):
                            self.All_moves[self.action_names[index]][j1][i1].append(
                                key([i1, j1], [i2, j2])
                            )
        self.possible_moves = self.All_moves

    def update(self):

        for index, key in enumerate(self.actions):
            self.possible_moves[self.action_names[index]] = [
                [[] for i in range(self.length)] for j in range(self.width)
            ]
            for i1 in range(self.length):
                for j1 in range(self.width):
                    for i2 in range(self.length):
                        for j2 in range(self.width):
                            for action in self.All_moves[str(key)][j1][i1]:
                                if action.is_possible():
                                    self.possible_moves[self.action_names[index]][j1][
                                        i1
                                    ].append(action)


def init_actions(length, width):
    moves_dict = {}
    list_actions = [Plaquage, Pass, BallKick]
    list_action_names = ["plaquages", "passes", "ballkicks", "moves"]
    for index, key in enumerate(list_actions):
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
"""

def inbound(board, pos):
    return (0 <= pos[0] < board.width and 0 <= pos[1] < board.height)

def neighbours(case):
    res = []
    for angle in [0, math.pi/2, math.pi, -math.pi/2]:
        res.append([case[0] + int(math.cos(angle)), case[1] + int(math.sin(angle))])
    return res


def accessibles_cases(path_length, team, board, position1):
    print(position1)
    acc_cases = set(tuple(i) for i in [position1])
    print(acc_cases)
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


def execute_duel(player_1, player_2, card_1, card_2):
    return player_1, player_2

def execute_action(started, from_case, to_case, selected_action):
    duel = False
    if selected_action == MOVE:
        if to_case.player is None:
            if started:
                from_case.player.move(from_case.l1_distance(to_case))
            to_case.set_player(from_case.player)
            from_case.set_player(None)

    return duel, from_case, to_case