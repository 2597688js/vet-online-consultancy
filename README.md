# Vet Online Consultancy

Online consultation platform for Dr. Nituparna Sarkar (a single-veterinarian practice). Pet owners register
and book consultations; Dr. Sarkar logs in with an admin account.

Quick start (needs Node, Python 3.11+ and a running PostgreSQL):

```bash
# terminal 1: backend
cd backend && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# terminal 2: frontend
npm install && npm run dev
```

Full guide: **[HOW_TO_USE.md](HOW_TO_USE.md)**
