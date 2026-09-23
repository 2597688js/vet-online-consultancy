# Vet Online Consultancy

Online consultation platform for Dr. Nituparna Sarkar (a single-veterinarian practice). Pet owners register
and submit consultation requests; Dr. Sarkar manages them from the admin dashboard.

## How booking works

1. The pet owner signs in and fills in the form at `/book`:
   - **Owner:** name and WhatsApp number (pre-filled from their account, editable per request)
   - **Pet:** name (optional), species, breed, age, sex, plus optional weight and color
   - **Health:** main problem (required), require home visit (Yes/No, with an optional address or location shared on WhatsApp), medical history, current medications and allergies (optional)
   - Owners share photos and videos with Dr. Sarkar directly on WhatsApp.
2. There is no time slot to pick. The request is saved as **Pending**.
3. Dr. Sarkar sees each request on the admin dashboard with the owner's contact and the pet's details,
   contacts the owner using its WhatsApp button to arrange the consultation, then marks it **Confirmed**, **Completed** or
   **Cancelled**. **Download Excel** on the dashboard exports every request with the owner's and pet's details.

Quick start (needs Node, Python 3.11+ and PostgreSQL installed; the backend runs its own PostgreSQL server
with the data in the project's `db/` folder):

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
