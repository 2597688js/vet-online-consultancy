Online consultation platform for Dr. Nituparna Sarkar (a single-veterinarian practice). Pet owners register
and book consultations; Dr. Sarkar logs in with an admin account.

## Running the project

### Frontend

```bash
npm install
npm run dev
```

The app runs at `http://localhost:5173`.

### Backend

```bash
cd backend
python -m venv .venv          # skip if .venv already exists
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/` (if not already present) with:

```
DATABASE_URL=postgresql+psycopg://user:pass@localhost/dbname
JWT_SECRET=your-secret-key
```

Then run migrations and start the API:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`.

#### Admin account (Dr. Sarkar)

There is no signup form for the admin account — it's created with a one-off script that upserts by
email, so it's safe to re-run (e.g. to reset the password):

```bash
cd backend
source .venv/bin/activate
ADMIN_EMAIL='her-email@example.com' ADMIN_PASSWORD='a-strong-password' python -m scripts.seed_admin
```

She can then log in from the normal `/login` page with those credentials.

To inspect the database directly:

```bash
psql -h localhost -U <user> -d <dbname>
```

(`<user>` and `<dbname>` come from `DATABASE_URL` in `backend/.env`.) Once connected, `\dt` lists tables and `\d table_name` describes one.

---

DB:
Host:     localhost
Port:     5432
User:     janarddan
Password: (none set)
Database: vet_online_consultancy