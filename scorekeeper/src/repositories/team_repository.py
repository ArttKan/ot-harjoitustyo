from database.db_connection import db
from entities.team import Team
from entities.player import Player


class TeamRepository:
    def __init__(self):
        self._connection = db.get_connection()

    def add_team(self, team):
        """Add a new team to the database."""
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO teams (name) VALUES (?)",
            (team.name,)
        )

        self._connection.commit()
        return team

    def get_all_teams(self):
        """Get all teams from database."""
        cursor = self._connection.cursor()

        cursor.execute("SELECT id, name FROM teams")
        rows = cursor.fetchall()

        return [Team(row["name"]) for row in rows]

    def get_team_by_name(self, team_name):
        """Get a team by its name."""
        for team in self.teams:
            if team.name == team_name:
                return team
        return None

    def add_player_to_team(self, team_name, player):
        """Add a player to a team."""
        team = self.get_team_by_name(team_name)
        if team:
            team.add_player(player)
            return True
        return False

    def get_team_players(self, team_name):
        """Get all players in a team."""
        team = self.get_team_by_name(team_name)
        return team.get_players() if team else []
