import bcrypt
from pathlib import Path
from app.data.db import connect_database

def migrate_users_from_file(filepath='DATA/users.txt'):
    """
    Migrate users from users.txt to the database.
    """
    # Convert filepath to Path object
    filepath = Path(filepath)
    
    # Check if file exists
    if not filepath.exists():
        print(f"⚠️  File not found: {filepath}")
        print("   No users to migrate.")
        return 0
    
    # Connect to database
    conn = connect_database()
    cursor = conn.cursor()
    
    # Counter for migrated users
    migrated_count = 0
    
    # Read each line from users.txt
    with open(filepath, 'r') as f:
        for line in f:
            # Remove extra spaces and newlines
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Split line by comma: username,password_hash
            parts = line.split(',')
            
            # Make sure we have at least 2 parts
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                
                # Try to insert the user into database
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    
                    # If a row was inserted, increment counter
                    if cursor.rowcount > 0:
                        migrated_count += 1
                        print(f"  ✅ Migrated user: {username}")
                
                except Exception as e:
                    print(f"  ❌ Error migrating user {username}: {e}")
    
    # Save all changes to database
    conn.commit()
    conn.close()
    
    # Print final summary
    print(f"\n✅ Migrated {migrated_count} users from {filepath.name}")
    return migrated_count


def register_user(username, password, role='user'):
    """
    Register a new user with password hashing.
    """
    # Connect to database
    conn = connect_database()
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."
    
    # Hash the password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode('utf-8')
    
    # Insert new user into database
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    
    # Save changes
    conn.commit()
    conn.close()
    
    return True, f"User '{username}' registered successfully!"


def login_user(username, password):
    """
    Authenticate a user.
    """
    # Connect to database
    conn = connect_database()
    cursor = conn.cursor()
    
    # Find user by username
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    # Check if user exists
    if not user:
        return False, "User not found."
    
    # Get the password hash from database (3rd column, index 2)
    stored_hash = user[2]
    
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')
    
    # Check if password matches
    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."