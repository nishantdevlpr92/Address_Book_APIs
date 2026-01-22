#!/bin/bash

# Entry script for Docker container
# This script handles database initialization and starts the application

set -e

echo "Starting Address Book API..."

# Create data directory if it doesn't exist
mkdir -p /app/data

# Run database migrations/initialization
echo "Initializing database..."
python -c "
from app.db.base import engine
from sqlmodel import SQLModel
SQLModel.metadata.create_all(engine)
print('Database tables created successfully!')
"   

echo "Starting FastAPI server..."
exec "$@"