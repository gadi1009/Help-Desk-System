#!/bin/bash

echo "Performing health check..."

# Define application URL (adjust as needed)
APP_URL="http://localhost:5000"
DB_PATH="./database/help_desk.db"

# Check if the application is reachable
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $APP_URL)
if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "Application is reachable (HTTP Status: $HTTP_STATUS)"
else
    echo "Application is NOT reachable (HTTP Status: $HTTP_STATUS)"
fi

# Check database connectivity (simple check for SQLite)
if [ -f "$DB_PATH" ]; then
    echo "Database file exists: $DB_PATH"
    # You could add a more robust check here, e.g., trying to query the DB
else
    echo "Database file NOT found: $DB_PATH"
fi

echo "Health check completed."
