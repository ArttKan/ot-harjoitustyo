import os

DIRNAME = os.path.dirname(__file__)
ROOT_DIR = os.path.normpath(os.path.join(DIRNAME, ".."))
DATABASE_FILENAME = "database.sqlite"
DATABASE_FILE_PATH = os.path.join(ROOT_DIR, "data", DATABASE_FILENAME)
