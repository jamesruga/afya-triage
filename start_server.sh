#!/bin/bash
# Clean up any existing Gunicorn processes on port 8000
pkill -f gunicorn 2>/dev/null || true
sleep 1

echo "Starting Afya Triage Gunicorn WSGI Server..."
exec gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 60 "src.api:app"
