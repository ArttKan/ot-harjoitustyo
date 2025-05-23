import sqlite3
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
            "INSERT INTO teams (id, name) VALUES (?, ?)",
            (team.id, team.name)
        )

        self._connection.commit()
        return Team(team.name, team.id)

    def create_team(self, team_name, team_id):
        """Create a new team entity without saving to database.

        Args:
            team_name (str): Name of the team to create

        Returns:
            Team: Created team entity without database ID

        Raises:
            ValueError: If team name is invalid
        """
        if not team_name or not isinstance(team_name, str):
            raise ValueError("Team name must be a non-empty string")

        return Team(team_name, team_id)

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
                """INSERT INTO players (name, number, team_id) 
                VALUES (?, ?, (SELECT id FROM teams WHERE name = ?))""",
                (player.name, player.number, team_name)
            )

            self._connection.commit()
            player_id = cursor.lastrowid
            return Player(player.name, player.number, player_id)
        except sqlite3.IntegrityError as error:
            print(f"Player number already exists in team: {error}")
            return None
        except sqlite3.Error as error:
            print(f"Database error: {error}")
            return None

    def get_team_players(self, team_name):
        """Get all players in a team."""
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT p.id, p.name, p.number 
            FROM players p 
            JOIN teams t ON p.team_id = t.id 
            WHERE t.name = ?
        """, (team_name,))
        rows = cursor.fetchall()

        return [Player(row["name"], row["number"], row["id"]) for row in rows]
