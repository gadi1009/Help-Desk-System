#!/bin/bash

# Define source database path
DB_PATH="/home/mcipks/Desktop/New Folder 1/help_desk_system/database/help_desk.db"

# Define backup directory
BACKUP_DIR="/home/mcipks/Desktop/New Folder 1/help_desk_system/backups"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create a timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Define backup file name
BACKUP_FILE="$BACKUP_DIR/help_desk_backup_$TIMESTAMP.db"

# Copy the database file
cp "$DB_PATH" "$BACKUP_FILE"

echo "Database backup created: $BACKUP_FILE"
