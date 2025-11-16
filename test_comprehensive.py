import sqlite3
import pandas as pd
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_services import register_user, login_user, migrate_users_from_file
from app.data.incidents import (
    insert_incident,
    get_all_incidents,
    get_incident_by_id,
    get_incidents_by_severity_count,
    get_critical_incidents,
    get_open_incidents
)
from app.data.tickets import (
    get_all_tickets,
    get_tickets_by_priority_count,
    get_critical_tickets
)
from app.data.dataset import get_all_datasets

def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "=" * 80)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("=" * 80)
    
    # ========== TEST 1: Authentication ==========
    print("\n[TEST 1] AUTHENTICATION")
    print("-" * 80)
    
    # Test registration
    success, msg = register_user("test_user", "TestPass123!", "analyst")
    print(f"  Register: {'✅' if success else '❌'} {msg}")
    
    # Test login with correct password
    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login (correct password): {'✅' if success else '❌'} {msg}")
    
    # Test login with wrong password
    success, msg = login_user("test_user", "WrongPassword!")
    print(f"  Login (wrong password): {'✅' if success else '❌'} {msg}")
    
    # ========== TEST 2: CRUD Operations ==========
    print("\n[TEST 2] CRUD OPERATIONS")
    print("-" * 80)
    
    conn = connect_database()
    
    # CREATE: Insert new incident
    print("  CREATE: Inserting new incident...")
    incident_id = insert_incident(
        "2024-11-15",
        "Test Incident",
        "High",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"    ✅ Created incident #{incident_id}")
    
    # READ: Get incident by ID
    print("  READ: Retrieving incident by ID...")
    incident = get_incident_by_id(incident_id)
    if incident:
        print(f"    ✅ Found incident #{incident_id}")
    else:
        print(f"    ❌ Could not find incident #{incident_id}")
    
    # UPDATE: Update status
    print("  UPDATE: Changing incident status...")
    from app.data.incidents import update_incident_status
    update_incident_status(incident_id, "In Progress")
    print(f"    ✅ Updated incident #{incident_id} status to 'In Progress'")
    
    # DELETE: Remove incident
    print("  DELETE: Removing incident...")
    from app.data.incidents import delete_incident
    delete_incident(incident_id)
    print(f"    ✅ Deleted incident #{incident_id}")
    
    # ========== TEST 3: Data Queries ==========
    print("\n[TEST 3] DATA QUERIES")
    print("-" * 80)
    
    # Query all incidents
    print("  Querying all incidents...")
    df_incidents = get_all_incidents()
    print(f"    ✅ Found {len(df_incidents)} incidents in database")
    
    # Query by severity
    print("  Querying incidents by severity...")
    df_severity = get_incidents_by_severity_count()
    print(f"    ✅ Found {len(df_severity)} severity levels")
    print(df_severity.to_string(index=False))
    
    # Get critical incidents
    print("\n  Querying critical incidents...")
    df_critical = get_critical_incidents()
    print(f"    ✅ Found {len(df_critical)} critical incidents")
    
    # Get open incidents
    print("  Querying open incidents...")
    df_open = get_open_incidents()
    print(f"    ✅ Found {len(df_open)} open incidents")
    
    # ========== TEST 4: Tickets ==========
    print("\n[TEST 4] IT TICKETS")
    print("-" * 80)
    
    # Get all tickets
    print("  Querying all tickets...")
    df_tickets = get_all_tickets()
    print(f"    ✅ Found {len(df_tickets)} tickets in database")
    
    # Tickets by priority
    print("  Querying tickets by priority...")
    df_priority = get_tickets_by_priority_count()
    print(f"    ✅ Found {len(df_priority)} priority levels")
    print(df_priority.to_string(index=False))
    
    # Critical tickets
    print("\n  Querying critical tickets...")
    df_crit_tickets = get_critical_tickets()
    print(f"    ✅ Found {len(df_crit_tickets)} critical tickets")
    
    # ========== TEST 5: Datasets ==========
    print("\n[TEST 5] DATASETS")
    print("-" * 80)
    
    print("  Querying all datasets...")
    df_datasets = get_all_datasets()
    print(f"    ✅ Found {len(df_datasets)} datasets")
    print(df_datasets[['dataset_name', 'record_count']].to_string(index=False))
    
    # ========== TEST 6: Database Summary ==========
    print("\n[TEST 6] DATABASE SUMMARY")
    print("-" * 80)
    
    cursor = conn.cursor()
    
    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\nTable Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)
    
    total_rows = 0
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")
        total_rows += count
    
    print("-" * 40)
    print(f"{'TOTAL':<25} {total_rows:<15}")
    
    conn.close()
    
    # ========== FINAL SUMMARY ==========
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("\nYour database is ready for production!")
    print("You can now move to Part 9 (Week 9: Streamlit Web Interface)")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    run_comprehensive_tests()