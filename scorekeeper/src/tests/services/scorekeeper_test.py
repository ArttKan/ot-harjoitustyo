import unittest
from src.services.score_service import ScoreService


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
