import sqlite3
from config import DATABASE_FILE_PATH


class DatabaseConnection:
    def __init__(self):
        self._connection = None
        self._database_path = DATABASE_FILE_PATH

    def get_database_connection(self):
        """Get database connection."""
        if not self._connection:
            self._connection = sqlite3.connect(self._database_path)
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def close_connection(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def set_database_path(self, path):
        """Sets the database path. Closes any existing connections
        Args:
        path (str): The new database path"""
        self.close_connection()
        self._database_path = path


_db = DatabaseConnection()

# Public interface
def get_database_connection():
    return _db.get_database_connection()


def close_connection():
    _db.close_connection()


def set_database_path(path):
    _db.set_database_path(path)
