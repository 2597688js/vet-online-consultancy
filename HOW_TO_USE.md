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
migrations, creates the doctor's profile, and saves a generated `JWT_SECRET` (signs pet owners'
login tokens) into `backend/.env`.
You don't need to configure anything.

**3. Frontend** (terminal 2, from the project root)

```bash
npm install
npm run dev
```

Open **http://localhost:5173**.

**4. Admin dashboard**

Open **http://localhost:5173/admin**. There's no login or password.

> Anyone who can open the site can open `/admin` and see every owner's contact details. That's fine while
> the app runs only on the doctor's own computer. Add protection before putting it on the internet.

## Using the app

| Page | Who | What |
|---|---|---|
| `/register` | Pet owners | Create an account |
| `/login` | Pet owners | Sign in |
| `/book` | Pet owners | Book a consultation |
| `/admin` | Doctor | See and manage all appointments (no login) |

## Configuration (optional)

Everything works with the defaults. To change something, create `backend/.env`; see
`backend/.env.example` for the options.

- **Postgres needs a username/password.** By default the backend connects to a local Postgres as your OS user
  (the Homebrew / Postgres.app default). Otherwise set:
  `DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/vet_online_consultancy`
- **Dr. Sarkar's WhatsApp:** set `VITE_DOCTOR_WHATSAPP=+91XXXXXXXXXX` in `.env.local` at the project root. This turns on
  the "Chat on WhatsApp" links (floating button, home page, footer, booking page) so owners can message her and
  share photos and videos. The links stay hidden until it's set.
- **Google sign-in:** set `GOOGLE_CLIENT_ID` in `backend/.env` and `VITE_GOOGLE_CLIENT_ID` in `.env.local` at the project root.
- **Email reminders to the doctor:** set `DOCTOR_EMAIL` and the `SMTP_*` values in `backend/.env`.
  Each reminder links to the dashboard.

Restart the backend (and frontend, for `.env.local`) after changing these.

## Troubleshooting

| Problem | Fix |
|---|---|
| `connection refused` on backend start | Postgres isn't running. Start it (`brew services start postgresql@16`). |
| `role "..." does not exist` / `password authentication failed` | Set `DATABASE_URL` in `backend/.env` (see Configuration). |
| `permission denied to create database` | Create it yourself (`createdb vet_online_consultancy`) or use a user that can. |
| Frontend shows network errors | Make sure the backend is running on port 8000. |
| Port already in use | `lsof -ti :8000 \| xargs kill` (or `:5173`). |
