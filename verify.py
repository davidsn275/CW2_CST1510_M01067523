from app.data.db import connect_database

def verify_migration():
    """
    Check that users were successfully migrated to the database.
    """
    # Connect to database
    conn = connect_database()
    cursor = conn.cursor()
    
    # Query all users from database
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    
    conn.close()
    
    # Print header
    print("\n" + "=" * 50)
    print("✅ USERS IN DATABASE")
    print("=" * 50)
    
    # Print column headers
    print(f"{'ID':<5} {'Username':<20} {'Role':<15}")
    print("-" * 50)
    
    # Print each user
    for user in users:
        user_id = user[0]      # First column: id
        username = user[1]     # Second column: username
        role = user[2]         # Third column: role
        
        print(f"{user_id:<5} {username:<20} {role:<15}")
    
    # Print summary
    print("-" * 50)
    print(f"Total users: {len(users)}")
    print("=" * 50 + "\n")
    
    return len(users)

if __name__ == "__main__":
    verify_migration()