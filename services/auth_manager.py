import hashlib
from typing import Optional, Tuple
from services.database_manager import DatabaseManager
from models.user import User

class SimpleHasher:
    """Simple hasher using SHA256 for password hashing."""

    @staticmethod
    def hash_password(plain: str) -> str:
        """Hash a plain text password."""
        return hashlib.sha256(plain.encode("utf-8")).hexdigest()

    @staticmethod
    def check_password(plain: str, hashed: str) -> bool:
        """Check if plain password matches hashed password."""
        return SimpleHasher.hash_password(plain) == hashed


class AuthManager:
    """Handles user registration and login."""

    def __init__(self, db: DatabaseManager):
        self._db = db

    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Register a new user. Returns (success, message)."""
        # Check if user already exists
        if self._db.user_exists(username):
            return False, "Username already exists"

        # Hash password and insert user
        password_hash = SimpleHasher.hash_password(password)
        try:
            self._db.insert_user(username, password_hash)
            return True, "Registration successful"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"


    def login_user(self, username: str, password: str) -> Tuple[bool, str, Optional[str]]:
        """Login a user. Returns (success, message, role)."""
        row = self._db.get_user(username)

        if row is None:
            return False, "User not found", None

        username_db, password_hash_db = row[0], row[1]

        if SimpleHasher.check_password(password, password_hash_db):
            return True, "Login successful", None

        return False, "Invalid password", None


    def get_user(self, username: str) -> Optional[User]:
        """Get User object by username."""
        row = self._db.get_user(username)
        if row is None:
            return None
        role = row[2] if len(row) >= 3 else "user"
        return User(row[0], row[1], role)

