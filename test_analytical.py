from app.data.incidents import (
    get_incidents_by_severity_count,
    get_incidents_by_status_count,
    get_incidents_by_type_count,
    get_critical_incidents,
    get_open_incidents,
    get_high_severity_by_status,
    get_incidents_count_total
)
from app.data.tickets import (
    get_tickets_by_priority_count,
    get_tickets_by_status_count,
    get_critical_tickets,
    get_open_tickets,
    get_tickets_assigned_to,
    get_tickets_count_total
)

print("\n" + "=" * 80)
print("🔍 ANALYTICAL QUERIES TEST")
print("=" * 80)

# ==================== CYBER INCIDENTS ANALYSIS ====================

print("\n" + "-" * 80)
print("CYBER INCIDENTS ANALYSIS")
print("-" * 80)

# Total incidents
total = get_incidents_count_total()
print(f"\n[1] Total Incidents: {total}\n")

# By severity
print("[2] Incidents by Severity:")
print("-" * 80)
df = get_incidents_by_severity_count()
print(df.to_string(index=False))

# By status
print("\n[3] Incidents by Status:")
print("-" * 80)
df = get_incidents_by_status_count()
print(df.to_string(index=False))

# By type
print("\n[4] Incidents by Type:")
print("-" * 80)
df = get_incidents_by_type_count()
print(df.to_string(index=False))

# Critical incidents
print("\n[5] All Critical Incidents:")
print("-" * 80)
df = get_critical_incidents()
print(f"Total critical: {len(df)}")
print(df[['id', 'date', 'incident_type', 'severity', 'status']].head(10).to_string(index=False))

# Open incidents
print("\n[6] All Open Incidents:")
print("-" * 80)
df = get_open_incidents()
print(f"Total open: {len(df)}")
print(df[['id', 'date', 'incident_type', 'severity', 'status']].head(10).to_string(index=False))

# High severity by status
print("\n[7] High Severity Incidents by Status:")
print("-" * 80)
df = get_high_severity_by_status()
print(df.to_string(index=False))

# ==================== IT TICKETS ANALYSIS ====================

print("\n" + "-" * 80)
print("IT TICKETS ANALYSIS")
print("-" * 80)

# Total tickets
total = get_tickets_count_total()
print(f"\n[8] Total Tickets: {total}\n")

# By priority
print("[9] Tickets by Priority:")
print("-" * 80)
df = get_tickets_by_priority_count()
print(df.to_string(index=False))

# By status
print("\n[10] Tickets by Status:")
print("-" * 80)
df = get_tickets_by_status_count()
print(df.to_string(index=False))

# Critical tickets
print("\n[11] All Critical Tickets:")
print("-" * 80)
df = get_critical_tickets()
print(f"Total critical: {len(df)}")
print(df[['ticket_id', 'priority', 'status', 'assigned_to']].head(10).to_string(index=False))

# Open tickets
print("\n[12] All Open Tickets:")
print("-" * 80)
df = get_open_tickets()
print(f"Total open: {len(df)}")
print(df[['ticket_id', 'priority', 'status', 'assigned_to']].head(10).to_string(index=False))

# Tickets for specific person
print("\n[13] Tickets Assigned to 'IT_Support_A':")
print("-" * 80)
df = get_tickets_assigned_to("IT_Support_A")
print(f"Total: {len(df)}")
print(df[['ticket_id', 'priority', 'status']].head(10).to_string(index=False))

print("\n" + "=" * 80)
print("✅ ANALYTICAL QUERIES TEST COMPLETE")
print("=" * 80 + "\n")