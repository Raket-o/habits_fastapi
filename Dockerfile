#FROM python:3.12
#
#RUN mkdir /app
#
#COPY requirements.txt /app/
#
#RUN python -m pip install --upgrade pip
#
#RUN python -m pip install -r /app/requirements.txt
#
#COPY . /app/
#
#WORKDIR /app

# Dockerfile

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip "poetry"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

#COPY ./requirements.txt .
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt

COPY ./config_data ./config_data
COPY alembic.ini alembic.ini
COPY alembic alembic
COPY .env .env
COPY ./app ./app

ENTRYPOINT ["./app/docker-entrypoint.sh"]
