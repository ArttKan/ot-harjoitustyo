import unittest
from src.services.score_service import ScoreService
from entities.team import Team


class TestScoreService(unittest.TestCase):
    def setUp(self):
        self.score_service = ScoreService()

    def test_events_after_initialization(self):
        self.assertEqual(self.score_service.get_events(), [])

    def test_add_event(self):
        self.score_service.add_event(2, "basket")
        events = self.score_service.get_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].content, 2)
        self.assertEqual(events[0].type, "basket")

    def test_add_team(self):
        test_team = Team("test")
        self.score_service.add_team(test_team)
        self.assertEqual(self.score_service.teams[0], test_team)

    def test_get_teams(self):
        test_team1 = Team("test1")
        test_team2 = Team("test2")
        self.score_service.add_team(test_team1)
        self.score_service.add_team(test_team2)
        self.assertEqual(self.score_service.get_teams(),
                         [test_team1, test_team2])
