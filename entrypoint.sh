#!/bin/sh
set -e

echo "Waiting for database..."

# Wait for database to be ready
until pg_isready -h ${DATABASE_HOST:-ep-tiny-snowflake-abm0ymkb-pooler.eu-west-2.aws.neon.tech} -p ${DATABASE_PORT:-5432} -U ${DATABASE_USER:-store_owner} -d ${DATABASE_NAME:-store}; do
  echo "DB is unavailable - sleeping"
  sleep 2
done

echo "Running migrations..."
python manage.py migrate

echo "Starting server..."
exec uvicorn saleor.asgi:application --host=0.0.0.0 --port=8000 --workers=2 --lifespan=off --ws=none --no-server-header --no-access-log --timeout-keep-alive=35 --timeout-graceful-shutdown=30 --limit-max-requests=10000