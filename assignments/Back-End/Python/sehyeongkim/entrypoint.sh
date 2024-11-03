#!/bin/sh
/src/wait-for-it.sh mysql:3306 -t 60
poetry run  alembic upgrade head
poetry run uvicorn app.server:app --host 0.0.0.0 --port 8080
