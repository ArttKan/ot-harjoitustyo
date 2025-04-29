import unittest
from src.entities.team import Team
from src.entities.game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.test_team1 = Team("test_team1")
        self.test_team2 = Team("test_team2")
        self.test_game = Game(1)
        self.test_game.add_team(self.test_team1)
        self.test_game.add_team(self.test_team2)

    def test_team_addition(self):
        self.assertEqual(self.test_game.get_teams(), (
                         self.test_team1, self.test_team2))

    def test_get_teams(self):
        self.assertEqual((self.test_team1, self.test_team2),
                         self.test_game.get_teams())

    def test_get_teams_with_only_home_team(self):
        self.test_game2 = Game()
        self.test_game2.add_team(self.test_team1)
        self.assertEqual(None, self.test_game2.get_teams()[1])

    def test_get_home_team(self):
        self.assertEqual(self.test_team1, self.test_game.get_home_team())

    def test_get_away_team(self):
        self.assertEqual(self.test_team2, self.test_game.get_away_team())

    def test_adding_third_team(self):
        self.test_team3 = Team("test_team3")
        self.assertEqual(self.test_game.add_team(self.test_team3), False)

    def test_get_game_id(self):
        self.assertEqual(self.test_game.id, 1)
