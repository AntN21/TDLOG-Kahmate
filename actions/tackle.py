"""
File containing the tackle action class
"""
import random as rd
from actions.action import Action
from actions.duel import Duel
from actions.action_utils import get_neighbours, forward


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
        If the game was not in a duel state, it will return a Duel. It the game
        had a duel, then it will first execute along the rules and the duel result
        (containing the player that won and both player's scores)
        """
        if game.duel is None:
            return Duel(self.position1, self.position2)
        duel_results = game.duel.play(game)
        if duel_results is None:
            return Duel(self.position1, self.position2, -1)
        attacker = game.team_playing
        game.board(self.position1).player.available_moves = 0
        if duel_results[0] == attacker:
            if duel_results[1] - duel_results[2] >= 2:
                p_ball = self.position1
            else:
                p_ball = [self.position2[0] + forward(attacker), self.position2[1]]
                if p_ball[0] < 0 or p_ball[0] > game.board.width:
                    delta_y = self.position2[0] - self.position1[0]
                    if delta_y != 0:
                        if (
                            p_ball[1] + delta_y < game.board.height
                            and p_ball[1] + delta_y >= 0
                        ):
                            p_ball[1] += delta_y
                        else:
                            p_ball[0] -= 2 * forward(attacker)
                    else:
                        possible_pos = [
                            [self.position2[0], self.position2[1] + 1],
                            [self.position2[0], self.position2[1] - 1],
                        ]
                        possible_pos = [
                            p
                            for p in possible_pos
                            if p[1] >= 0 and p[1] < game.board.height
                        ]
                        p_ball = rd.choice(possible_pos)
            game.board.move_ball(
                self.position2[0], self.position2[1], p_ball[0], p_ball[1]
            )
            game.board(self.position2).player.set_stunned()
        else:
            game.board(self.position1).player.set_stunned()

        return game.board
