# Week 8 - Database connection file
# This file connects to the SQLite database

import sqlite3
from pathlib import Path

# Where the database file will be saved
DB_PATH = Path("DATA") / "intelligence_platform.db"


def connect_database(db_path=DB_PATH):
    # Connect to database (makes it if it doesn't exist)
    return sqlite3.connect(str(db_path))
