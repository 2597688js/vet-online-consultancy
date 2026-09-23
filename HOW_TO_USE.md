# How to Use This Project

Online consultation platform for Dr. Nituparna Sarkar's veterinary practice. Pet owners register and
submit consultation requests; the doctor contacts them on WhatsApp and manages requests from an admin dashboard.

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
| `/` | Everyone | About Dr. Sarkar, with links to book or chat on WhatsApp |
| `/register` | Pet owners | Create an account |
| `/login` | Pet owners | Sign in (email/password or Google) |
| `/book` | Pet owners | Submit a consultation request |
| `/admin` | Doctor | See and manage all requests (no login) |

### Pet owners

1. Register or sign in, then open **Book Now** (`/book`).
2. Fill in the form:
   - **Owner details:** name and WhatsApp number (pre-filled from the account; can be changed per request)
   - **Pet details:** name (optional), species, breed, sex, age in years and months, plus optional weight and color
   - **Health information:** main problem (required), **Require home visit?** (Yes/No), plus optional medical
     history, current medications and allergies
3. Click **Submit consultation request**. There's no time slot to pick; Dr. Sarkar contacts the owner on WhatsApp.
4. To share photos or videos, use a **WhatsApp** link: the button on the confirmation screen, the link in
   the Health section, or the floating button on every page.

### Doctor

1. Open `/admin`. New requests appear under **Pending**, newest first, with the owner's contact details, the
   pet's details and the health information.
2. Use the **WhatsApp** button on a request to message the owner and arrange the consultation.
3. Mark the request **Confirmed**, **Completed** or **Cancelled** (with an optional reason).
4. Click **Download Excel** to get every request as a spreadsheet: owner details, pet details, health
   information, home visit, status and dates, one row per request. Requests that need a home visit are
   also tagged **Home visit** on the dashboard.

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
  Reminders go out 15 minutes before an appointment's scheduled time and link to the dashboard. Requests
  submitted through the current form have no scheduled time, so only older bookings get reminders.

Restart the backend (and frontend, for `.env.local`) after changing these.

## Troubleshooting

| Problem | Fix |
|---|---|
| `connection refused` on backend start | Postgres isn't running. Start it (`brew services start postgresql@16`). |
| `role "..." does not exist` / `password authentication failed` | Set `DATABASE_URL` in `backend/.env` (see Configuration). |
| `permission denied to create database` | Create it yourself (`createdb vet_online_consultancy`) or use a user that can. |
| Frontend shows network errors, or the terminal shows `http proxy error ... ECONNREFUSED` | The backend isn't running. Start it (step 2) on port 8000. |
| No WhatsApp links on the site | Set `VITE_DOCTOR_WHATSAPP` in `.env.local` and restart `npm run dev`. |
| Port already in use | `lsof -ti :8000 \| xargs kill` (or `:5173`). |
