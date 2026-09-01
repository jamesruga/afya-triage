#!/bin/bash
export PYTHONPATH=.
exec gunicorn --workers 2 --bind 0.0.0.0:8000 src.api:app
