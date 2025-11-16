import pandas as pd
from pathlib import Path
from app.data.db import connect_database

def load_csv_to_table(csv_path, table_name):
    """
    Load a CSV file into a database table.
    """
    # Convert to Path object
    csv_path = Path(csv_path)
    
    # Check if file exists
    if not csv_path.exists():
        print(f"⚠️  File not found: {csv_path}")
        return 0
    
    try:
        # Read CSV file using pandas
        df = pd.read_csv(csv_path)
        
        # Rename columns to match database table schema
        if table_name == "cyber_incidents":
            df = df.rename(columns={
                'incident_id': 'id',
                'timestamp': 'date',
                'category': 'incident_type',
                'description': 'description'
            })
            # Keep only the columns we need
            df = df[['id', 'date', 'incident_type', 'severity', 'status', 'description']]
        
        elif table_name == "datasets_metadata":
            df = df.rename(columns={
                'dataset_id': 'id',
                'name': 'dataset_name',
                'rows': 'record_count',
                'columns': 'file_size_mb',
                'uploaded_by': 'source'
            })
            # Keep only the columns we need
            df = df[['id', 'dataset_name', 'record_count', 'file_size_mb', 'source']]
        
        elif table_name == "it_tickets":
            df = df.rename(columns={
                'ticket_id': 'ticket_id',
                'description': 'subject',
                'created_at': 'created_date'
            })
            # Keep only the columns we need
            df = df[['ticket_id', 'priority', 'status', 'assigned_to', 'subject', 'created_date']]
        
        # Connect to database
        conn = connect_database()
        
        # Insert data into table
        # if_exists='append' means add to existing data (don't delete old data)
        # index=False means don't save the index as a column
        df.to_sql(table_name, conn, if_exists='append', index=False)
        
        # Close connection
        conn.close()
        
        # Print success message
        row_count = len(df)
        print(f"✅ Loaded {row_count} rows from {csv_path.name} into {table_name}")
        return row_count
        
    except Exception as e:
        print(f"❌ Error loading {csv_path.name}: {e}")
        return 0


def load_all_csv_data():
    """
    Load all CSV files into the database.
    """
    print("\n" + "=" * 70)
    print("LOADING CSV DATA")
    print("=" * 70 + "\n")
    
    total_rows = 0
    
    # Load cyber incidents
    print("[1] Loading cyber_incidents.csv...")
    rows = load_csv_to_table("DATA/cyber_incidents.csv", "cyber_incidents")
    total_rows += rows
    
    # Load datasets metadata
    print("\n[2] Loading datasets_metadata.csv...")
    rows = load_csv_to_table("DATA/datasets_metadata.csv", "datasets_metadata")
    total_rows += rows
    
    # Load IT tickets
    print("\n[3] Loading it_tickets.csv...")
    rows = load_csv_to_table("DATA/it_tickets.csv", "it_tickets")
    total_rows += rows
    
    print("\n" + "=" * 70)
    print(f"✅ TOTAL ROWS LOADED: {total_rows}")
    print("=" * 70 + "\n")
    
    return total_rows


if __name__ == "__main__":
    load_all_csv_data()