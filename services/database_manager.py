# DatabaseManager service class
import sqlite3
from pathlib import Path
from typing import Any, List, Tuple, Optional

class DatabaseManager:
    """Handles SQLite database connections and queries."""

    def __init__(self, db_path: str = "DATA/intelligence_platform.db"):
        self._db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Establish database connection."""
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path, check_same_thread=False)
            print(f"Connected to database at: {self._db_path}")

    def close(self) -> None:
        """Close database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def execute_query(self, sql: str, params: Tuple = ()) -> sqlite3.Cursor:
        """Execute a write query (INSERT, UPDATE, DELETE)."""
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, params)
        self._connection.commit()
        return cur

    def fetch_one(self, sql: str, params: Tuple = ()) -> Optional[Tuple]:
        """Fetch a single row from database."""
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, params)
        return cur.fetchone()

    def fetch_all(self, sql: str, params: Tuple = ()) -> List[Tuple]:
        """Fetch all rows from database."""
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    # Incident methods
    def get_all_incidents(self) -> List[Tuple]:
        """Get all security incidents."""
        return self.fetch_all(
            "SELECT id, date, incident_type, severity, status, description FROM cyber_incidents"
        )

    def insert_incident(self, date: str, incident_type: str, severity: str, 
                       status: str, description: str) -> None:
        """Insert a new incident."""
        self.execute_query(
            "INSERT INTO cyber_incidents (date, incident_type, severity, status, description) VALUES (?, ?, ?, ?, ?)",
            (date, incident_type, severity, status, description)
        )

    # Dataset methods
    def get_all_datasets(self) -> List[Tuple]:
        """Get all datasets."""
        return self.fetch_all(
            "SELECT id, dataset_name, category, source, last_updated, record_count, file_size_mb FROM datasets_metadata"
        )

    def insert_dataset(self, name: str, category: str, source: str, 
                      last_updated: str, record_count: int, file_size_mb: float) -> None:
        """Insert a new dataset."""
        self.execute_query(
            "INSERT INTO datasets_metadata (dataset_name, category, source, last_updated, record_count, file_size_mb) VALUES (?, ?, ?, ?, ?, ?)",
            (name, category, source, last_updated, record_count, file_size_mb)
        )

    # Ticket methods
    def get_all_tickets(self) -> List[Tuple]:
        """Get all IT tickets."""
        return self.fetch_all(
            "SELECT ticket_id, created_date, category, priority, status, description, assigned_to FROM it_tickets"
        )

    def insert_ticket(self, date: str, category: str, priority: str, 
                     status: str, description: str, assigned_to: str) -> None:
        """Insert a new ticket."""
        # Generate a unique ticket_id if needed
        import uuid
        ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
        self.execute_query(
            "INSERT INTO it_tickets (ticket_id, created_date, category, priority, status, subject, description, assigned_to) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (ticket_id, date, category, priority, status, description[:100] if description else "", description, assigned_to)
        )

    # User methods
    def get_user(self, username: str) -> Optional[Tuple]:
        """Get user by username. Returns (username, password_hash, role)."""
        return self.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,)
        )

    def insert_user(self, username: str, password_hash: str) -> None:
        """Insert a new user."""
        self.execute_query(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )

    def user_exists(self, username: str) -> bool:
        """Check if user exists."""
        result = self.fetch_one(
            "SELECT 1 FROM users WHERE username = ?",
            (username,)
        )
        return result is not None

