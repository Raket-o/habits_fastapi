#!/usr/bin/env bash

alembic downgrade head
uvicorn app.main:app --host 192.168.55.5 --port 8000 --reload
