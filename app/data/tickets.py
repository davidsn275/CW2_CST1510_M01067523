import pandas as pd
from app.data.db import connect_database

def insert_ticket(ticket_id, priority, status, category, subject, description, created_date, assigned_to):
    """
    INSERT: Add a new ticket.
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO it_tickets 
        (ticket_id, priority, status, category, subject, description, created_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject, description, created_date, assigned_to))
    
    conn.commit()
    conn.close()


def get_all_tickets():
    """
    READ: Get all tickets.
    """
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df

# ==================== ANALYTICAL QUERIES ====================

def get_tickets_by_priority_count(conn=None):
    """
    Count tickets by priority level.
    """
    if conn is None:
        conn = connect_database()
    
    df = pd.read_sql_query("""
        SELECT priority, COUNT(*) as count
        FROM it_tickets
        GROUP BY priority
        ORDER BY count DESC
    """, conn)
    
    conn.close()
    return df


def get_tickets_by_status_count(conn=None):
    """
    Count tickets by status.
    """
    if conn is None:
        conn = connect_database()
    
    df = pd.read_sql_query("""
        SELECT status, COUNT(*) as count
        FROM it_tickets
        GROUP BY status
        ORDER BY count DESC
    """, conn)
    
    conn.close()
    return df


def get_critical_tickets(conn=None):
    """
    Get all CRITICAL priority tickets.
    """
    if conn is None:
        conn = connect_database()
    
    df = pd.read_sql_query("""
        SELECT * FROM it_tickets
        WHERE priority = 'Critical'
        ORDER BY created_date DESC
    """, conn)
    
    conn.close()
    return df


def get_open_tickets(conn=None):
    """
    Get all OPEN status tickets.
    """
    if conn is None:
        conn = connect_database()
    
    df = pd.read_sql_query("""
        SELECT * FROM it_tickets
        WHERE status = 'Open'
        ORDER BY created_date DESC
    """, conn)
    
    conn.close()
    return df


def get_tickets_assigned_to(assigned_to, conn=None):
    """
    Get all tickets assigned to a specific person.
    """
    if conn is None:
        conn = connect_database()
    
    df = pd.read_sql_query("""
        SELECT * FROM it_tickets
        WHERE assigned_to = ?
        ORDER BY created_date DESC
    """, conn, params=(assigned_to,))
    
    conn.close()
    return df


def get_tickets_count_total(conn=None):
    """
    Get total count of all tickets.
    """
    if conn is None:
        conn = connect_database()
    
    result = conn.execute("""
        SELECT COUNT(*) FROM it_tickets
    """).fetchone()
    
    conn.close()
    return result[0]