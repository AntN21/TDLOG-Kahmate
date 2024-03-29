"""
File containing the tackle action class
"""
import random as rd
from actions.action import Action
from actions.duel import Duel
from actions.action_utils import get_neighbours, forward, check_duel


class Tackle(Action):
    """
    This is one of the possible actions of a player.

    It happens when a non-stunned player without a ball is next to an
    opposite player with the ball.

    It generates a duel, if the attacking player wins by a 2 margin it steals the ball
    directly, if he wins without a big margin the defending player loses the ball behind
    him or to the sides if he is in the last row. The player that loses gets stunned for
    two turns.
    """

    def is_possible(self, game):
        """
        Checks if there is a non-stunned player in position 1 and an opposite team player
        with the ball in a neighbouring square
        """
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
                if self.position2 in get_neighbours(self.position1):
                    return True
        return False

    def play(self, game):
        """
        Executes tackle action or loads the duel.
        """
        duel_results = check_duel(
            game,
            self.position1,
            self.position2,
        )
        if isinstance(duel_results, Duel):
            return duel_results
        winner = duel_results[0]
        defense_score = duel_results[1]
        attack_score = duel_results[2]
        attacker = game.team_playing
        game.board(self.position1).player.available_moves = 0
        if winner == attacker:
            if defense_score - attack_score >= 2:
                p_ball = self.position1
            else:
                p_ball = [self.position2[0] + forward(attacker), self.position2[1]]
                if p_ball[0] < 0 or p_ball[0] > game.board.width:
                    delta_y = self.position2[0] - self.position1[0]
                    if delta_y != 0:
                        if game.board.height > p_ball[1] + delta_y >= 0:
                            p_ball[1] += delta_y
                        else:
                            p_ball[0] -= 2 * forward(attacker)
                    else:
                        possible_pos = [
                            [self.position2[0], self.position2[1] + 1],
                            [self.position2[0], self.position2[1] - 1],
                        ]
                        possible_pos = [
                            p for p in possible_pos if 0 <= p[1] < game.board.height
                        ]
                        p_ball = rd.choice(possible_pos)
            game.board.move_ball(
                self.position2[0], self.position2[1], p_ball[0], p_ball[1]
            )
            game.board(self.position2).player.set_stunned()
        else:
            game.board(self.position1).player.set_stunned()

        return game.board
