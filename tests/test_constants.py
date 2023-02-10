"""
Test for the methods in the constants file
"""
import unittest
from constants import Teams, BOARD_WIDTH, other, get_goal


class TestConstants(unittest.TestCase):
    """Tests for the two functions of the constants file"""

    def test_other(self):
        """other function test"""
        self.assertEqual(Teams.BLUE.value, other(Teams.RED.value))
        self.assertEqual(Teams.RED.value, other(Teams.BLUE.value))
        self.assertIsNone(other("Other"))

    def test_get_goal(self):
        """get goal function test"""
        self.assertEqual(0, get_goal(Teams.BLUE.value))
        self.assertEqual(BOARD_WIDTH - 1, get_goal(Teams.RED.value))


if __name__ == "__main__":
    unittest.main()
