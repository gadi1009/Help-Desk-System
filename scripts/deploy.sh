#!/bin/bash

echo "Starting deployment process..."

# Install/update dependencies
pip install -r ../requirements.txt

# Run database migrations
./db_migrate.sh

# Restart application services (example using pkill and nohup)
# This is a simple way to restart a development server.
# For production, you would use a process manager like Gunicorn or uWSGI.
pkill -f "flask run"
nohup flask run &

echo "Deployment process completed."
