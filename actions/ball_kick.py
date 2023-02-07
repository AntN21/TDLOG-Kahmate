"""
File containing the ball kick class
"""
from actions.action import Action
from actions.action_utils import forward, move_ball


def in_front(board, position):
    """
    Checks that the player is the most advanced one of his team.
    """
    team = board(position).player.team
    for row in range(
        position[0] + forward(team), max(0, board.width * forward(team)), forward(team)
    ):
        for col in range(board.height):
            if board.square(row, col).player is not None:
                if board.square(row, col).player.team == team:
                    return False
    return True


class BallKick(Action):
    """
    This is one of the possible actions of a player.

    A player holding the ball can send it in front of him if he is the one most advanced
    of their team.
    """

    def is_possible(self, game):
        """
        Checks if the position 1 is the most advanced player of the team, has the ball
        and the position 2 is a certain distance from them.
        """
        square1 = game.board(self.position1)
        player = square1.player
        if (
            square1.player is not None
            and square1.ball
            and player.team == game.team_playing
        ):
            if in_front(game.board, self.position1):
                if (
                    abs(self.position2[1] - self.position1[1]) <= 3
                    and self.position2[0] < 12
                    and self.position2[0] > 0
                ):
                    if (self.position2[0] - self.position1[0]) * forward(
                        player.team
                    ) <= 3 and (self.position2[0] - self.position1[0]) * forward(
                        player.team
                    ) >= 1:
                        return True
        return False

    def play(self, game):
        """
        Executes a ball kick
        """
        return move_ball(game, self.position1, self.position2)
