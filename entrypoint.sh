#!/bin/sh
set -e

echo "Starting Saleor container..."

# Function to check if database is reachable
check_database() {
  echo "Checking database connectivity..."
  if pg_isready -h ${DATABASE_HOST:-ep-tiny-snowflake-abm0ymkb-pooler.eu-west-2.aws.neon.tech} -p ${DATABASE_PORT:-5432} -U ${DATABASE_USER:-store_owner} -d ${DATABASE_NAME:-store} -t 10; then
    echo "Database is ready!"
    return 0
  else
    echo "Database is not ready or unreachable"
    return 1
  fi
}

# Try to wait for database with timeout
echo "Waiting for database..."
timeout_counter=0
max_timeout=60  # 60 seconds timeout

while ! check_database && [ $timeout_counter -lt $max_timeout ]; do
  echo "DB is unavailable - sleeping (attempt $((timeout_counter + 1))/$max_timeout)"
  sleep 2
  timeout_counter=$((timeout_counter + 2))
done

if [ $timeout_counter -ge $max_timeout ]; then
  echo "WARNING: Database timeout reached. Proceeding without database check..."
fi

# Try to run migrations
echo "Running migrations..."
if python manage.py migrate --noinput; then
  echo "Migrations completed successfully"
else
  echo "WARNING: Migrations failed, but continuing..."
fi

echo "Starting server..."
echo "Server will be available on port 8000"
exec uvicorn saleor.asgi:application --host=0.0.0.0 --port=8000 --workers=2 --lifespan=off --ws=none --no-server-header --no-access-log --timeout-keep-alive=35 --timeout-graceful-shutdown=30 --limit-max-requests=10000