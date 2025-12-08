import bcrypt
from app.data.db import connect_database

 # Read
def get_user_by_username(username):
    """Get a user by username."""

    # Connect to the database
    conn = connect_database()
    cursor = conn.cursor()

    # Execute parameterized query to find user by username
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    # Fetch the first matching row
    user = cursor.fetchone()

    # Close the database connection
    conn.close()
    
    return user

def verify_user(username, password):
   
    # Get user from database
    user = get_user_by_username(username)
    
    if not user:
        return False, None, "Username not found"
    
    # Extract password hash from user tuple
    stored_hash = user[2]  # password_hash is at index 2
    
    # Verify password with bcrypt
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')
    
    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, user, f"Welcome, {username}!"
    else:
        return False, None, "Invalid password"

    

# Update
def update_user_password(username, new_password_hash):
   
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        UPDATE users 
        SET password_hash = ? 
        WHERE username = ?
        """,
        (new_password_hash, username)
    )
    
    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()
    
    if rows_updated > 0:
        print(f"✅ Password updated for {username}")
    else:
        print(f"⚠️  User '{username}' not found")
    
    return rows_updated

def insert_user(username, password_hash):
    """Insert a new user."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    conn.commit()
    conn.close()

def update_user_password(username, new_password_hash):
   
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        UPDATE users 
        SET password_hash = ? 
        WHERE username = ?
        """,
        (new_password_hash, username)
    )
    
    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()
    
    if rows_updated > 0:
        print(f"✅ Password updated for {username}")
    else:
        print(f"⚠️  User '{username}' not found")
    
    return rows_updated


# Delete
def delete_user(username):
    
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        DELETE FROM users 
        WHERE username = ?
        """,
        (username,)
    )
    
    conn.commit()
    rows_deleted = cursor.rowcount
    
    conn.close()
    
    if rows_deleted > 0:
        print(f"✅ Deleted user '{username}'")
    else:
        print(f"⚠️  User '{username}' not found")
    
    return rows_deleted
