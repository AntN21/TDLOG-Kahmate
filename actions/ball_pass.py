"""
File containing the pass action class
"""
from actions.action import Action
from actions.action_utils import forward


class Pass(Action):
    """
    This is one of the possible actions of a player.

    It represents passing the ball from the current holder to another team member
    at a distance of at most 2 squares behind the player.
    """

    def is_possible(self, game):
        """
        Checks if the current player has the ball and in position 2 there is a
        player of the same team.
        """
        case1 = game.board(self.position1)
        case2 = game.board(self.position2)
        if case1.ball and case1.player is not None and case2.player is not None:
            if (
                case1.player.team == case2.player.team
                and case1.player.team == game.team_playing
            ):
                if (
                    abs(case1.pos_y - case2.pos_y) < 3
                    and 0
                    < forward(game.team_playing) * (case1.pos_x - case2.pos_x)
                    <= 2
                ):
                    return True

        return False

    def play(self, game):
        """
        Moves the ball from position 1 to position 2
        """
        game.board.move_ball(
            self.position1[0], self.position1[1], self.position2[0], self.position2[1]
        )
        return game.board
