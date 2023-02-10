"""
Test for class board
"""
import unittest
import random as r
from board import Board
from constants import Teams
from players.ordinary import Ordinary

TOTAL_TESTS = 20
r.seed(1)

def get_mock_player():
    """Returns a mock player"""
    return Ordinary(Teams.RED.value)

def get_random_coordinates_set(board, size):
    """Gets an array of random pair coordinates"""
    return [(get_random_coordinates(board)) for _ in range(size)]


def get_random_coordinates(board):
    """Gets a random pair of coordinates to test a function"""
    x_square = r.randint(0, board.width - 1)
    y_square = r.randint(0, board.height - 1)
    return x_square, y_square

class TestBoard(unittest.TestCase):
    """Board test class"""

    def test_put_ball(self):
        """put ball test"""
        for _ in range(TOTAL_TESTS):
            board = Board()
            x_square, y_square = get_random_coordinates(board)
            self.assertFalse(board.square(x_square,y_square).ball)
            board.put_ball(x_square, y_square)
            self.assertTrue(board.square(x_square,y_square).ball)

    def test_put_player(self):
        """put player test"""
        mock_player = get_mock_player()
        for _ in range(TOTAL_TESTS):
            board = Board()
            x_square, y_square = get_random_coordinates(board)
            self.assertIsNone(board.square(x_square,y_square).player)
            board.put_player(mock_player, x_square, y_square)
            self.assertEqual(mock_player, board.square(x_square,y_square).player)

    def test_clear_selected(self):
        """clear selected test"""
        board = Board()
        coordinates = get_random_coordinates_set(board, TOTAL_TESTS)
        for coordinate in coordinates:
            board.square(coordinate[0], coordinate[1]).set_selected(True)
            self.assertTrue(board.square(coordinate[0], coordinate[1]).selected)
        board.clear_selected()
        for coordinate in coordinates:
            self.assertFalse(board.square(coordinate[0], coordinate[1]).selected)

    def test_clear_available(self):
        """clear available test"""
        board = Board()
        coordinates = get_random_coordinates_set(board, TOTAL_TESTS)
        for coordinate in coordinates:
            board.square(coordinate[0], coordinate[1]).set_available(True)
            self.assertTrue(board.square(coordinate[0], coordinate[1]).available)
        board.clear_available()
        for coordinate in coordinates:
            self.assertFalse(board.square(coordinate[0], coordinate[1]).available)

    def test_move_ball(self):
        """Move ball test"""
        board = Board()
        from_coordinates = get_random_coordinates_set(board, TOTAL_TESTS)
        to_coordinates = get_random_coordinates_set(board, TOTAL_TESTS)
        for index, from_coordinate in enumerate(from_coordinates):
            board = Board()
            to_coordinate = to_coordinates[index]
            board.put_ball(from_coordinate[0], from_coordinate[1])
            board.move_ball(from_coordinate[0], from_coordinate[1],
                            to_coordinate[0], to_coordinate[1])
            self.assertTrue(board.square(to_coordinate[0], to_coordinate[1]).ball)


    def test_move_player(self):
        "move player test"
        board = Board()
        from_coordinates = get_random_coordinates_set(board, TOTAL_TESTS)
        to_coordinates = get_random_coordinates_set(board, TOTAL_TESTS)
        for index, from_coordinate in enumerate(from_coordinates):
            board = Board()
            mock_player = get_mock_player()
            to_coordinate = to_coordinates[index]
            board.put_player(mock_player, from_coordinate[0], from_coordinate[1])
            board.move_player(from_coordinate[0], from_coordinate[1],
                            to_coordinate[0], to_coordinate[1])
            self.assertEqual(mock_player,
            board.square(to_coordinate[0], to_coordinate[1]).player)

if __name__ == "__main__":
    unittest.main()
