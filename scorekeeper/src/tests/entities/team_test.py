import unittest
from src.entities.team import Team
from src.entities.player import Player


class TestTeam(unittest.TestCase):
    def setUp(self):
        self.test_team = Team("test_team", 1)

    def test_add_player(self):
        test_player = Player("test_player", "test_team")
        self.test_team.add_player(test_player)
        self.assertEqual(self.test_team.get_players(), [test_player])

    def test_get_players(self):
        test_player1 = Player("test_player1", "test_team")
        test_player2 = Player("test_player2", "test_team")
        self.test_team.add_player(test_player1)
        self.test_team.add_player(test_player2)
        self.assertEqual(self.test_team.get_players(),
                         [test_player1, test_player2])

    def test_get_id(self):
        self.assertEqual(self.test_team.id, 1)

    def test_get_name(self):
        self.assertEqual(self.test_team.name, "test_team")
