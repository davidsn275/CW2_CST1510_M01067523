import sqlite3
from app.data.db import connect_database

def create_users_table(conn):
    """Create the users table."""
    cursor = conn.cursor()

    create_table_sql ="""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

     # Execute the SQL statement
    cursor.execute(create_table_sql)

    # Save the changes to the database
    conn.commit()

    print("Users table created successfully!")

def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table.
    """

    # Get a cursor from the connection
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        incident_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT NOT NULL,
        description TEXT,
        reported_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    
    # Execute the SQL statement
    cursor.execute(create_table_sql)

    # Commit the changes
    conn.commit()

    # Print success message
    print("Cyber incidents table created successfully!")


def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table if it doesn't exists
    """

    # Get a cursor to execute SQL commands
    cursor = conn.cursor()

    # SQL statement to create datasets_metadata table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT NOT NULL,
        category TEXT,
        source TEXT,
        last_updated TEXT,
        record_count INTEGER,
        file_size_mb REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    # Execute the SQL statement
    cursor.execute(create_table_sql)
    
    # Save the changes to the database
    conn.commit()
    
    # Print success message
    print("Datasets metadata table created successfully!")


def create_it_tickets_table(conn):
    """
    Create the datasets_metadata table
    """

    # Get a cursor to execute SQL commands
    cursor = conn.cursor()
    
    # SQL statement to create it_tickets table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL,
        category TEXT,
        subject TEXT NOT NULL,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    # Execute the SQL statement
    cursor.execute(create_table_sql)
    
    # Save the changes to the database
    conn.commit()
    
    # Print success message
    print("IT tickets table created successfully!")

def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)