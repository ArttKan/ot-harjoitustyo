from datetime import datetime
from database_connection import get_database_connection
from entities.game import Game
from entities.team import Team
from repositories.team_repository import TeamRepository


class GameRepository:
    """Repository class for Game entities."""

    def __init__(self):
        self._connection = get_database_connection()
        self._current_game_id = None
        self._team_repository = TeamRepository()

    def start_new_game(self, game):
        """Start a new game and store it in database.

        Args:
            game: Game object containing teams

        Returns:
            Game: Started game with ID
        """
        cursor = self._connection.cursor()
        teams = game.get_teams()


        cursor.execute(
            """INSERT INTO games (home_team_id, away_team_id, date) 
            VALUES (?, ?, ?)""",
            (teams[0].id, teams[1].id, datetime.now().isoformat())
        )

        self._connection.commit()
        self._current_game_id = cursor.lastrowid

        game_with_id = Game(game_id=self._current_game_id)
        game_with_id.add_team(teams[0])
        game_with_id.add_team(teams[1])

        return game_with_id

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

    def get_current_game(self):
        """Get the current game from database.

        Returns:
            Game: Current game instance or None
        """
        if not self._current_game_id:
            return None

        cursor = self._connection.cursor()
        cursor.execute(
            """SELECT g.*, 
                    t1.name as home_team_name,
                    t2.name as away_team_name
            FROM games g
            JOIN teams t1 ON g.home_team_id = t1.id
            JOIN teams t2 ON g.away_team_id = t2.id
            WHERE g.id = ?""",
            (self._current_game_id,)
        )
        row = cursor.fetchone()

        if not row:
            return None

        game = Game(game_id=row["id"])
        game.add_team(Team(row["home_team_name"]))
        game.add_team(Team(row["away_team_name"]))

        return game

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

    def add_points(self, game_id, team_id, points):
        """Add points to a team's score in a game.

        Args:
            game_id (int): ID of the game
            team_id (int): ID of the team
            points (int): Number of points to add
        """
        cursor = self._connection.cursor()

        cursor.execute(
            """INSERT INTO events (type, game_id, team_id, timestamp)
            VALUES (?, ?, ?, ?)""",
            (f"{points}-Pointer", game_id, team_id, datetime.now().isoformat())
        )

        self._connection.commit()
