# DOLY — Architecture

Last updated: 2026-01-06

## Overview

DOLY is a monolithic web application built with Flask. The project follows a clear separation of concerns: request routing and controllers (Flask blueprints), persistence (SQLAlchemy models), templates (Jinja2), and static assets (SCSS → CSS, JS). The schema is managed as SQL DDL in `app/utilities/Documentation/Database/ServiceDDL.sql` and example seed data in `ServiceDML.sql`.

## High-level components

- Application factory: `app/__init__.py` constructs the Flask app, configures extensions, and registers Blueprints.
- Blueprints: logical areas are separated (e.g., `views`, `auth`) so routes and templates remain modular.
- Database: PostgreSQL accessed via Flask-SQLAlchemy (`app/database.py`). Models live in `app/models/`, each entity in its own module and using `@dataclass` + `db.Model`.
- Templates: Jinja2 templates under `app/templates/` grouped by feature (auth, landpage, admin, client).
- Static assets: compiled CSS and JS in `app/static/` (SCSS sources under `app/static/scss/` when present).
- Documentation & scripts: DDL, DML and ERD diagrams are in `app/utilities/Documentation/Database/`.

## Request flow

1. Client issues HTTP request to Flask (served via dev server, gunicorn, or WSGI host).
2. Flask routes the request to the appropriate Blueprint view.
3. Views interact with SQLAlchemy models and services to perform business logic.
4. Responses are rendered via templates or returned as JSON for API endpoints.

## Data model & schema

- The canonical database schema is defined in `ServiceDDL.sql` (PostgreSQL). Models in `app/models/` mirror that DDL and include `CHECK` constraints and `server_default` clauses where applicable.
- Use the provided DML for seeding sample data: `ServiceDML.sql`. For production, prefer Alembic migrations rather than raw DDL execution.

## Development setup

- Use a Python virtual environment and install dependencies from `requirements.txt`.
- Configure `DATABASE_URL` and `SECRET_KEY` in a `.env` file or environment variables.
- Run the DDL once to create schema, then seed with DML for local testing.

## Deployment recommendations

- Production server: `gunicorn` behind a reverse proxy (NGINX). Use multiple worker processes and keep static assets served by CDN or object storage.
- TLS: terminate TLS at the proxy or load balancer with HSTS.
- Secrets: store `DATABASE_URL`, `SECRET_KEY`, and API credentials in a secrets manager or environment variables (never commit `.env`).
- Migrations: adopt Alembic for schema evolution; commit migration scripts to VCS.

## Observability & maintenance

- Logs: application logs are written to `app/utilities/logs/` and stdout. Integrate with a centralized logging system for production.
- Health checks: add a lightweight `/health` endpoint that verifies DB connectivity and basic app readiness.

## Notes & caveats

- Password hashing: the project uses Werkzeug hashing; the SQL seed intentionally avoids pgcrypto so credential management is handled in the app layer.
- Model import checks: there are utility commands in `app/utilities/README.md` to verify Python imports of `app.models` after changes.

---

If you want, I can:
- Generate an `ARCHITECTURE.md` version in English.
- Add an `arch/diagrams` folder with the ERD exported as PNG/SVG from the Mermaid source.
