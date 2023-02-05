"""
File containing the ActionManager
"""
import copy
from constants import Actions
from actions.tackle import Tackle
from actions.ball_kick import BallKick
from actions.forced_passage import ForcedPassage
from actions.move import Move
from actions.ball_pass import Pass


class ActionManager:
    """
    This class generates an array with all the possible actions that can be executed given a
    current game state.
    """
    def __init__(self, width, height):
        self.all_moves = {}

        self.width = width
        self.height = height
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
                [[] for i in range(width)] for j in range(height)
            ]
            for pos_1_x in range(width):
                for pos_1_y in range(height):
                    for pos_2_x in range(width):
                        for pos_2_y in range(height):
                            self.all_moves[self.action_names[index]][pos_1_y][pos_1_x].append(
                                key([pos_1_x, pos_1_y], [pos_2_x, pos_2_y])
                            )
        self.possible_moves = copy.copy(self.all_moves)

    def update(self, game):
        """
        Updates the possible moves matrix from the game state.
        """
        for index in range(len(self.actions)):
            self.possible_moves[self.action_names[index]] = [
                [[] for i in range(self.width)] for j in range(self.height)
            ]
            for pos_1_x in range(self.width):
                for pos_1_y in range(self.height):
                    for action in self.all_moves[self.action_names[index]][pos_1_y][pos_1_x]:
                        if action.is_possible(game):
                            self.possible_moves[self.action_names[index]][pos_1_y][
                                pos_1_x
                            ].append(action)

    def get_possible_moves(self):
        """
        Returns an array with dictionaries for all possible moves.
        """
        moves_dict = []
        for action_type in self.possible_moves:
            for initial_line in self.possible_moves[action_type]:
                for initial_square in initial_line:
                    for possible_action in initial_square:
                        action_json = {}
                        action_json["type"] = action_type
                        action_json["position_1"] = possible_action.position1
                        action_json["position_2"] = possible_action.position2
                        moves_dict.append(action_json)
        return moves_dict
