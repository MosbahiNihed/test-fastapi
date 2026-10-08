# test-fastapi

FastAPI service with a PostgreSQL database. Liquibase manages the schema and
data migrations, and pgAdmin gives you a UI to look at the database.

## Run the stack

```bash
cp .env.example .env    # optional: change credentials/ports
docker compose up -d --build
```

| Service    | URL                         | Notes                                          |
|------------|-----------------------------|------------------------------------------------|
| API        | http://localhost:8000/docs  | Swagger UI                                     |
| pgAdmin    | http://localhost:5050       | `admin@example.com` / `admin`; add server host `postgres`, user/password `app` |
| PostgreSQL | localhost:5432              | db/user/password: `app`                        |

If a port is already taken, override it with `POSTGRES_PORT`, `PGADMIN_PORT`, or `APP_PORT`.

Startup order: `postgres` (healthy) → `liquibase update` (runs once and exits) → `app`.

## Migrations (Liquibase)

The changelogs live in `db/changelog/` and are baked into the Liquibase image (`db/Dockerfile`). To add a migration, create
`db/changelog/changes/NNN-description.yaml` and include it in
`db.changelog-master.yaml`. **Never edit a changeset that has already run.**
Add a new one instead.

```bash
docker compose build liquibase                  # rebuild after changing changelogs
docker compose run --rm liquibase               # apply pending changesets
docker compose run --rm liquibase status        # list pending changesets
docker compose run --rm liquibase rollback-count 1   # roll back the last changeset
```

Seed data (`002-seed-users`) uses the `dev` context. To skip it, set `LIQUIBASE_CONTEXTS=prod`.

## User CRUD

| Method | Path            | Description                     |
|--------|-----------------|---------------------------------|
| POST   | `/users`        | Create a user (409 if the email is taken) |
| GET    | `/users`        | List users (`skip`, `limit`)    |
| GET    | `/users/{id}`   | Get one user                    |
| PATCH  | `/users/{id}`   | Partial update                  |
| DELETE | `/users/{id}`   | Delete a user                   |

## Tests

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

Tests use in-memory SQLite, so you don't need a database running.
