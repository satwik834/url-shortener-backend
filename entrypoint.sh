#!/bin/sh


echo "Waiting for database..."

until alembic upgrade head
do
  echo "Database not ready yet..."
  sleep 2
done

echo "Migrations successful."

echo "Starting server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000