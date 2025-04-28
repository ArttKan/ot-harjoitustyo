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

    # Create teams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Create players table
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

    # Create games table
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

    # Create events table
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
        print(f"Data directory path: {data_dir}")
        print(f"Data directory exists: {os.path.exists(data_dir)}")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Created data directory: {data_dir}")

        print(f"Full database path will be: {DATABASE_FILE_PATH}")

        connection = get_database_connection()
        print("Got database connection successfully")

        drop_tables(connection)
        print("Tables dropped successfully")

        create_tables(connection)
        print("Tables created successfully")

        close_connection()
        print(f"Database initialized successfully at: {DATABASE_FILE_PATH}")

    except Exception as error:
        print(f"Error during database initialization: {str(error)}")
        raise


if __name__ == "__main__":
    initialize_database()
