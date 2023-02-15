"""
Test for the methods in the constants file
"""
import unittest
from constants import Teams, BOARD_WIDTH, other, get_goal


class TestConstants(unittest.TestCase):
    """Tests for the two functions of the constants file"""

    def test_other(self):
        """other function test"""
        self.assertEqual(Teams.BLUE, Teams.RED.other(Teams.RED))
        self.assertEqual(Teams.RED, Teams.RED.other(Teams.BLUE))
        self.assertIsNone(other("Other"))

    def test_get_goal(self):
        """get goal function test"""
        self.assertEqual(0, get_goal(Teams.BLUE))
        self.assertEqual(BOARD_WIDTH - 1, get_goal(Teams.RED))


if __name__ == "__main__":
    unittest.main()
