# pokeapi-graphql

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![codecov](https://codecov.io/gh/kohdice/pokeapi-graphql/graph/badge.svg?token=01EPH5KG7V)](https://codecov.io/gh/kohdice/pokeapi-graphql)

GraphQL API of Pokédex

## 1. Table of Contents

- [1. Table of Contents](#1-table-of-contents)
- [2. About This Repository](#2-about-this-repository)
- [3. Usage](#3-usage)
  - [a. Install Docker](#a-install-docker)
  - [b. Clone Repository](#b-clone-repository)
  - [c. Run servers](#c-run-servers)
  - [d. Database Migration](#d-database-migration)
  - [e. Health Check](#e-health-check)

## 2. About This Repository

This is a repository for a GraphQL API that returns Pokémon data,
created with [FastAPI](https://fastapi.tiangolo.com/) and [Strawberry](https://strawberry.rocks/).

## 3. Usage

### a. Install Docker

Download and install Docker Desktop from the [Docker official website](https://www.docker.com/products/docker-desktop/).

### b. Clone Repository

[Clone this repository]([https://github.com/kohdice/pokeapi-graphql](https://github.com/kohdice/pokeapi-graphql))
to your development machine and create a local repository

### c. Run Servers

Execute the following command.

```bash
docker compose up --build
```

### d. Database Migration

Execute the following command within the `app` container.

```bash
docker compose exec app bash
task migrate
```

### e. Health Check

Execute the following command.

```bash
curl -X GET http://localhost:8000/health
```

If `{"status": "OK"}` is returned, server setup is successful.

## Scripts

Run the following commands in the Docker container.

- Run tests (Testing by pytest)

```bash
task test
```

- Run formatters (Formatting by ruff)

```bash
task fmt
```

- Run linters (Static code analysis by ruff)

```bash
task lint
```
