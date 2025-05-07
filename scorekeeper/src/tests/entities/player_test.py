import unittest
from src.entities.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.test_player1 = Player("test_player1", 1, 1)

    def test_get_id(self):
        self.assertEqual(self.test_player1.id, 1)

    def test_get_str(self):
        self.assertEqual(str(self.test_player1), "1 test_player1")
