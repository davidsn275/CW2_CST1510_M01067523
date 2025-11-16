import sqlite3
from pathlib import Path

DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    # Check if the DATA folder exists, if not create it
    if not db_path.parent.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Created DATA folder")
    
    # Connect to the database (creates file if it doesn't exist)
    conn = sqlite3.connect(str(db_path))
    
    print(f"Connected to database at: {db_path}")
    
    return sqlite3.connect(str(db_path))