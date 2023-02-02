"""
File containing the forced passage action class
"""
from constants import other
from actions.action import Action
from actions.duel import Duel
from actions.action_utils import forward, get_neighbours


class ForcedPassage(Action):
    """
    This is one of the possible actions of a player.

    When a player with the ball is next to an opponent it can opt to force its way to be able to
    go over him. For this he has to win a duel.
    """

    def is_possible(self, game):
        """
        Checks that the player in position 1 is not stunned, has the ball has enough movements
        to go over the opponent and that in the position 2 there is another player.
        """
        if (
            game.board(self.position1).player is not None
            and game.board(self.position2).player
        ):
            player1 = game.board(self.position1).player
            player2 = game.board(self.position2).player
            if player1.team != player2.team:
                if player1.available_moves > 1 and game.board(self.position1).ball:
                    if self.position2 in get_neighbours(self.position1):
                        return True
        return False

    def play(self, game):
        """
        Raises a duel if it was not already raised. If not executes the action.
        """
        if game.duel is None:
            return Duel(self.position1, self.position2)
        duel_result = game.duel.play(game)
        if duel_result is None:
            return Duel(self.position1, self.position2, -1)
        winner = duel_result[0]
        attacker = game.team_playing
        if winner == attacker:
            game.board(self.position2).player.set_stunned()
            game.board(self.position2).player.set_just_lost()
        else:
            game.board(self.position1).player.set_stunned()
            p_ball = [self.position1[0] + forward(other(attacker)), self.position1[1]]
            game.board.move_ball(
                self.position1[0], self.position1[1], p_ball[0], p_ball[1]
            )
        return game.board
