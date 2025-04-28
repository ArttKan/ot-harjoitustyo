from database_connection import get_database_connection
from entities.game import Game
from datetime import datetime


class GameRepository:
    """Repository class for Game entities."""

    def __init__(self):
        """Initialize GameRepository with database connection."""
        self._connection = get_database_connection()
        self._current_game_id = None

    def start_new_game(self, home_team_id, away_team_id):
        """Start a new game and store it in database.

        Args:
            home_team_id (int): ID of the home team
            away_team_id (int): ID of the away team

        Returns:
            int: ID of the created game
        """
        cursor = self._connection.cursor()

        cursor.execute(
            """INSERT INTO games (home_team_id, away_team_id, date) 
               VALUES (?, ?, ?)""",
            (home_team_id, away_team_id, datetime.now().isoformat())
        )

        self._connection.commit()
        self._current_game_id = cursor.lastrowid
        return self._current_game_id

    def get_current_game(self):
        """Get the current game from database.

        Returns:
            tuple: Game data (id, home_team_id, away_team_id, date) or None
        """
        if not self._current_game_id:
            return None

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM games WHERE id = ?",
            (self._current_game_id,)
        )
        return cursor.fetchone()

    def get_game_score(self, game_id, team_id):
        """Get current score for a team in a game.

        Args:
            game_id (int): ID of the game
            team_id (int): ID of the team

        Returns:
            int: Current score
        """
        cursor = self._connection.cursor()
        cursor.execute(
            """SELECT SUM(
                CASE 
                    WHEN type = '2-Pointer' THEN 2
                    WHEN type = '3-Pointer' THEN 3
                    ELSE 0
                END
            ) as score
            FROM events
            WHERE game_id = ? AND team_id = ?
            AND type IN ('2-Pointer', '3-Pointer')""",
            (game_id, team_id)
        )
        result = cursor.fetchone()
        return result["score"] or 0

    def get_all_games(self):
        """Get all games from database.

        Returns:
            list: List of game data tuples
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM games ORDER BY date DESC")
        return cursor.fetchall()

    def delete_game(self, game_id):
        """Delete a game and its related events.

        Args:
            game_id (int): ID of the game to delete
        """
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM events WHERE game_id = ?", (game_id,))
        cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))
        self._connection.commit()

        if self._current_game_id == game_id:
            self._current_game_id = None
