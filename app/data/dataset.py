import pandas as pd
import sqlite3
from pathlib import Path
from app.data.db import connect_database

# Set up the data directory path where CSV files will be stored
DATA_DIR = Path("DATA")

# CSV file operations

def load_datasets_csv():
    """Load datasets from CSV file."""
    # Check if the CSV file exists in the DATA directory
    csv_file = DATA_DIR / "datasets_metadata.csv"
    if csv_file.exists():
        return pd.read_csv(csv_file)
    return pd.DataFrame()

def save_datasets_csv(df):
    """Save datasets to CSV file."""
    # Create DATA directory if it doesn't exist
    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(DATA_DIR / "datasets_metadata.csv", index=False)


# create operations
def insert_dataset(dataset_name, category, source, last_updated, record_count, file_size_mb):
    """
    INSERT: Add a new dataset.
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO datasets_metadata 
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    

    # Save changes to database
    conn.commit()
    conn.close()


# Read operations
def get_all_datasets():
    """
    READ: Get all datasets.
    """
    conn = connect_database()
    # Use pandas to read SQL query directly into dataframe
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df


def get_dataset_by_id(dataset_id):
    """
    READ: Get dataset by ID.
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM datasets_metadata WHERE id = ?",
        (dataset_id,)
    )
    dataset = cursor.fetchone()
    conn.close()
    return dataset


def get_datasets_by_category(category):
    """
    READ: Get datasets filtered by category.
    """
    conn = connect_database()
    # Use pandas to filter and order results
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata WHERE category = ? ORDER BY id DESC",
        conn,
        params=(category,)
    )
    conn.close()
    return df


def get_datasets_by_source(source):
    """
    READ: Get datasets filtered by source.
    """
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata WHERE source = ? ORDER BY id DESC",
        conn,
        params=(source,)
    )
    conn.close()
    return df


def get_total_data_size():
    """
    READ: Get total size of all datasets in GB.
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(file_size_mb) FROM datasets_metadata")
    result = cursor.fetchone()
    conn.close()
    
    total_mb = result[0] if result[0] is not None else 0
    return round(total_mb / 1024, 2)


def count_datasets_by_category():
    """
    READ: Get count of datasets grouped by category for analytics.
    """
    conn = connect_database()
    df = pd.read_sql_query("""
        SELECT category, COUNT(*) as count
        FROM datasets_metadata
        GROUP BY category
        ORDER BY count DESC
    """, conn)
    conn.close()
    return df


def get_largest_datasets(limit=5):
    """
    READ: Get the largest datasets by file size.
    """
    conn = connect_database()
    df = pd.read_sql_query("""
        SELECT dataset_name, file_size_mb, category
        FROM datasets_metadata
        ORDER BY file_size_mb DESC
        LIMIT ?
    """, conn, params=(limit,))
    conn.close()
    return df


def get_dataset_summary():
    """
    READ: Get summary statistics for dashboard.
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM datasets_metadata")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(record_count) FROM datasets_metadata")
    total_records = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(file_size_mb) FROM datasets_metadata")
    total_size_mb = cursor.fetchone()[0] or 0
    total_size_gb = round(total_size_mb / 1024, 2)
    
    cursor.execute("""
        SELECT category FROM datasets_metadata 
        GROUP BY category 
        ORDER BY COUNT(*) DESC LIMIT 1
    """)
    most_common = cursor.fetchone()
    most_common_cat = most_common[0] if most_common else "N/A"
    
    conn.close()
    
    return {
        'total_datasets': total,
        'total_records': total_records,
        'total_size_gb': total_size_gb,
        'most_common_category': most_common_cat
    }



# UPDATE - Modify Dataset
def update_dataset_category(dataset_id, new_category):
    """
    UPDATE: Change dataset category.
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE datasets_metadata SET category = ? WHERE id = ?",
        (new_category, dataset_id)
    )
    
    conn.commit()
    conn.close()




def update_dataset_size(dataset_id, new_size_mb):
    """
    UPDATE: Change dataset file size.
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE datasets_metadata SET file_size_mb = ? WHERE id = ?",
        (new_size_mb, dataset_id)
    )
    
    conn.commit()
    conn.close()


def update_dataset_last_updated(dataset_id, new_date):
    """
    UPDATE: Change dataset last updated date.
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE datasets_metadata SET last_updated = ? WHERE id = ?",
        (new_date, dataset_id)
    )
    
    conn.commit()
    conn.close()



# DELETE
def delete_dataset(dataset_id):
    """
    DELETE: Remove a dataset from database.
    """
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM datasets_metadata WHERE id = ?",
        (dataset_id,)
    )


     # Commit the delet   
    conn.commit()
    conn.close()
