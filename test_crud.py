from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.data.incidents import (
    insert_incident, 
    get_all_incidents, 
    get_incident_by_id,
    get_incidents_by_severity,
    update_incident_status,
    update_incident_severity,
    delete_incident
)

print("\n" + "=" * 70)
print("🧪 TESTING CRUD OPERATIONS")
print("=" * 70)

# CREATE: Insert incidents
print("\n[1] CREATE - Insert New Incidents")
print("-" * 70)
id1 = insert_incident("2024-11-05", "Phishing", "High", "Open", "Suspicious email detected", "alice")
id2 = insert_incident("2024-11-06", "Malware", "Critical", "Investigating", "Ransomware detected", "bob")
id3 = insert_incident("2024-11-07", "DDoS", "Medium", "Open", "DDoS attack on main server", "charlie")

# READ: Get all incidents
print("\n[2] READ - Get All Incidents")
print("-" * 70)
df_all = get_all_incidents()
print(f"Total incidents: {len(df_all)}\n")
print(df_all.to_string())

# READ: Get specific incident
print("\n[3] READ - Get Incident by ID")
print("-" * 70)
get_incident_by_id(id1)

# READ: Filter by severity
print("\n[4] READ - Get Incidents by Severity")
print("-" * 70)
df_high = get_incidents_by_severity("High")
print(df_high.to_string())

# UPDATE: Change status
print("\n[5] UPDATE - Change Status")
print("-" * 70)
update_incident_status(id1, "Resolved")

# UPDATE: Change severity
print("\n[6] UPDATE - Change Severity")
print("-" * 70)
update_incident_severity(id3, "High")

# READ: Check updates
print("\n[7] READ - Verify Updates")
print("-" * 70)
df_updated = get_all_incidents()
print(df_updated.to_string())

# DELETE: Remove one incident
print("\n[8] DELETE - Remove One Incident")
print("-" * 70)
delete_incident(id3)

# READ: Check after delete
print("\n[9] READ - After Delete")
print("-" * 70)
df_final = get_all_incidents()
print(f"Total incidents remaining: {len(df_final)}\n")
print(df_final.to_string())

print("\n" + "=" * 70)
print("✅ CRUD TESTS COMPLETE")
print("=" * 70 + "\n")