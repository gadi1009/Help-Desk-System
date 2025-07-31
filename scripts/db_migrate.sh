#!/bin/bash

echo "Starting database migration..."

# Initialize the database using Flask's command-line interface
flask initdb

echo "Database migration completed."
