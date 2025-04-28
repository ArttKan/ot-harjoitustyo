from database_connection import get_database_connection
from entities.event import Event
from datetime import datetime


class EventRepository:
    """Repository class for Event entities."""

    def __init__(self):
        """Initialize EventRepository with database connection."""
        self._connection = get_database_connection()

    def add_event(self, event, game_id):
        """Add a new event to the database.

        Args:
            event (Event): Event object to add
            game_id (int): ID of the game this event belongs to

        Returns:
            Event: Added event
        """
        cursor = self._connection.cursor()

        cursor.execute(
            """INSERT INTO events (type, game_id, player_id, team_id, timestamp)
               VALUES (?, ?, ?, ?, ?)""",
            (
                event.type,
                game_id,
                event.player.id,
                event.team.id,
                datetime.now().isoformat()
            )
        )

        self._connection.commit()
        return event

    def get_all_events(self):
        """Get all events from database.

        Returns:
            list: List of event data tuples
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT e.*, p.name as player_name, p.number as player_number, 
                   t.name as team_name
            FROM events e
            JOIN players p ON e.player_id = p.id
            JOIN teams t ON e.team_id = t.id
            ORDER BY e.timestamp DESC
        """)
        return cursor.fetchall()

    def get_events_by_team(self, team_id):
        """Get all events for a specific team.

        Args:
            team_id (int): ID of the team

        Returns:
            list: List of event data tuples
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT e.*, p.name as player_name, p.number as player_number
            FROM events e
            JOIN players p ON e.player_id = p.id
            WHERE e.team_id = ?
            ORDER BY e.timestamp DESC
        """, (team_id,))
        return cursor.fetchall()

    def get_events_by_player(self, player_id):
        """Get all events for a specific player.

        Args:
            player_id (int): ID of the player

        Returns:
            list: List of event data tuples
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT e.*, t.name as team_name
            FROM events e
            JOIN teams t ON e.team_id = t.id
            WHERE e.player_id = ?
            ORDER BY e.timestamp DESC
        """, (player_id,))
        return cursor.fetchall()

    def get_scoring_events_by_team(self, team_id):
        """Get all scoring events for a team.

        Args:
            team_id (int): ID of the team

        Returns:
            list: List of scoring event data tuples
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT e.*, p.name as player_name, p.number as player_number
            FROM events e
            JOIN players p ON e.player_id = p.id
            WHERE e.team_id = ? AND e.type IN ('2-Pointer', '3-Pointer')
            ORDER BY e.timestamp DESC
        """, (team_id,))
        return cursor.fetchall()

    def delete_all(self):
        """Delete all events from database."""
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM events")
        self._connection.commit()
