from datetime import datetime
import sqlite3
from database_connection import get_database_connection
from entities.event import Event
from entities.player import Player
from entities.team import Team


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
        try:
            cursor = self._connection.cursor()

            player_id = event.player.id if event.player else None
            print(
                "Adding event to database: "
                f"game_id={game_id}, "
                f"type={event.type}, "
                f"team={event.team.name}")

            cursor.execute(
                """INSERT INTO events (type, game_id, player_id, team_id, timestamp)
                VALUES (?, ?, ?, ?, ?)""",
                (
                    event.type,
                    game_id,
                    player_id,
                    event.team.id,
                    datetime.now().isoformat()
                )
            )

            self._connection.commit()

            cursor.execute("SELECT last_insert_rowid()")
            event_id = cursor.fetchone()[0]
            print(f"Event added with ID: {event_id}")

            return event

        except sqlite3.IntegrityError as error:
            print(f"Database constraint violation: {error}")
            raise

        except sqlite3.Error as error:
            print(f"Database error: {error}")
            raise

    def get_all_events(self):
        """Get all events from database.

        Returns:
            list: List of Event objects
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT e.*, 
                p.name as player_name, 
                p.number as player_number, 
                t.name as team_name,
                t.id as team_id
            FROM events e
            LEFT JOIN players p ON e.player_id = p.id
            JOIN teams t ON e.team_id = t.id
            ORDER BY e.timestamp DESC
        """)

        rows = cursor.fetchall()
        return [self._create_event_from_row(row) for row in rows]

    def _create_event_from_row(self, row):
        """Create Event object from database row."""
        if row["player_id"]:
            player = Player(row["player_name"],
                            row["player_number"], row["player_id"])
        else:
            player = None

        team = Team(row["team_name"], row["team_id"])
        return Event(row["type"], player, team)

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

    def get_game_events(self, game_id):
        """Get all events for a specific game.

        Args:
            game_id (int): ID of the game

        Returns:
            list: List of Event objects
        """

        cursor = self._connection.cursor()

        print(f"Fetching events with game_id={game_id}")

        cursor.execute(
            """SELECT 
                e.*,
                t.name as team_name,
                t.id as team_id,
                p.name as player_name,
                p.number as player_number
            FROM events e
            JOIN teams t ON e.team_id = t.id
            LEFT JOIN players p ON e.player_id = p.id
            WHERE e.game_id = ?
            ORDER BY e.timestamp DESC""",
            (game_id,)
        )

        rows = cursor.fetchall()

        events = []
        for row in rows:
            try:
                if row["player_id"]:
                    player = Player(
                        row["player_name"],
                        row["player_number"],
                        row["player_id"]
                    )
                else:
                    player = None

                team = Team(row["team_name"], row["team_id"])
                event = Event(row["type"], player, team)
                events.append(event)

            except KeyError:
                continue
            except ValueError:
                continue

        return events

    def delete_all(self):
        """Delete all events from database."""
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM events")
        self._connection.commit()
