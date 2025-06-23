#!/bin/bash
# Run DB migrations first
python manage.py migrate

# Then exec the original CMD (pass all args)
exec uvicorn saleor.asgi:application \
  --host=0.0.0.0 --port=8000 \
  --workers=2 --lifespan=off --ws=none \
  --no-server-header --no-access-log \
  --timeout-keep-alive=35 --timeout-graceful-shutdown=30 \
  --limit-max-requests=10000
