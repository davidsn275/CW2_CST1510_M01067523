from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_services import migrate_users_from_file

print("\n" + "=" * 60)
print("SETTING UP DATABASE")
print("=" * 60)

# Step 1: Connect to database
print("\n[Step 1] Connecting to database...")
conn = connect_database()

# Step 2: Create all tables
print("\n[Step 2] Creating tables...")
create_all_tables(conn)
conn.close()

# Step 3: Migrate users from users.txt
print("\n[Step 3] Migrating users from users.txt...")
migrate_users_from_file()

print("\n" + "=" * 60)
print("✅ DATABASE SETUP COMPLETE!")
print("=" * 60 + "\n")