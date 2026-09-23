# Vet Online Consultancy

Online consultation platform for Dr. Nituparna Sarkar (a single-veterinarian practice). Pet owners register
and book consultations; Dr. Sarkar manages them from the admin dashboard.

Quick start (needs Node, Python 3.11+ and a running PostgreSQL):

```bash
# terminal 1: backend
cd backend && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# terminal 2: frontend
npm install && npm run dev
```

Once both are running:

| What | Link |
|---|---|
| Website (pet owners) | http://localhost:5173 |
| Admin dashboard (Nituparna) | http://localhost:5173/admin |
| Backend API | http://localhost:8000 |
| API docs | http://localhost:8000/docs |

The admin dashboard has no login, so keep the app on the doctor's own computer until `/admin` is protected.

Full guide: **[HOW_TO_USE.md](HOW_TO_USE.md)**
