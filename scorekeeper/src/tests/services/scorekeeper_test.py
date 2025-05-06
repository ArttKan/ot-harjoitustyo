import unittest
from src.services.score_service import ScoreService
from entities.team import Team
from entities.event import Event
from entities.player import Player
from initialize_database import initialize_database
from database_connection import set_database_path, close_connection
from config import TEST_DATABASE_FILE_PATH


class TestScoreService(unittest.TestCase):
    def setUp(self):
        set_database_path(TEST_DATABASE_FILE_PATH)
        initialize_database()
        self.score_service = ScoreService()
        self.test_player1 = Player("test_player1", "11")
        self.test_player2 = Player("test_player2", "12")
        self.test_team1 = Team("test_team1", 1)
        self.test_team2 = Team("test_team2", 2)
        self.score_service.add_player(self.test_team1, self.test_player1.name, self.test_player1.number)
        self.score_service.add_player(self.test_team2, self.test_player2.name, self.test_player2.number)
        self.test_event = Event("Foul", self.test_player1, self.test_team1)
        self.score_service.start_new_game(self.test_team1.name, self.test_team2.name)

    def test_events_after_initialization(self):
        self.assertEqual(self.score_service.get_events(), [])

    def test_add_event(self):
        """Test that events are properly added to database."""
        print("\nStarting test_add_event")
        
        # Verify game exists
        current_game = self.score_service.get_current_game()
        print(f"Current game ID: {current_game.id if current_game else 'None'}")
        
        # Create event and verify it was added
        result = self.score_service.add_event(self.test_event)
        print(f"Add event result: {result}")
        self.assertIsNotNone(result, "Event should be returned after adding")
        
        # Get events and verify content
        events = self.score_service.get_events()
        print(f"Retrieved events count: {len(events)}")
        
        # Direct database query to verify event existence
        cursor = self.score_service.event_repository._connection.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM events")
        count = cursor.fetchone()["count"]
        print(f"Events in database: {count}")
        
        self.assertEqual(len(events), 1, "Should have exactly one event")
        
        if events:
            added_event = events[0]
            print(f"Added event details: {added_event.type} by {added_event.player.name}")
            self.assertEqual(added_event.type, "Foul")
            self.assertEqual(added_event.player.name, self.test_player1.name)
            self.assertEqual(added_event.team.name, self.test_team1.name)

    def test_get_score(self):
        self.assertEqual(0, self.score_service.get_team_score(self.test_team1.name))

    def tearDown(self):
        initialize_database()
        close_connection()   
