import unittest
from src.services.score_service import ScoreService
from entities.team import Team
from entities.event import Event
from entities.player import Player
from initialize_database import initialize_database
from database_connection import set_database_path, get_database_connection, close_connection
from config import TEST_DATABASE_FILE_PATH


class TestScoreService(unittest.TestCase):
    def setUp(self):
        set_database_path(TEST_DATABASE_FILE_PATH)
        initialize_database()
        get_database_connection()
        self.score_service = ScoreService()
        self.test_player1 = Player("test_player1", 11)
        self.test_player2 = Player("test_player2", 12)
        self.test_team1 = Team("test_team1", 1)
        self.test_team2 = Team("test_team2", 2)
        self.score_service.add_player(self.test_team1, self.test_player1.name, self.test_player1.number)
        self.score_service.add_player(self.test_team2, self.test_player2.name, self.test_player2.number)
        self.test_event = Event("Foul", self.test_player1, self.test_team1)
        self.score_service.start_new_game(self.test_team1.name, self.test_team2.name)

    def test_events_after_initialization(self):
        self.assertEqual(self.score_service.get_events(), [])


    def test_get_score(self):
        self.assertEqual(0, self.score_service.get_team_score(self.test_team1.name))

    def test_get_team_by_name(self):
        self.assertEqual(self.score_service.get_team_by_name("test_team1").name, self.test_team1.name)

    def test_get_all_teams(self):
        self.assertEqual([x.id for x in self.score_service.get_teams()], [self.test_team1.id, self.test_team2.id])

    def tearDown(self):
        initialize_database()
        close_connection()   
