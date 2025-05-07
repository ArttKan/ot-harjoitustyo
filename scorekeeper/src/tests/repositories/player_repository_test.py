import unittest
from entities.player import Player 
from entities.team import Team
from repositories.player_repository import PlayerRepository
from initialize_database import initialize_database
from database_connection import set_database_path, close_connection
from config import TEST_DATABASE_FILE_PATH


class TestPlayerRepository(unittest.TestCase):
    def setUp(self):
        set_database_path(TEST_DATABASE_FILE_PATH)
        initialize_database()
        self.player_repository = PlayerRepository()
        self.test_player1 = Player("test_player1", 11)
        self.test_player2 = Player("test_player2", 12)
        self.test_team1 = Team("test_team1", 1)
        self.test_team2 = Team("test_team2", 2)

    def test_create_player(self):
        self.assertEqual(self.player_repository.create(self.test_player1, self.test_team1.id).name, self.test_player1.name)

    def test_find_by_team(self):
        self.player_repository.create(self.test_player1, self.test_team1.id)
        self.player_repository.create(self.test_player2, self.test_team1.id)
        self.assertEqual([(x.name, x.number) for x in self.player_repository.find_by_team(self.test_team1.id)], [("test_player1", 11), ("test_player2", 12)])

    def test_find_all(self):
        self.player_repository.create(self.test_player1, self.test_team1.id)
        self.player_repository.create(self.test_player2, self.test_team1.id)
        self.assertEqual([(x.name, x.number) for x in self.player_repository.find_all()], [("test_player1", 11), ("test_player2", 12)])

    def test_find_by_number_and_team(self):
        self.player_repository.create(self.test_player1, self.test_team1.id)
        self.player_repository.create(self.test_player2, self.test_team1.id)
        self.assertEqual([(x.name, x.number) for x in [self.player_repository.find_by_number_and_team(self.test_player2.number, self.test_team1.id)]][0], (self.test_player2.name, self.test_player2.number))

    def test_delete_all(self):
        self.player_repository.create(self.test_player1, self.test_team1.id)
        self.player_repository.create(self.test_player2, self.test_team1.id)
        self.player_repository.delete_all()
        self.assertEqual(self.player_repository.find_all(), [])





    def tearDown(self):
        initialize_database()
        close_connection()   

