#!/bin/sh
ENV=dev uvicorn app.server:app --host 127.0.0.1 --port 8080 --workers 1 --reload
