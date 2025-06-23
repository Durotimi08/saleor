#!/bin/sh
set -e

echo "Starting Saleor container in debug mode..."

echo "Skipping database checks and migrations for debugging..."

echo "Starting server..."
echo "Server will be available on port ${PORT:-8000}"
exec uvicorn saleor.asgi:application --host=0.0.0.0 --port=${PORT:-8000} --workers=2 --lifespan=off --ws=none --no-server-header --no-access-log --timeout-keep-alive=35 --timeout-graceful-shutdown=30 --limit-max-requests=10000