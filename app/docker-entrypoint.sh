#!/usr/bin/env bash

alembic upgrade head
#uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
uvicorn app.main:app --host 192.168.55.5 --port 8000 --reload
