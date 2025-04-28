from entities.team import Team
from entities.game import Game
from entities.player import Player
from entities.event import Event
from repositories.event_repository import EventRepository
from repositories.game_repository import GameRepository
from repositories.team_repository import TeamRepository


class ScoreService:
    def __init__(self):
        self.event_repository = EventRepository()
        self.game_repository = GameRepository()
        self.team_repository = TeamRepository()
        self._initialize_demo_data()

    def _initialize_demo_data(self):
        """Initialize demo data."""
        team1 = Team("Golden State Warriors")
        team2 = Team("Los Angeles Lakers")
        team1.add_player(Player("Stephen Curry", 30))
        team1.add_player(Player("Draymond Green", 23))
        team2.add_player(Player("Luka Doncic", 77))
        team2.add_player(Player("LeBron James", 6))

        self.team_repository.add_team(team1)
        self.team_repository.add_team(team2)

    def get_teams(self):
        """Get list of available teams."""
        return self.team_repository.get_all_teams()

    def start_new_game(self):
        """Start a new game."""
        game = Game()
        return self.game_repository.start_new_game(game)

    def get_current_game(self):
        """Get current game instance."""
        return self.game_repository.get_current_game()

    def add_event(self, event: Event):
        """Add an event and update scores if needed."""
        self.event_repository.add_event(event)

        # Update score for scoring events
        if event.type == "2-Pointer":
            self.game_repository.update_score(event.team.name, 2)
        elif event.type == "3-Pointer":
            self.game_repository.update_score(event.team.name, 3)

    def get_events(self):
        """Get list of all events."""
        return self.event_repository.get_all_events()

    def get_team_score(self, team_name: str):
        """Get current score for a team."""
        return self.game_repository.get_score(team_name)

