import sqlite3
import argparse
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = '/home/mcipks/Desktop/New Folder 1/help_desk_system/database/help_desk.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def add_user(username, password, role):
    conn = get_db_connection()
    hashed_password = generate_password_hash(password)
    try:
        conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, hashed_password, role))
        conn.commit()
        print(f"User '{username}' added successfully with role '{role}'.")
    except sqlite3.IntegrityError:
        print(f"Error: User '{username}' already exists.")
    finally:
        conn.close()

def delete_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"User '{username}' deleted successfully.")
    else:
        print(f"Error: User '{username}' not found.")
    conn.close()

def list_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, username, role FROM users").fetchall()
    conn.close()
    if users:
        print("Existing Users:")
        for user in users:
            print(f"  ID: {user['id']}, Username: {user['username']}, Role: {user['role']}")
    else:
        print("No users found.")

def main():
    parser = argparse.ArgumentParser(description="Manage users for the Help Desk System.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add user command
    add_parser = subparsers.add_parser("add", help="Add a new user")
    add_parser.add_argument("username", help="Username for the new user")
    add_parser.add_argument("password", help="Password for the new user")
    add_parser.add_argument("role", choices=["employee", "technician"], help="Role of the new user (employee or technician)")

    # Delete user command
    delete_parser = subparsers.add_parser("delete", help="Delete an existing user")
    delete_parser.add_argument("username", help="Username of the user to delete")

    # List users command
    list_parser = subparsers.add_parser("list", help="List all existing users")

    args = parser.parse_args()

    if args.command == "add":
        add_user(args.username, args.password, args.role)
    elif args.command == "delete":
        delete_user(args.username)
    elif args.command == "list":
        list_users()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
