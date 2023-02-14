"""
Test for class game
"""
import unittest
import random as r
import json
from game import Game
from constants import Teams, Actions, PlayerType
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
            if square.player.team == Teams.RED:
                red_player_square = square
            if square.player.team == Teams.BLUE:
                blue_player_square = square
    return mock_game, red_player_square, blue_player_square


def get_confronted_players_mock_game_info():
    """Returns a mock_game where two players are facing each other with
    their two squares"""
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
    return (
        mock_game,
        mock_game.board.square(new_red_pos_x, new_red_pos_x),
        mock_game.board.square(new_blue_pos_x, new_blue_pos_y),
    )


def get_tackle_duel_mock_game_info():
    """Returns a mock_game where there is a tackle duel taking place"""
    (
        mock_game,
        red_player_square,
        blue_player_square,
    ) = get_confronted_players_mock_game_info()
    mock_game.board.put_ball(blue_player_square.pos_x, blue_player_square.pos_y)

    # Pass turn two times to update actions
    mock_game.pass_turn(Teams.RED)
    mock_game.pass_turn(Teams.BLUE)

    mock_game.select_square(
        red_player_square.pos_x, red_player_square.pos_y, Teams.RED
    )
    mock_game.select_action(Actions.TACKLE.value, Teams.RED)
    mock_game.select_square(
        blue_player_square.pos_x, blue_player_square.pos_y, Teams.RED
    )
    return mock_game, red_player_square, blue_player_square


def get_forced_passage_duel_mock_game_info():
    """Returns a mock_game where there is a forced passage duel taking place"""
    (
        mock_game,
        red_player_square,
        blue_player_square,
    ) = get_confronted_players_mock_game_info()
    mock_game.board.put_ball(red_player_square.pos_x, red_player_square.pos_y)

    # Pass turn two times to update actions
    mock_game.pass_turn(Teams.RED)
    mock_game.pass_turn(Teams.BLUE)

    mock_game.select_square(
        red_player_square.pos_x, red_player_square.pos_y, Teams.RED
    )
    mock_game.select_action(Actions.FORCED_PASSAGE.value, Teams.RED)
    mock_game.select_square(
        blue_player_square.pos_x, blue_player_square.pos_y, Teams.RED
    )
    return mock_game, red_player_square, blue_player_square


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
                if square.player is not None and square.player.type == PlayerType.ORDINARY
            ),
        )
        self.assertEqual(
            2,
            sum(
                1
                for square in mock_game.board.squares
                if square.player is not None and square.player.type == PlayerType.FAST
            ),
        )
        self.assertEqual(
            2,
            sum(
                1
                for square in mock_game.board.squares
                if square.player is not None and square.player.type == PlayerType.TOUGH
            ),
        )
        self.assertEqual(
            2,
            sum(
                1
                for square in mock_game.board.squares
                if square.player is not None and square.player.type == PlayerType.STRONG
            ),
        )
        self.assertEqual(
            2,
            sum(
                1
                for square in mock_game.board.squares
                if square.player is not None and square.player.type == PlayerType.CLEVER
            ),
        )
        self.assertEqual(
            6,
            sum(
                1
                for square in mock_game.board.squares
                if square.player is not None and square.player.team == Teams.RED
            ),
        )
        self.assertEqual(1, sum(1 for square in mock_game.board.squares if square.ball))

        self.assertEqual(Teams.RED, mock_game.team_playing)
        self.assertIsNone(mock_game.duel)
        self.assertIsNone(mock_game.selected_case)
        self.assertIsNone(mock_game.winner)

    def test_select_square(self):
        """Tests the different cases for the select square function"""
        mock_game, red_player_square, blue_player_square = get_mock_game_info()

        # Case not your turn
        mock_game.select_square(
            blue_player_square.pos_x, blue_player_square.pos_y, Teams.BLUE
        )
        self.assertFalse(blue_player_square.selected)

        # Case select player
        mock_game.select_square(
            red_player_square.pos_x, red_player_square.pos_y, Teams.RED
        )
        self.assertTrue(red_player_square.selected)

        # Case player selected, touching anywhere
        pos_x, pos_y = get_random_coordinates(mock_game.board)
        mock_game.select_square(pos_x, pos_y, Teams.RED)

        mock_game.select_square(
            red_player_square.pos_x, red_player_square.pos_y, Teams.RED
        )
        self.assertTrue(red_player_square.selected)

        # Case player selected, touching an available square
        player_present = red_player_square.player
        mock_game.select_action(Actions.MOVE.value, Teams.RED)
        available_squares = get_available_squares(mock_game)
        self.assertGreater(len(available_squares), 0)
        available_square = r.choice(available_squares)
        mock_game.select_square(
            available_square.pos_x, available_square.pos_y, Teams.RED
        )
        self.assertIsNone(red_player_square.player)
        self.assertEqual(player_present, available_square.player)

        # Case duel
        (
            duel_game,
            red_player_square,
            blue_player_square,
        ) = get_tackle_duel_mock_game_info()
        duel_game.select_square(
            red_player_square.pos_x, red_player_square.pos_y, Teams.RED
        )
        self.assertFalse(red_player_square.selected)

    def test_select_action(self):
        """Tests different cases for the select action function"""
        mock_game, red_player_square, _ = get_mock_game_info()

        # Case no square selected
        mock_game.select_action(Actions.MOVE.value, Teams.RED)
        available_squares = get_available_squares(mock_game)
        self.assertEqual(0, len(available_squares))

        # Case other player's turn
        mock_game.select_square(
            red_player_square.pos_x, red_player_square.pos_y, Teams.RED
        )
        mock_game.select_action(Actions.MOVE.value, Teams.BLUE)
        available_squares = get_available_squares(mock_game)
        self.assertEqual(0, len(available_squares))

        # Correct selection case
        mock_game.select_action(Actions.MOVE.value, Teams.RED)
        available_squares = get_available_squares(mock_game)
        self.assertGreater(len(available_squares), 0)

        # Duel case
        duel_game, red_player_square, _ = get_tackle_duel_mock_game_info()
        duel_game.select_action(Actions.MOVE.value, Teams.RED)
        available_squares = get_available_squares(duel_game)
        self.assertEqual(0, len(available_squares))

    def test_select_duel_card(self):
        """Tests the selection of cards for a duel"""

        # Test 1st tie and already used card
        duel_mock_game, _, _ = get_tackle_duel_mock_game_info()
        duel_mock_game.select_duel_card(1, Teams.RED)
        self.assertFalse(duel_mock_game.duel.is_ready())
        duel_mock_game.select_duel_card(1, Teams.BLUE)
        self.assertIsNotNone(duel_mock_game.duel)
        duel_mock_game.select_duel_card(1, Teams.RED)
        with self.assertRaises(ValueError):
            duel_mock_game.select_duel_card(1, Teams.BLUE)

        # Test 1st win
        duel_mock_game, _, blue_square = get_tackle_duel_mock_game_info()
        duel_mock_game.select_duel_card(2, Teams.RED)
        duel_mock_game.select_duel_card(1, Teams.BLUE)
        self.assertTrue(blue_square.player.stunned)

        # Test 2nd tie
        duel_mock_game, red_square, _ = get_tackle_duel_mock_game_info()
        duel_mock_game.select_duel_card(1, Teams.RED)
        duel_mock_game.select_duel_card(1, Teams.BLUE)
        duel_mock_game.select_duel_card(2, Teams.RED)
        duel_mock_game.select_duel_card(2, Teams.BLUE)
        self.assertTrue(red_square.player.stunned)

    def test_pass_turn(self):
        """Pass turn function test"""
        mock_game, red_player_square, blue_player_square = get_mock_game_info()

        # Test other team's turn
        mock_game.select_square(
            red_player_square.pos_x, red_player_square.pos_y, Teams.RED
        )
        self.assertTrue(red_player_square.selected)
        mock_game.pass_turn(Teams.BLUE)
        self.assertTrue(red_player_square.selected)

        # Test resets moves
        mock_game.select_action(Actions.MOVE.value, Teams.RED)
        target_square = r.choice(get_available_squares(mock_game))
        mock_game.select_square(
            target_square.pos_x, target_square.pos_y, Teams.RED
        )
        self.assertNotEqual(
            target_square.player.available_moves, target_square.player.max_move
        )
        mock_game.pass_turn(Teams.RED)
        self.assertEqual(
            target_square.player.available_moves, target_square.player.max_move
        )

        # Test cleans availables and selected squares
        mock_game.select_square(
            blue_player_square.pos_x, blue_player_square.pos_y, Teams.BLUE
        )
        mock_game.select_action(Actions.MOVE.value, Teams.BLUE)
        self.assertGreater(len(get_available_squares(mock_game)), 0)
        self.assertTrue(blue_player_square.selected)
        mock_game.pass_turn(Teams.BLUE)
        self.assertEqual(0, len(get_available_squares(mock_game)))
        self.assertFalse(blue_player_square.selected)

        # Test cleans stunned and lost states
        duel_mock_game, _, blue_square = get_forced_passage_duel_mock_game_info()
        duel_mock_game.select_duel_card(2, Teams.RED)
        duel_mock_game.select_duel_card(1, Teams.BLUE)
        self.assertTrue(blue_square.player.stunned)
        self.assertTrue(blue_square.player.get_just_lost())
        duel_mock_game.pass_turn(Teams.RED)
        self.assertTrue(blue_square.player.stunned)
        duel_mock_game.pass_turn(Teams.BLUE)
        self.assertFalse(blue_square.player.get_just_lost())
        duel_mock_game.pass_turn(Teams.RED)
        self.assertFalse(blue_square.player.stunned)

    def test_to_json(self):
        """Tests if the json was correctly created"""
        mock_game, _, _ = get_mock_game_info()
        mock_game_json = json.loads(mock_game.to_json())
        self.assertEqual(mock_game_json["team_playing"], Teams.RED.value)
        self.assertEqual(
            len(mock_game_json["board"]),
            mock_game.board.width * mock_game.board.height,
        )
        self.assertGreater(len(mock_game_json["actions"]), 0)
        self.assertIsNone(mock_game_json["duel"])
        self.assertIsNone(mock_game_json["winner"])
        self.assertEqual(mock_game_json["team_red"], mock_game_json["team_blue"])
        self.assertEqual(len(mock_game_json["team_red"]["cards"]), 6)


if __name__ == "__main__":
    unittest.main()
