import unittest
from src.services.score_service import ScoreService
from entities.team import Team
from entities.event import Event
from entities.player import Player


class TestScoreService(unittest.TestCase):
    def setUp(self):
        self.score_service = ScoreService()
        self.test_player = Player("test_player", "13")
        self.test_team1 = Team("test_team1")
        self.test_team2 = Team("test_team2")
        self.test_event = Event("Foul", self.test_player, self.test_team1)

    def test_events_after_initialization(self):
        self.assertEqual(self.score_service.get_events(), [])

    def test_add_event(self):
        self.score_service.add_event(self.test_event)
        events = self.score_service.get_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].player, self.test_player)
        self.assertEqual(events[0].type, "Foul")

    def test_add_team(self):
        self.score_service.add_team(self.test_team1)
        self.assertEqual(self.score_service.teams[0], self.test_team1)

    def test_get_teams(self):
        self.score_service.add_team(self.test_team1)
        self.score_service.add_team(self.test_team2)
        self.assertEqual(self.score_service.get_teams(),
                         [self.test_team1, self.test_team2])

    def test_get_score(self):
        self.assertEqual(0, self.score_service.get_team_score(self.test_team1))
