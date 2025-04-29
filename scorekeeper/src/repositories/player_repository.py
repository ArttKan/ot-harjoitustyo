from database_connection import get_database_connection
from entities.player import Player


class PlayerRepository:
    """Repository class for Player entities."""

    def __init__(self):
        """Initialize PlayerRepository with database connection."""
        self._connection = get_database_connection()

    def create(self, player, team_id):
        """Create a new player in the database.

        Args:
            player (Player): Player object to add
            team_id (int): ID of the team the player belongs to

        Returns:
            Player: Created player with id
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO players (name, number, team_id) VALUES (?, ?, ?)",
            (player.name, player.number, team_id)
        )

        self._connection.commit()
        return Player(player.name, player.number, cursor.lastrowid)

    def find_by_team(self, team_id):
        """Get all players in a team."""
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, name, number FROM players WHERE team_id = ?",
            (team_id,)
        )
        rows = cursor.fetchall()

        return [Player(row["name"], row["number"], row["id"]) for row in rows]

    def find_all(self):
        """Get all players from database.

        Returns:
            list: List of Player objects
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT name, number FROM players")
        rows = cursor.fetchall()

        return [Player(row["name"], row["number"]) for row in rows]

    def find_by_team(self, team_id):
        """Get all players in a team.

        Args:
            team_id (int): ID of the team

        Returns:
            list: List of Player objects
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT name, number FROM players WHERE team_id = ?",
            (team_id,)
        )
        rows = cursor.fetchall()

        return [Player(row["name"], row["number"]) for row in rows]

    def find_by_number_and_team(self, number, team_id):
        """Find a player by their number in a specific team.

        Args:
            number (int): Player's number
            team_id (int): Team's ID

        Returns:
            Player: Found player or None
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT name, number FROM players WHERE number = ? AND team_id = ?",
            (number, team_id)
        )
        row = cursor.fetchone()

        return Player(row["name"], row["number"]) if row else None

    def delete_all(self):
        """Delete all players from database."""
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM players")
        self._connection.commit()
