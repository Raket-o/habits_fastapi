#!/usr/bin/env bash

alembic upgrade head
uvicorn app.main:app --host 192.168.55.5 --port 8000 --reload
