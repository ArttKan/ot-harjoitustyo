import unittest
from src.entities.team import Team
from src.entities.game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.test_team1 = Team("test_team1")
        self.test_team2 = Team("test_team2")
        self.test_game = Game()
        self.test_game.add_home_team(self.test_team1)
        self.test_game.add_away_team(self.test_team2)

    def test_team_addition(self):
        self.assertEqual(self.test_game.get_teams(), [
                         self.test_team1, self.test_team2])

    def test_get_team_names(self):
        self.assertEqual(["test_team1", "test_team2"],
                         self.test_game.get_team_names())

    def test_get_names_with_only_home_team(self):
        self.test_game2 = Game()
        self.test_game2.add_home_team(self.test_team1)
        self.assertEqual(None, self.test_game2.get_team_names()[1])
