import sqlite3
import pandas as pd
from pathlib import Path
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_services import migrate_users_from_file
from app.data.incidents import get_all_incidents, get_incidents_count_total
from app.data.dataset import get_all_datasets
from app.data.tickets import get_all_tickets

def load_csv_to_table(csv_path, table_name):
    """
    Load a CSV file into a database table.
    """
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        print(f"⚠️  File not found: {csv_path}")
        return 0
    
    try:
        # Read CSV file using pandas
        df = pd.read_csv(csv_path)
        
        # Rename columns to match database schema
        if table_name == "cyber_incidents":
            df = df.rename(columns={
                'incident_id': 'id',
                'timestamp': 'date',
                'category': 'incident_type'
            })
            df = df[['id', 'date', 'incident_type', 'severity', 'status', 'description']]
        
        elif table_name == "datasets_metadata":
            df = df.rename(columns={
                'dataset_id': 'id',
                'name': 'dataset_name',
                'rows': 'record_count',
                'columns': 'file_size_mb',
                'uploaded_by': 'source'
            })
            df = df[['id', 'dataset_name', 'record_count', 'file_size_mb', 'source']]
        
        elif table_name == "it_tickets":
            df = df.rename(columns={
                'description': 'subject',
                'created_at': 'created_date'
            })
            df = df[['ticket_id', 'priority', 'status', 'assigned_to', 'subject', 'created_date']]
        
        # Connect to database
        conn = connect_database()
        
        # Insert data into table
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.close()
        
        row_count = len(df)
        print(f"  ✅ Loaded {row_count} rows into {table_name}")
        return row_count
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return 0


def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" + "=" * 80)
    print("🚀 COMPLETE DATABASE SETUP")
    print("=" * 80)
    
    # ========== STEP 1: Connect and Create Tables ==========
    print("\n[STEP 1] Creating Database Tables...")
    print("-" * 80)
    try:
        conn = connect_database()
        create_all_tables(conn)
        conn.close()
        print("✅ All tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return
    
    # ========== STEP 2: Migrate Users ==========
    print("\n[STEP 2] Migrating Users from users.txt...")
    print("-" * 80)
    try:
        migrate_users_from_file()
    except Exception as e:
        print(f"❌ Error migrating users: {e}")
        return
    
    # ========== STEP 3: Load CSV Data ==========
    print("\n[STEP 3] Loading CSV Data...")
    print("-" * 80)
    total_rows = 0
    
    print("Loading cyber_incidents.csv...")
    rows = load_csv_to_table("DATA/cyber_incidents.csv", "cyber_incidents")
    total_rows += rows
    
    print("Loading datasets_metadata.csv...")
    rows = load_csv_to_table("DATA/datasets_metadata.csv", "datasets_metadata")
    total_rows += rows
    
    print("Loading it_tickets.csv...")
    rows = load_csv_to_table("DATA/it_tickets.csv", "it_tickets")
    total_rows += rows
    
    # ========== STEP 4: Verify Data ==========
    print("\n[STEP 4] Verifying Data...")
    print("-" * 80)
    
    conn = connect_database()
    cursor = conn.cursor()
    
    # Count users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM cyber_incidents")
    incident_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM datasets_metadata")
    dataset_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM it_tickets")
    ticket_count = cursor.fetchone()[0]
    
    conn.close()
    
    # Print summary
    print(f"\nDatabase Summary:")
    print(f"  👥 Users: {user_count}")
    print(f"  🚨 Cyber Incidents: {incident_count}")
    print(f"  📊 Datasets: {dataset_count}")
    print(f"  🎫 IT Tickets: {ticket_count}")
    
    # ========== FINAL SUMMARY ==========
    print("\n" + "=" * 80)
    print("✅ DATABASE SETUP COMPLETE!")
    print("=" * 80)
    print(f"\nTotal Data Loaded: {total_rows} rows")
    print(f"Database Location: DATA/intelligence_platform.db")
    print("\nYou can now use the database with:")
    print("  - app/data/incidents.py")
    print("  - app/data/datasets.py")
    print("  - app/data/tickets.py")
    print("  - app/services/user_service.py")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    setup_database_complete()