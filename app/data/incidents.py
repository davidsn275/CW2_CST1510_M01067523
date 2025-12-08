import pandas as pd
from pathlib import Path
from app.data.db import connect_database


DATA_DIR = Path("DATA")

def load_incidents_csv():
    """Load incidents from CSV file."""
    csv_file = DATA_DIR / "cyber_incidents.csv"
    if csv_file.exists():
        return pd.read_csv(csv_file)
    return pd.DataFrame()


def save_incidents_csv(df):
    """Save incidents to CSV file."""
    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(DATA_DIR / "cyber_incidents.csv", index=False)

# create 
def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """
    Insert a new cyber incident into the database.
    """
    # Connect to database
    conn = connect_database()
    cursor = conn.cursor()
    
    # Insert incident using parameterized query
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    
    # Save changes
    conn.commit()
    
    # Get the ID of inserted incident
    incident_id = cursor.lastrowid
    conn.close()
    
    print(f"✅ Incident #{incident_id} created successfully!")
    return incident_id



# Read
def get_all_incidents():
    """
    Get all incidents from the database.
    """
    # Connect to database
    conn = connect_database()
    
    # Read all incidents into DataFrame
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    
    conn.close()
    
    return df


def get_incident_by_id(incident_id):
    """
    Get a specific incident by ID.
    """
    # Connect to database
    conn = connect_database()
    cursor = conn.cursor()
    
    # Find incident by ID
    cursor.execute("SELECT * FROM cyber_incidents WHERE id = ?", (incident_id,))
    incident = cursor.fetchone()
    conn.close()
    
    if incident:
        print(f"✅ Found incident #{incident_id}")
        return incident
    else:
        print(f"❌ Incident #{incident_id} not found")
        return None


def get_incidents_by_severity(severity):
    """
    Get all incidents with specific severity.
    """
    # Connect to database
    conn = connect_database()
    
    # Read incidents with specific severity
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE severity = ? ORDER BY date DESC",
        conn,
        params=(severity,)
    )
    
    conn.close()
    
    print(f"✅ Found {len(df)} incidents with severity '{severity}'")
    return df


# Update

def update_incident_status(incident_id, new_status):
    """
    Change the status of an incident.
    """
    # Connect to database
    conn = connect_database()
    cursor = conn.cursor()
    
    # Update incident status
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )
    
    # Save changes
    conn.commit()
    
    # Check if incident was found and updated
    if cursor.rowcount > 0:
        print(f"✅ Incident #{incident_id} status updated to '{new_status}'")
        conn.close()
        return True
    else:
        print(f"❌ Incident #{incident_id} not found")
        conn.close()
        return False



# Delete 

def delete_incident(incident_id):
    """
    DELETE: Remove an incident from the database.
    """
    # Connect to database
    conn = connect_database()
    cursor = conn.cursor()
    
    # Delete incident by ID
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    
    # Save changes
    conn.commit()
    
    # Check if incident was found and deleted
    if cursor.rowcount > 0:
        print(f"✅ Incident #{incident_id} deleted successfully!")
        conn.close()
        return True
    else:
        print(f"❌ Incident #{incident_id} not found")
        conn.close()
        return False
    

#analytic queries
def get_incidents_by_severity_count(conn=None):
    """
    Count incidents by severity level.
    
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    if conn is None:
        conn = connect_database()
    
    df = pd.read_sql_query("""
        SELECT severity, COUNT(*) as count
        FROM cyber_incidents
        GROUP BY severity
        ORDER BY count DESC
    """, conn)
    

    conn.close()
    return df


def get_incidents_by_status_count(conn=None):
    """
    Count incidents by status.
    
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    if conn is None:
        conn = connect_database()
    
    df = pd.read_sql_query("""
        SELECT status, COUNT(*) as count
        FROM cyber_incidents
        GROUP BY status
        ORDER BY count DESC
    """, conn)
    
    conn.close()
    return df


def get_incidents_by_type_count(conn=None):
    """
    Count incidents by type.
    
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    if conn is None:
        conn = connect_database()
    
    df = pd.read_sql_query("""
        SELECT incident_type, COUNT(*) as count
        FROM cyber_incidents
        GROUP BY incident_type
        ORDER BY count DESC
    """, conn)
    
    conn.close()
    return df


def get_critical_incidents(conn=None):
    """
    Get all CRITICAL severity incidents.
    
    Uses: SELECT, FROM, WHERE, ORDER BY
    """
    if conn is None:
        conn = connect_database()
    
    df = pd.read_sql_query("""
        SELECT * FROM cyber_incidents
        WHERE severity = 'Critical'
        ORDER BY date DESC
    """, conn)
    

    conn.close()
    return df


def get_open_incidents(conn=None):
    """
    Get all OPEN status incidents.
    
    Uses: SELECT, FROM, WHERE, ORDER BY
    """
    if conn is None:
        conn = connect_database()
    
    df = pd.read_sql_query("""
        SELECT * FROM cyber_incidents
        WHERE status = 'Open'
        ORDER BY date DESC
    """, conn)
    
    conn.close()
    return df


def get_high_severity_by_status(conn=None):
    """
    Count HIGH severity incidents by status.
    
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    if conn is None:
        conn = connect_database()
    
    df = pd.read_sql_query("""
        SELECT status, COUNT(*) as count
        FROM cyber_incidents
        WHERE severity = 'High'
        GROUP BY status
        ORDER BY count DESC
    """, conn)
    
    conn.close()
    return df


def get_incidents_count_total(conn=None):
    """
    Get total count of all incidents.
    """
    if conn is None:
        conn = connect_database()
    
    result = conn.execute("""
        SELECT COUNT(*) FROM cyber_incidents
    """).fetchone()
    

    conn.close()
    return result[0]