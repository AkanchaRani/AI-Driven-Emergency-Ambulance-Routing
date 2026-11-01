# Team setup guide (Windows 11, PowerShell)

Do this once on every team member's laptop. Open the project folder in VS Code and use
**Terminal > New Terminal** (PowerShell).

## 1. Software to install

| Software | Version | Check with |
|---|---|---|
| Python | 3.11 or 3.12 (tick "Add python.exe to PATH" in the installer) | `python --version` |
| Node.js | 20 LTS or newer | `node --version` |
| MySQL Server | **8.0** (remember the root password you set) | `mysql --version` |
| VS Code | latest | |
| Postman | latest (optional) | |

If `mysql` is not recognised, add `C:\Program Files\MySQL\MySQL Server 8.0\bin` to your PATH, or use MySQL Workbench.

## 2. Create the .env file

Run from the project root folder:

```powershell
Copy-Item .env.example .env
notepad .env
```

Set `DB_USER` and `DB_PASSWORD` to your MySQL login. Leave the other values unless MySQL uses a different port.
`.env` is private and is ignored by Git. Never send it to anyone or upload it.

## 3. Create the database (optional step)

The next step creates the database automatically. To do it by hand instead:

```powershell
mysql -u root -p -e "source database/database.sql"
```

## 4. Backend: install and start

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.database.initialize_db
uvicorn app.main:app --reload
```

- If PowerShell blocks `Activate.ps1`, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then retry.
- `initialize_db` creates the database (if missing), creates/updates all tables and inserts sample data only into empty tables.
  It is safe to run again at any time; it never deletes data.
- API is now at http://localhost:8000 and its documentation at http://localhost:8000/docs.

## 5. Frontend: install and start (second terminal)

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The green dot at the bottom of the sidebar means the backend and database are connected.

## 6. Test the APIs

**Browser:** open http://localhost:8000/api/health - you should see `"database":"connected"`.

**FastAPI docs:** http://localhost:8000/docs, click an endpoint, then "Try it out".

**PowerShell:**

```powershell
Invoke-RestMethod http://localhost:8000/api/health

$body = @{ caller_name="Test Caller"; caller_phone="9000000000"; emergency_type="accident";
           severity="high"; location_address="Test Street 1, Demo City" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/emergencies -ContentType "application/json" -Body $body
```

**Postman:** create a request `POST http://localhost:8000/api/emergencies`, Body > raw > JSON, paste the JSON
`{"caller_name":"Test Caller","caller_phone":"9000000000","emergency_type":"accident","severity":"high","location_address":"Test Street 1, Demo City"}`.
Expect status 201. Send invalid data (for example `"caller_phone":"abc"`) to see the 422 validation error.

**Automated tests:** `cd backend` then `python -m pytest`.

## 7. Check that data is saved in MySQL

```powershell
mysql -u root -p ambulance_routing_db -e "SELECT id, caller_name, severity, status, created_at FROM emergency_requests ORDER BY id DESC LIMIT 5;"
mysql -u root -p ambulance_routing_db -e "SELECT * FROM emergency_status_history ORDER BY id DESC LIMIT 5;"
```

Or open MySQL Workbench, connect, and browse `ambulance_routing_db`.

## 8. Changing the database later (migrations)

Never delete and recreate the database for a change. Edit `backend/app/database/models.py`, then:

```powershell
cd backend
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

Open the new file in `backend/alembic/versions/` and read it before upgrading. Commit it to Git so every team member
gets the change by running `alembic upgrade head` (or `python -m app.database.initialize_db`).

## 9. Common problems

| Problem | Fix |
|---|---|
| `Access denied for user` | wrong `DB_USER` / `DB_PASSWORD` in `.env` |
| `Can't connect to MySQL server` | MySQL service is not running (Services > MySQL80 > Start) |
| `DB_USER is not set` | `.env` is missing or not in the project root folder |
| Sidebar shows "Backend not reachable" | FastAPI is not running, or a different port is used (see `frontend/.env.example`) |
| Browser CORS error | frontend runs on another port; add it to `CORS_ORIGINS` in `.env` and restart uvicorn |
| `cryptography` error with MySQL 8 | run `pip install -r requirements.txt` again inside the activated venv |
