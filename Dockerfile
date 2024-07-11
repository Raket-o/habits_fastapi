FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip "poetry"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY ./config_data ./config_data
COPY alembic.ini alembic.ini
COPY alembic alembic
COPY .env .env
COPY ./app ./app

ENTRYPOINT ["./app/docker-entrypoint.sh"]
