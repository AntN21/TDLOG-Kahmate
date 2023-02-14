"""
Test for class square
"""
import unittest
import random as r
from constants import BOARD_WIDTH, BOARD_HEIGHT, Teams
from square import Square
from players.ordinary import Ordinary

r.seed(1)
mock_player = Ordinary(Teams.RED)


def get_mock_square():
    """Returns a mock square"""
    return Square(r.randint(0, BOARD_WIDTH), r.randint(0, BOARD_HEIGHT))


class TestSquare(unittest.TestCase):
    """Square test class"""

    def test_set_ball(self):
        """set ball test"""
        mock_square = get_mock_square()
        self.assertFalse(mock_square.ball)
        mock_square.set_ball(True)
        self.assertTrue(mock_square.ball)
        mock_square.set_ball(False)
        self.assertFalse(mock_square.ball)

    def test_set_player(self):
        """set player test"""
        mock_square = get_mock_square()
        self.assertIsNone(mock_square.player)
        mock_square.set_player(mock_player)
        self.assertEqual(mock_player, mock_square.player)

    def test_set_available(self):
        """set available test"""
        mock_square = get_mock_square()
        self.assertFalse(mock_square.available)
        mock_square.set_available(True)
        self.assertTrue(mock_square.available)
        mock_square.set_available(False)
        self.assertFalse(mock_square.available)

    def test_set_selected(self):
        """set selected test"""
        mock_square = get_mock_square()
        self.assertFalse(mock_square.selected)
        mock_square.set_selected(True)
        self.assertTrue(mock_square.selected)
        mock_square.set_selected(False)
        self.assertFalse(mock_square.selected)

    def test_remove_player(self):
        """remove player test"""
        mock_square = get_mock_square()
        mock_square.set_player(mock_player)
        returned_player = mock_square.remove_player()
        self.assertEqual(mock_player, returned_player)
        self.assertIsNone(mock_square.player)


if __name__ == "__main__":
    unittest.main()
