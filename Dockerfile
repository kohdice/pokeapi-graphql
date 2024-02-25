# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  apt-transport-https \
  build-essential \
  curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE=false
SHELL ["/bin/bash", "-oeux", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python - \
  && cd /usr/local/bin \
  && ln -s /opt/poetry/bin/poetry \
  && poetry config virtualenvs.create false

WORKDIR /app

# Development stage
FROM base AS development

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-root

COPY . .

RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Production image
FROM base AS production

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-root --only main

ARG UID=10001
RUN adduser \
  --disabled-password \
  --gecos "" \
  --home "/nonexistent" \
  --shell "/sbin/nologin" \
  --no-create-home \
  --uid "${UID}" \
  appuser

USER appuser

COPY . .

EXPOSE 8000

CMD uvicorn 'pokeapi.main:app' --host=0.0.0.0 --port=8000
