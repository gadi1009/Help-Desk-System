import sqlite3
import sys

DATABASE = '/home/mcipks/Desktop/New Folder 1/help_desk_system/database/help_desk.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def assign_and_prioritize_tickets():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all technicians
    technicians = conn.execute("SELECT id FROM users WHERE role = 'technician'").fetchall()
    if not technicians:
        print("No technicians found in the database. Cannot assign tickets.")
        conn.close()
        return
    technician_ids = [tech['id'] for tech in technicians]
    current_technician_index = 0

    # Fetch new tickets
    new_tickets = conn.execute("SELECT ticket_id, title, description, urgency FROM tickets WHERE status = 'New'").fetchall()

    if not new_tickets:
        print("No new tickets to assign or prioritize.")
        conn.close()
        return

    print(f"Found {len(new_tickets)} new tickets.")

    for ticket in new_tickets:
        ticket_id = ticket['ticket_id']
        title = ticket['title'].lower()
        description = ticket['description'].lower()
        current_urgency = ticket['urgency']

        # Simple prioritization logic based on keywords
        new_urgency = current_urgency
        if "urgent" in title or "urgent" in description or \
           "critical" in title or "critical" in description:
            new_urgency = 'High'
        elif "slow" in title or "slow" in description or \
             "performance" in title or "performance" in description:
            if new_urgency != 'High': # Don't downgrade from High
                new_urgency = 'Medium'

        # Assign to next technician in a round-robin fashion
        assigned_technician_id = technician_ids[current_technician_index]
        current_technician_index = (current_technician_index + 1) % len(technician_ids)

        # Update ticket status, urgency, and assign to technician
        cursor.execute(
            "UPDATE tickets SET status = ?, urgency = ?, user_id = ? WHERE ticket_id = ?",
            ('In Progress', new_urgency, assigned_technician_id, ticket_id)
        )
        print(f"Ticket {ticket_id}: Assigned to technician {assigned_technician_id}, Urgency set to {new_urgency}.")

    conn.commit()
    conn.close()
    print("Ticket assignment and prioritization complete.")

if __name__ == "__main__":
    assign_and_prioritize_tickets()
