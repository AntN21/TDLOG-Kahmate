"""
File containing the ActionManager
"""
from actions.tackle import Tackle
from actions.ball_kick import BallKick
from actions.forced_passage import ForcedPassage
from actions.move import Move
from actions.ball_pass import Pass
import copy
from actions.action_utils import forward
from constants import Actions, other


class ActionManager:
    def __init__(self, length, width):
        self.all_moves = {}

        self.length = length
        self.width = width
        self.actions = [Tackle, ForcedPassage, Pass, BallKick, Move]
        self.action_names = [
            Actions.TACKLE.value,
            Actions.FORCED_PASSAGE.value,
            Actions.PASS.value,
            Actions.BALL_KICK.value,
            Actions.MOVE.value,
        ]

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
