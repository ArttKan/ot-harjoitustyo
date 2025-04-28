from database_connection import get_database_connection
from entities.team import Team
from entities.player import Player


class TeamRepository:
    def __init__(self):
        self._connection = get_database_connection()

    def add_team(self, team):
        """Add a new team to the database."""
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO teams (name) VALUES (?)",
            (team.name,)
        )

        self._connection.commit()
        return Team(team.name, cursor.lastrowid)

    def get_team_by_name(self, team_name):
        """Get a team by its name."""
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, name FROM teams WHERE name = ?",
            (team_name,)
        )
        row = cursor.fetchone()
        return Team(row["name"], row["id"]) if row else None

    def get_all_teams(self):
        """Get all teams from database."""
        cursor = self._connection.cursor()

        cursor.execute("SELECT id, name FROM teams")
        rows = cursor.fetchall()

        return [Team(row["name"], row["id"]) for row in rows]

    def add_player_to_team(self, team_name, player):
        """Add a player to a team."""
        try:
            cursor = self._connection.cursor()
            cursor.execute(
                "INSERT INTO players (name, number, team_id) VALUES (?, ?, (SELECT id FROM teams WHERE name = ?))",
                (player.name, player.number, team_name)
            )
            self._connection.commit()
            return True
        except:
            return False

    def get_team_players(self, team_name):
        """Get all players in a team."""
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT p.name, p.number 
            FROM players p 
            JOIN teams t ON p.team_id = t.id 
            WHERE t.name = ?
        """, (team_name,))
        rows = cursor.fetchall()

        return [Player(row["name"], row["number"]) for row in rows]
