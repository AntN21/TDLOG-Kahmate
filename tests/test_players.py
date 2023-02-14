"""
Test for the classes of the different players
"""
import unittest
import random as rd
from constants import Teams
from players.ordinary import Ordinary
from players.fast import Fast
from players.clever import Clever
from players.strong import Strong
from players.tough import Tough

rd.seed(1)


def get_team():
    """Gets a random team"""
    return rd.choice([Teams.RED, Teams.BLUE])


def get_players():
    """Get an array of all players with random teams"""
    return [
        Ordinary(get_team()),
        Fast(get_team()),
        Clever(get_team()),
        Strong(get_team()),
        Tough(get_team()),
    ]


class TestPlayers(unittest.TestCase):
    """Different players tests class"""

    def test_reduce_moves(self):
        """reduce moves function test"""
        for mock_player in get_players():
            self.assertEqual(mock_player.max_move, mock_player.available_moves)
            mock_player.reduce_moves(mock_player.max_move)
            self.assertEqual(0, mock_player.available_moves)

    def test_set_stunned(self):
        """set stunned function test"""
        for mock_player in get_players():
            self.assertFalse(mock_player.stunned)
            mock_player.set_stunned()
            self.assertTrue(mock_player.stunned)

    def test_recover(self):
        """recover function test"""
        for mock_player in get_players():
            self.assertFalse(mock_player.stunned)
            self.assertFalse(mock_player.get_just_lost())
            mock_player.set_stunned()
            mock_player.set_just_lost()
            self.assertTrue(mock_player.stunned)
            self.assertTrue(mock_player.get_just_lost())
            mock_player.recover()
            self.assertTrue(mock_player.stunned)
            self.assertFalse(mock_player.get_just_lost())
            mock_player.recover()
            self.assertFalse(mock_player.stunned)

    def test_reset_moves(self):
        """reset moves function test"""
        for mock_player in get_players():
            mock_player.reduce_moves(mock_player.max_move)
            self.assertEqual(0, mock_player.available_moves)
            mock_player.reset_moves()
            self.assertEqual(mock_player.max_move, mock_player.available_moves)

    def test_set_just_lost(self):
        """set just lost test"""
        for mock_player in get_players():
            self.assertFalse(mock_player.get_just_lost())
            mock_player.set_just_lost()
            self.assertTrue(mock_player.get_just_lost())

    def test_reset_just_lost(self):
        """reset just lost function test"""
        for mock_player in get_players():
            mock_player.set_just_lost()
            mock_player.reset_just_lost()
            self.assertFalse(mock_player.get_just_lost())

    def test_str(self):
        """string convertion function test"""
        for mock_player in get_players():
            self.assertEqual(f"{mock_player.type}_{mock_player.team}", str(mock_player))
            mock_player.set_stunned()
            self.assertEqual(f"ko_{mock_player.team}", str(mock_player))


if __name__ == "__main__":
    unittest.main()
