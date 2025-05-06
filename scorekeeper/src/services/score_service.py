import sqlite3
from entities.game import Game
from entities.player import Player
from repositories.event_repository import EventRepository
from repositories.game_repository import GameRepository
from repositories.team_repository import TeamRepository


class ScoreService:
    def __init__(self):
        """Initialize score service with repositories."""
        self.event_repository = EventRepository()
        self.game_repository = GameRepository()
        self.team_repository = TeamRepository()

    def get_team_by_name(self, team):
        team = self.team_repository.get_team_by_name(team)
        return team

    def get_teams(self):
        """Get all available teams.

        Returns:
            list: List of Team objects
        """
        return self.team_repository.get_all_teams()

    def get_team_players(self, team_name):
        """Get all players in a team.

        Args:
            team_name (str): Name of the team

        Returns:
            list: List of Player objects
        """
        return self.team_repository.get_team_players(team_name)

    def start_new_game(self, team1_name, team2_name):
        """Start a new game with selected teams.

        Args:
            team1_name (str): Name of home team
            team2_name (str): Name of away team

        Returns:
            Game: Started game instance

        Raises:
            ValueError: If either team doesn't exist
        """
        team1 = self.team_repository.create_team(team1_name, 1)
        team2 = self.team_repository.create_team(team2_name, 2)
        self.team_repository.add_team(team1)
        self.team_repository.add_team(team2)

        if not team1 or not team2:
            raise ValueError("Both teams must exist")

        game = Game()
        game.add_team(team1)
        game.add_team(team2)

        return self.game_repository.start_new_game(game)

    def get_current_game(self):
        """Get current game instance with teams and players.

        Returns:
            Game: Current game instance or None
        """
        game = self.game_repository.get_current_game()
        if game:
            for team in game.get_teams():
                players = self.get_team_players(team.name)
                for player in players:
                    team.add_player(player)
        return game

    def add_player(self, team, name, number):
        """Add a player to a team.

        Args:
            team (Team): Team to add player to
            name (str): Player name
            number (int): Player jersey number

        Returns:
            Player: Added player or None if failed

        Raises:
            ValueError: If player creation fails
        """
        try:
            player = Player(name, number)
            success = self.team_repository.add_player_to_team(
                team.name, player)
            return player if success else None
        except sqlite3.IntegrityError:
            print(f"Player number {number} already exists in team {team.name}")
            raise

    def add_event(self, event):
        """Add a game event and update scores if needed.

        Args:
            event (Event): Event to add
        """
        current_game = self.get_current_game()
        if not current_game:
            raise ValueError("No active game")

        result = self.event_repository.add_event(event, current_game.id)
        if not result:
            print("Failed to add event")
            return None

        return result

    def get_events(self):
        """Get all events for current game.

        Returns:
            list: List of Event objects
        """
        current_game = self.get_current_game()
        if not current_game:
            return []
        return self.event_repository.get_game_events(current_game.id)

    def get_team_score(self, team_name):
        """Get current score for a team.

        Args:
            team_name (str): Name of the team

        Returns:
            int: Current score
        """
        current_game = self.get_current_game()
        if not current_game:
            return 0

        team = self.team_repository.get_team_by_name(team_name)
        if not team:
            return 0

        return self.game_repository.get_game_score(current_game.id, team.id)
