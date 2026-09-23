# How to Use This Project

Online consultation platform for Dr. Nituparna Sarkar's veterinary practice. Pet owners register,
add their pets and book consultations; the doctor manages them from an admin dashboard.

- **Frontend:** React + TypeScript + Vite (`src/`)
- **Backend:** FastAPI + PostgreSQL (`backend/`)

## Prerequisites

- **Node.js** 20.19+ or 22.12+: https://nodejs.org
- **Python** 3.11+: https://www.python.org/downloads/
- **PostgreSQL**, installed and running. On macOS: `brew install postgresql@16 && brew services start postgresql@16`

## Setup and run

**1. Clone**

```bash
git clone <this-repo-url>
cd vet_online_consultancy
```

**2. Backend** (terminal 1)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://localhost:8000 (interactive docs at http://localhost:8000/docs).

On startup the backend creates the `vet_online_consultancy` database if it doesn't exist, applies all
migrations, and generates a `JWT_SECRET` (the key that signs login tokens) into `backend/.env`.
You don't need to configure anything.

**3. Frontend** (terminal 2, from the project root)

```bash
npm install
npm run dev
```

Open **http://localhost:5173**.

**4. Create the doctor's admin account** (once, in a third terminal)

```bash
cd backend
source .venv/bin/activate
ADMIN_EMAIL='doctor@example.com' ADMIN_PASSWORD='a-strong-password' python -m scripts.seed_admin
```

Re-running it with the same email resets the password.

## Using the app

| Page | Who | What |
|---|---|---|
| `/register` | Pet owners | Create an account |
| `/login` | Everyone | Sign in (the doctor uses the admin account) |
| `/book` | Pet owners | Book a consultation |
| `/appointments` | Pet owners | See your appointments |
| `/admin` | Doctor | See and manage all appointments |

## Configuration (optional)

Everything works with the defaults. To change something, create `backend/.env`; see
`backend/.env.example` for the options.

- **Postgres needs a username/password.** By default the backend connects to a local Postgres as your OS user
  (the Homebrew / Postgres.app default). Otherwise set:
  `DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/vet_online_consultancy`
- **Google sign-in:** set `GOOGLE_CLIENT_ID` in `backend/.env` and `VITE_GOOGLE_CLIENT_ID` in `.env.local` at the project root.
- **Email notifications to the doctor:** set the `SMTP_*` values in `backend/.env`.

Restart the backend (and frontend, for `.env.local`) after changing these.

## Troubleshooting

| Problem | Fix |
|---|---|
| `connection refused` on backend start | Postgres isn't running. Start it (`brew services start postgresql@16`). |
| `role "..." does not exist` / `password authentication failed` | Set `DATABASE_URL` in `backend/.env` (see Configuration). |
| `permission denied to create database` | Create it yourself (`createdb vet_online_consultancy`) or use a user that can. |
| Frontend shows network errors | Make sure the backend is running on port 8000. |
| Port already in use | `lsof -ti :8000 \| xargs kill` (or `:5173`). |
