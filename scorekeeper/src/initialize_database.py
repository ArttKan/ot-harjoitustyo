import os
from database_connection import get_database_connection, close_connection
from config import DATABASE_FILE_PATH


def drop_tables(connection):
    """Drops tables if they exist"""
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS teams''')
    cursor.execute('''DROP TABLE IF EXISTS players''')
    cursor.execute('''DROP TABLE IF EXISTS games''')
    cursor.execute('''DROP TABLE IF EXISTS events''')
    connection.commit()


def create_tables(connection):
    """Create database tables."""
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            number INTEGER NOT NULL,
            team_id INTEGER,
            FOREIGN KEY (team_id) REFERENCES teams (id),
            UNIQUE (team_id, number)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            home_team_id INTEGER,
            away_team_id INTEGER,
            date TEXT NOT NULL,
            FOREIGN KEY (home_team_id) REFERENCES teams (id),
            FOREIGN KEY (away_team_id) REFERENCES teams (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL,
            game_id INTEGER,
            player_id INTEGER,
            team_id INTEGER,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (game_id) REFERENCES games (id),
            FOREIGN KEY (player_id) REFERENCES players (id),
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )
    ''')

    connection.commit()


def initialize_database():
    """Initialize the database."""
    try:
        data_dir = os.path.dirname(DATABASE_FILE_PATH)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        connection = get_database_connection()
        drop_tables(connection)
        create_tables(connection)
        close_connection()

    except Exception as error:
        print(f"Error during database initialization: {str(error)}")
        raise


if __name__ == "__main__":
    initialize_database()
