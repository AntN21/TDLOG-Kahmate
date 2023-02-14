"""
File containing the move action class
"""
from constants import Teams, get_goal
from actions.action import Action
from actions.action_utils import path_exists


class Move(Action):
    """
    This is one of the possible actions of a player.

    Allows a player to move (carring the ball if they have it) to another
    square within its available_moves limit
    """

    def play(self, game):
        """
        Executes the action, traslating the player from position 1 to position 2 (the
        ball with them if it is the case)
        """
        player = game.board.square(self.position1[0], self.position1[1]).player
        if player not in game.teams[game.team_playing].players_moved:
            game.teams[game.team_playing].players_moved.append(player)
        player.reduce_moves(
            abs(self.position1[0] - self.position2[0])
            + abs(self.position1[1] - self.position2[1])
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
        """
        Checks that the position 1 contains a ready-to-move player and that position
        2 is inside its limits and without a player on it.
        """
        current_team = game.teams[game.team_playing]
        player = game.board(self.position1).player
        has_ball = game.board(self.position1).ball
        goal = get_goal(game.team_playing)
        back = get_goal(Teams.RED.other(game.team_playing))

        if player is None or player.team != game.team_playing or player.stunned:
            return False
        if (
            player not in current_team.players_moved
            and len(current_team.players_moved) == 2
        ):
            return False
        if game.board(self.position2).player is not None:
            return False
        if self.position2[0] == back or (self.position2[0] == goal and not has_ball):
            return False
        if path_exists(
            player.available_moves, game.board, self.position1, self.position2
        ):
            return True
        return False
