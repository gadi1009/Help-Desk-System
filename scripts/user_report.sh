#!/bin/bash

echo "Generating user report..."

# Define database path (adjust as needed)
DB_PATH="./database/help_desk.db"

# Example: Querying user count
USER_COUNT=$(sqlite3 $DB_PATH "SELECT COUNT(*) FROM users;")
echo "Total users: $USER_COUNT"

# Example: Listing all users
echo "
All Users:"
sqlite3 $DB_PATH "SELECT username, role FROM users;"

echo "User report generation completed."
