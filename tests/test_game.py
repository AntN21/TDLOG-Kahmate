"""
Test for class game
"""
import unittest
import random as r
from game import Game
from constants import Teams, Actions
from tests.test_utils import get_random_coordinates

TOTAL_TESTS = 20
r.seed(1)


def get_mock_game_info():
    """Returns a mock_game and useful information to use it"""
    mock_game = Game()

    red_player_square = None
    blue_player_square = None
    for square in mock_game.board.squares:
        if square.player is not None:
            if square.player.team == Teams.RED.value:
                red_player_square = square
            if square.player.team == Teams.BLUE.value:
                blue_player_square = square
    return mock_game, red_player_square, blue_player_square


def get_duel_mock_game_info():
    """Returns a mock_game where there is a duel taking place"""
    mock_game, red_player_square, blue_player_square = get_mock_game_info()
    new_red_pos_x, new_red_pos_y = 2, 2
    new_blue_pos_x, new_blue_pos_y = 2, 3
    mock_game.board.move_player(
        red_player_square.pos_x, red_player_square.pos_y, new_red_pos_x, new_red_pos_x
    )
    mock_game.board.move_player(
        blue_player_square.pos_x,
        blue_player_square.pos_y,
        new_blue_pos_x,
        new_blue_pos_y,
    )
    mock_game.board.put_ball(new_blue_pos_x, new_blue_pos_y)

    # Pass turn two times to update actions
    mock_game.pass_turn(Teams.RED.value)
    mock_game.pass_turn(Teams.BLUE.value)

    mock_game.select_square(new_red_pos_x, new_red_pos_y, Teams.RED.value)
    mock_game.select_action(Actions.TACKLE.value, Teams.RED.value)
    mock_game.select_square(new_blue_pos_x, new_blue_pos_y, Teams.RED.value)
    return (
        mock_game,
        mock_game.board.square(new_red_pos_x, new_red_pos_y),
        mock_game.board.square(new_blue_pos_x, new_blue_pos_y),
    )


def get_available_squares(game):
    """Gets all available squares"""
    return [square for square in game.board.squares if square.available]


class TestGame(unittest.TestCase):
    """Game test class"""

    def test_init(self):
        """Tests the correct setting of the game class"""
        mock_game = Game()
        self.assertEqual(
            4,
            sum(
                1
                for square in mock_game.board.squares
                if square.player is not None and square.player.type == "ordinary"
            ),
        )
        self.assertEqual(
            2,
            sum(
                1
                for square in mock_game.board.squares
                if square.player is not None and square.player.type == "fast"
            ),
        )
        self.assertEqual(
            2,
            sum(
                1
                for square in mock_game.board.squares
                if square.player is not None and square.player.type == "tough"
            ),
        )
        self.assertEqual(
            2,
            sum(
                1
                for square in mock_game.board.squares
                if square.player is not None and square.player.type == "strong"
            ),
        )
        self.assertEqual(
            2,
            sum(
                1
                for square in mock_game.board.squares
                if square.player is not None and square.player.type == "clever"
            ),
        )
        self.assertEqual(
            6,
            sum(
                1
                for square in mock_game.board.squares
                if square.player is not None and square.player.team == Teams.RED.value
            ),
        )
        self.assertEqual(1, sum(1 for square in mock_game.board.squares if square.ball))

        self.assertEqual(Teams.RED.value, mock_game.team_playing)
        self.assertIsNone(mock_game.duel)
        self.assertIsNone(mock_game.selected_case)
        self.assertIsNone(mock_game.winner)

    def test_select_square(self):
        """Tests the different cases for the select square function"""
        mock_game, red_player_square, blue_player_square = get_mock_game_info()

        # Case not your turn
        mock_game.select_square(
            blue_player_square.pos_x, blue_player_square.pos_y, Teams.BLUE.value
        )
        self.assertFalse(blue_player_square.selected)

        # Case select player
        mock_game.select_square(
            red_player_square.pos_x, red_player_square.pos_y, Teams.RED.value
        )
        self.assertTrue(red_player_square.selected)

        # Case player selected, touching anywhere
        pos_x, pos_y = get_random_coordinates(mock_game.board)
        mock_game.select_square(pos_x, pos_y, Teams.RED.value)

        mock_game.select_square(
            red_player_square.pos_x, red_player_square.pos_y, Teams.RED.value
        )
        self.assertTrue(red_player_square.selected)

        # Case player selected, touching an available square
        player_present = red_player_square.player
        mock_game.select_action(Actions.MOVE.value, Teams.RED.value)
        available_squares = get_available_squares(mock_game)
        self.assertGreater(len(available_squares), 0)
        available_square = r.choice(available_squares)
        mock_game.select_square(
            available_square.pos_x, available_square.pos_y, Teams.RED.value
        )
        self.assertIsNone(red_player_square.player)
        self.assertEqual(player_present, available_square.player)

        # Case duel
        duel_game, red_player_square, blue_player_square = get_duel_mock_game_info()
        duel_game.select_square(
            red_player_square.pos_x, red_player_square.pos_y, Teams.RED.value
        )
        self.assertFalse(red_player_square.selected)

    def test_select_action(self):
        """Tests different cases for the select action function"""
        mock_game, red_player_square, _ = get_mock_game_info()

        # Case no square selected
        mock_game.select_action(Actions.MOVE.value, Teams.RED.value)
        available_squares = get_available_squares(mock_game)
        self.assertEqual(0, len(available_squares))

        # Case other player's turn
        mock_game.select_square(
            red_player_square.pos_x, red_player_square.pos_y, Teams.RED.value
        )
        mock_game.select_action(Actions.MOVE.value, Teams.BLUE.value)
        available_squares = get_available_squares(mock_game)
        self.assertEqual(0, len(available_squares))

        # Correct selection case
        mock_game.select_action(Actions.MOVE.value, Teams.RED.value)
        available_squares = get_available_squares(mock_game)
        self.assertGreater(len(available_squares), 0)

        # Duel case
        duel_game, red_player_square, _ = get_duel_mock_game_info()
        duel_game.select_action(Actions.MOVE.value, Teams.RED.value)
        available_squares = get_available_squares(duel_game)
        self.assertEqual(0, len(available_squares))

    def test_select_duel_card(self):
        """Tests the selection of cards for a duel"""

        # Test 1st tie and already used card
        duel_mock_game, _, _ = get_duel_mock_game_info()
        duel_mock_game.select_duel_card(1, Teams.RED.value)
        self.assertFalse(duel_mock_game.duel.is_ready())
        duel_mock_game.select_duel_card(1, Teams.BLUE.value)
        self.assertIsNotNone(duel_mock_game.duel)
        duel_mock_game.select_duel_card(1, Teams.RED.value)
        with self.assertRaises(ValueError):
            duel_mock_game.select_duel_card(1, Teams.BLUE.value)

        # Test 1st win
        duel_mock_game, _, blue_square = get_duel_mock_game_info()
        duel_mock_game.select_duel_card(2, Teams.RED.value)
        duel_mock_game.select_duel_card(1, Teams.BLUE.value)
        self.assertTrue(blue_square.player.stunned)

        # Test 2nd tie
        duel_mock_game, red_square, _ = get_duel_mock_game_info()
        duel_mock_game.select_duel_card(1, Teams.RED.value)
        duel_mock_game.select_duel_card(1, Teams.BLUE.value)
        duel_mock_game.select_duel_card(2, Teams.RED.value)
        duel_mock_game.select_duel_card(2, Teams.BLUE.value)
        self.assertTrue(red_square.player.stunned)


# def pass_turn(self, team):
#
# def to_json(self):

if __name__ == "__main__":
    unittest.main()
