# Backend and database explained (Member 1 viva notes)

## 1. How one request travels

`React form -> POST /api/emergencies -> router -> schema validation -> service -> SQLAlchemy -> MySQL`

| File | Job |
|---|---|
| `routers/emergencies.py` | defines the URLs; receives the request, returns the response |
| `schemas/emergency.py` | Pydantic classes; reject bad data before it reaches the database (HTTP 422) |
| `services/emergency_service.py` | the real work: create row, write history, create notifications, check status rules |
| `database/models.py` | Python classes = MySQL tables |
| `database/connection.py` | engine (connection to MySQL), session per request (`get_db`) |
| `config.py` | reads DB settings from `.env`; no password in code |
| `main.py` | creates the app, enables CORS, handles database errors, health check |

## 2. Tables and relationships

- `users` - staff accounts (role: admin, dispatcher, driver, hospital_staff). Login is not built yet.
- `hospitals` - name, location, beds, ICU/trauma flags.
- `ambulances` - registration, type, status, base hospital (FK), driver (FK to users), last known position.
- `emergency_requests` - the main table: caller, patient (optional), type, severity, status, location.
- `assignments` - links one emergency to one ambulance and a destination hospital (FKs to all three).
- `routes` - route of an assignment (distance, minutes, geometry); filled by OSRM later.
- `notifications` - message for a user, optionally linked to an emergency.
- `emergency_status_history` - one row for every status change (audit trail).

Relationships: one emergency has many assignments, history rows and notifications; one assignment has many routes;
one hospital has many ambulances. Deleting an emergency deletes its history/assignments (`ON DELETE CASCADE`);
deleting a user keeps the records and sets the user column to NULL (`SET NULL`); an ambulance that has assignments
cannot be deleted (`RESTRICT`).

Indexes: on `status`, `severity`, `created_at` (the columns the list and dashboard filter by), on every foreign key
that is searched, and unique indexes on email, registration number and hospital name.

## 3. Decisions you may be asked about

- **Status and severity are VARCHAR, not MySQL ENUM.** Adding a new value later then needs no `ALTER TABLE`.
  The allowed values are enforced in Python (enum classes + Pydantic).
- **Status order is enforced** in `ALLOWED_TRANSITIONS`: pending > assigned > en_route > at_scene > transporting > completed;
  cancelled is possible until transporting starts. Wrong jumps return HTTP 409.
- **Times are stored in UTC.** The frontend converts them to local time.
- **Alembic migrations** instead of `create_all()`: `create_all` cannot change existing tables. Migrations let the team
  add columns later (for example an AI severity column) without losing data.
- **Passwords are not stored yet.** Seed users have a placeholder in `password_hash`; real hashing comes with the login module.
- **SQL injection:** SQLAlchemy sends values as parameters, never as text glued into SQL.

## 4. Short answers

- *What is an ORM?* It maps tables to Python classes so we write Python instead of raw SQL.
- *What is a session?* One unit of work with the database; we commit to save, or roll back on error.
- *What is CORS?* A browser rule. The React app (port 5173) and the API (port 8000) are different origins, so the API must allow it.
- *Why dependency injection (`Depends(get_db)`)?* Every request gets its own session and it is always closed afterwards; tests can replace it.
- *What is HTTP 422 / 404 / 409 / 201?* Invalid data / not found / conflicting state (invalid status change) / created.

## 5. Adding a new feature (example: assign an ambulance)

1. Model exists (`assignments`). If a column is missing: edit `models.py`, run `alembic revision --autogenerate`, then `alembic upgrade head`.
2. Add a schema in `schemas/`, logic in `services/assignment_service.py`, URLs in a new router, then `include_router` in `main.py`.
3. Add a function in `frontend/src/api/`, and use it from a page.
4. Add a test in `backend/tests/`, and update `PROJECT_PROGRESS.md`.
