# Veterinary Online Consultation Platform — Wireframe Spec & Build Reference

Reference doc for the project. §0–1 describe **the app as it is actually built**: a
single-doctor practice where owners submit consultation requests and Dr. Sarkar follows up
on WhatsApp. §2–9 are the **original Figma wireframe plan** (from
`Veterinary_Online_Consultation_Figma_Wireframe_Specification.pdf`) for a multi-vet
marketplace. They're kept as a design reference, but the app has deliberately moved away
from that plan; see §0 "Not built" for what was dropped.

## 0. Current App (what's actually built)

### Stack

- **Frontend**: React 19 + Vite + TypeScript, Tailwind CSS v4 (`@tailwindcss/vite`, CSS-first
  `@theme` config in `src/index.css`, no `tailwind.config.js`), `react-router-dom` v7.
  Brand palette (teal primary `--color-primary-600: #0d9488`), Inter font.
- **Backend**: FastAPI + SQLAlchemy + Alembic + PostgreSQL (`backend/`). On startup it creates
  the database if missing, runs migrations and creates Dr. Sarkar's doctor profile.
- **Run**: see `HOW_TO_USE.md`. Frontend on port 5173 proxies `/api` to the backend on 8000.

### Pages

| Route | Who | What |
|---|---|---|
| `/` | Everyone | Hero (Book Consultation, Meet Dr. Sarkar, WhatsApp link); About Dr. Sarkar (bio, stats, education & experience, areas of expertise, languages); emergency notice |
| `/register`, `/login` | Pet owners | Email/password or Google sign-in |
| `/book` | Pet owners (signed in) | Consultation request form (below) |
| `/admin` | Dr. Sarkar | All requests, filterable by status; **no login** (runs on her own computer) |

Header nav: Home, About; signed-in owners get **Book Now** and **Logout**. Footer: About,
Contact on WhatsApp. A floating **Chat on WhatsApp**
button shows on every page except `/admin`.

### Core flow

`Owner signs in → fills in the request form → submits → Dr. Sarkar sees it on /admin →
contacts the owner on WhatsApp → marks it Confirmed / Completed / Cancelled`

**Request form** (`src/pages/Book.tsx`), one page, no steps:

- **Owner details**: name, WhatsApp number (pre-filled from the account, editable per request)
- **Pet details**: name (optional), species (free text with suggestions), breed, sex
  (Male / Female / Not sure), age (years + months, stored as an approximate date of birth),
  weight and color (optional)
- **Health information**: main problem (required), require home visit (Yes/No, default No; if Yes, an optional address, with a link to share the location on WhatsApp instead),
  medical history, current medications, allergies (optional)

There is **no time slot, payment or photo upload**. Owners send photos and videos over
WhatsApp (links on the form, on the confirmation screen and site-wide). The confirmation
screen has a prefilled "Send photos & videos on WhatsApp" message.

**Admin dashboard** (`src/pages/AdminDashboard.tsx`): each request shows the pet (name or
"Unnamed <species>"), owner name and number with a WhatsApp button, breed / sex / age / weight,
main problem, medical history, medications and allergies. Status moves
Pending → Confirmed → Completed, or → Cancelled with an optional reason. Home-visit requests get
a **Home visit** tag. **Download Excel** (`GET /api/admin/appointments/export`, built with
`openpyxl`) returns all requests, one row each, with owner, pet, health, home-visit (incl. address), status and date columns.

### Data model (`backend/app/models.py`)

- `users` (owners and the doctor), `doctor_profiles` (one row: Dr. Sarkar), `pets`, `appointments`.
- An appointment stores the booking's `contact_name` / `contact_phone`, `symptoms` (the main
  problem), `home_visit_required`, `home_visit_address` and `status`. `scheduled_start` / `scheduled_end` are nullable: new requests have
  no time; older slot-based bookings keep theirs.
- Each request creates a new `pets` row; there's no saved-pets list.

### Configuration

- `VITE_DOCTOR_WHATSAPP` in `.env.local`: Dr. Sarkar's WhatsApp number; WhatsApp links are
  hidden until it's set.
- `VITE_GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_ID`: Google sign-in.
- `DOCTOR_EMAIL` + `SMTP_*`: 15-minute reminder emails. These only fire for appointments with
  a scheduled time, so requests from the current form don't trigger them.

### Not built (deliberately dropped from the original plan)

- Multiple vets, vet search, doctor profile pages, vet/admin role dashboards (§5 Vet and Admin areas)
- Time-slot booking, video/audio/chat inside the app: consultations happen over WhatsApp
- Payments, prescriptions, medical records, messages, reviews
- Owner dashboard, saved pets, pet profiles, owner appointment history ("My Appointments")
- Photo/document uploads: done over WhatsApp instead
- FAQs page/section

### Placeholder content

Doctor and hero images are emoji in tinted boxes; swap for real photography before launch.

## 1. Product Overview

**Current product**: an online consultation site for one veterinarian, Dr. Nituparna Sarkar.
Two roles in practice:

- **Pet Owner**: registers, submits a consultation request with pet and health details,
  chats with Dr. Sarkar on WhatsApp.
- **Doctor (admin)**: reviews requests on `/admin`, contacts owners on WhatsApp, tracks status.

Core journey:
`Pet is sick → Submit consultation request → Dr. Sarkar contacts owner on WhatsApp → Consultation → Mark completed`

**Original plan** (what §2–9 were designed for): a marketplace connecting pet owners with
many veterinarians for video/audio/chat consultations, plus medical records, prescriptions
and payments, with three roles (Pet Owner, Veterinarian, Admin) and the journey
`Pet Owner → pet is sick → Find a Vet → Choose Doctor → Book Slot → Pay → Talk to Doctor → Get Treatment → Save Medical Record`.
That wireframe effort was grayscale, low-fidelity, structure-and-flow only.

## 2. Figma File Reference

- **File**: `Veterinary Online Consultation Platform — Wireframes V1`
- **File key**: `5RW9K1ozcXAhNy34pffskf`
- **URL**: https://www.figma.com/design/5RW9K1ozcXAhNy34pffskf
- **Team/plan key**: `team::1646609040808856342` ("JanarS Aws's team", **Starter tier**)

### Constraints discovered during build (deviations from the original PDF spec)

- **3-page cap.** Starter plan caps files at 3 pages (PDF spec called for 7 pages —
  00 Cover, 01 Design System, 02 Public, 03 Owner, 04 Vet, 05 Admin, 06 Mobile).
  Adapted to 3 pages, using **Figma Sections** to organize within each page:
  - `01 — Design System` (id `0:1`) — Cover & Notes, Foundations, all component sections
  - `02 — Web Screens` (id `1:4`) — Public, Pet Owner, Veterinarian, Admin areas as sections
  - `03 — Mobile Screens` (id `1:5`) — mobile frames as a section
- **MCP tool call quota.** Starter plan allows only **6 Figma MCP tool calls/month**
  (per Figma's rate-limit doc — applies regardless of seat type on Starter). This was
  exceeded while building the component library; further programmatic edits are blocked
  until the quota resets or the plan is upgraded to Professional (200/day) or higher.
  **Check this before resuming automated builds.**
- **Component states simplified.** The PDF asks for Default/Hover/Pressed/Disabled/Loading
  states on interactive components and Default/Focused/Filled/Error/Disabled on inputs.
  Given the wireframe-stage instruction to skip polish and the 47-screen scope, only
  **Default state** was built for each component. State variants are a fast-follow, not
  blocking screen assembly.
- **No dedicated Danger color.** Spec mandates grayscale-only at this stage (no red for
  destructive actions). Danger button uses a dashed `border-strong` stroke on a white
  fill to differentiate structurally without introducing color.
- **Spacing tokens are a followed convention, not bound Figma variables.** Colors and
  type are real Figma variables/styles (for fast global edits); the 8pt spacing scale
  (4/8/12/16/24/32/40/48/64/80) is documented in Foundations and followed by convention
  in every frame, not wired through `setBoundVariable` on every node — this was a
  deliberate scope cut to keep the 47-screen build tractable.

### Design tokens already created

**Color variables** — collection `Colors` (id `VariableCollectionId:2:2`), single mode `Value`:

| Variable | Hex | Scope |
|---|---|---|
| `color/bg-page` | `#F7F7F7` | Frame/Shape fill |
| `color/bg-card` | `#FFFFFF` | Frame/Shape fill |
| `color/bg-inverse` | `#222222` | Frame/Shape fill |
| `color/bg-hover` | `#EFEFEF` | Frame/Shape fill |
| `color/bg-disabled` | `#F0F0F0` | Frame/Shape fill |
| `color/text-primary` | `#222222` | Text fill |
| `color/text-secondary` | `#666666` | Text fill |
| `color/text-inverse` | `#FFFFFF` | Text fill |
| `color/text-placeholder` | `#999999` | Text fill |
| `color/border-default` | `#DDDDDD` | Stroke |
| `color/border-strong` | `#222222` | Stroke |

**Text styles** — font **Inter**:

| Style | Size / Weight | Line height |
|---|---|---|
| `type/h1` | 40 / Bold | 48px |
| `type/h2` | 32 / Bold | 40px |
| `type/h3` | 24 / Semi Bold | 32px |
| `type/h4` | 18 / Semi Bold | 24px |
| `type/body` | 16 / Regular | 24px |
| `type/small` | 14 / Regular | 20px |
| `type/caption` | 12 / Regular | 16px |

**Spacing scale (convention, px)**: 4, 8, 12, 16, 24, 32, 40, 48, 64, 80.
Card padding 24, form-field gap 16, buttons 44–48 high, inputs 48 high, radius 8–12.

### Components already built (on `01 — Design System` page)

| Section (Figma node id) | Components | Key ids |
|---|---|---|
| Cover & Notes (`2:24`) | Title, notes | — |
| Foundations (`2:47`) | Color swatches, type specimen, spacing bars | — |
| Components — Buttons (`3:2`) | `Button` variant set (Style=Primary/Secondary/Text/Danger), `Icon Button` | set `3:12`, icon btn `3:13` |
| Components — Inputs (`4:2`) | `Input Field` variant set (Type=Text/Search/Dropdown/Date/Time), `Textarea`, `Checkbox`, `Radio` | set `4:29`, textarea `4:30`, checkbox `4:34`, radio `4:37` |
| Components — Cards 1/2 (`6:6`) | `Card/Doctor`, `Card/Pet`, `Card/Appointment`, `Card/Statistic` | `6:10`, `6:19`, `6:29`, `6:40` |
| Components — Cards 2/2 (`7:6`) | `Card/Prescription`, `Card/Medical Record`, `Card/Notification` | `7:10`, `7:19`, `7:31` |
| Components — Navigation (`8:34`) | `Header/Public`, `Header/Dashboard`, `Sidebar` variant set (Role=Owner/Doctor/Admin) | `8:37`, `8:50`, set `8:204` |
| Components — Feedback (`9:11`) | `Alert` variant set (Type=Success/Error/Warning), `Empty State`, `Loading` | set `9:26`, `9:27`, `9:34` |

### Components NOT yet built

- **Modals**: `Modal/Confirmation`, `Modal/Cancel Appointment`, `Modal/Upload Document`, `Modal/Add Pet`
  (script drafted, blocked by rate limit — see build notes below for the exact
  content each should contain, under §6 Reusable Components)

### Reusable helper patterns (for whoever resumes the `use_figma` scripting)

Two bugs were hit and fixed during the build — avoid repeating them:

1. **`layoutSizingHorizontal/Vertical = FILL` must be set AFTER `appendChild`**, never before.
   Setting it before the node is parented into an auto-layout frame throws.
2. **Never chain off `appendChild()`** (e.g. `frame.appendChild(placeholder(...)).cornerRadius = X`).
   `appendChild` does not reliably return the child in this scripting context — assign to a
   variable first, then set properties on the variable.
3. **Placeholder blocks**: build with `figma.createAutoLayout()` (not `createFrame()` +
   manual `layoutMode`), and set `primaryAxisSizingMode`/`counterAxisSizingMode = "FIXED"`
   **before** calling `resize(w, h)` — enabling auto-layout after `resize()` resets sizing
   to AUTO/hug and collapses the block to its label's size.
4. **Component instance text**: always override via `setProperties()` on the specific
   instance after `createInstance()` — don't rely on the variant's baked-in default text,
   which was observed to not reliably follow the correct variant when multiple sibling
   variants each declare a same-named TEXT property before `combineAsVariants`.

## 3. Figma Frame Sizes

- Desktop: 1440 × 1024 px
- Tablet: 1024 × 1366 px
- Mobile: 390 × 844 px
- Desktop grid: 12 columns, 24px gutter, 80px margins
- Dashboard layout: 240px sidebar, 32px main-content padding

## 4. Low-Fidelity Visual Language

Grayscale only (see token table above). Placeholder blocks: `[IMAGE]`, `[ICON]`, `[AVATAR]`.
No shadows, gradients, illustrations, or brand color at this stage.

## 5. Screen Inventory (target ~47 frames)

_Original wireframe plan. In the built app only Home, Login, Register, a one-page request
form (replacing the 5-step booking flow) and a single admin list exist; see §0._

None of the screens below are built in Figma yet — only the component library (§2) is done.
Build order should follow §8 (Recommended Build Order).

### Public Website (7) — page `02 — Web Screens`, section "Public"

1. **Home** — Header/Public; Hero (headline, subtext, Book Consultation + Find a Veterinarian CTAs, `[IMAGE]` right); How It Works (4 cards: Add Pet, Find Vet, Book, Consult); Services (6 cards: General Consultation, Nutrition, Skin & Allergy, Dental, Behaviour, Puppy/Kitten); Veterinarian Preview (4 `Card/Doctor`); Emergency notice; Footer (Company/Services/Support/Social)
2. **Veterinarians** (list/search) — filter bar (species, specialization, consultation type, availability, price) + grid of `Card/Doctor`
3. **Doctor Profile** — photo, name, specialty, rating, experience, education, languages, specializations, About, Reviews, consultation options (Video/Audio/Chat w/ duration+price), Book Consultation CTA
4. **Services** — service list/detail
5. **FAQs** — accordion list
6. **Login** — centered 420px card: logo, "Welcome Back", email, password, forgot-password, Login button, optional Google sign-in, Register link
7. **Register** — two-column: `[IMAGE]` pet-care visual left, Full Name/Email/Phone/Password + Create Account right

### Pet Owner (13) — section "Pet Owner", uses `Sidebar` (Role=Owner) + `Header/Dashboard`

1. **Dashboard** — welcome message; `Card/Statistic` × 3 (My Pets, Upcoming, Consultations); My Pets section (`Card/Pet` grid + Add Pet CTA); Upcoming Appointment (`Card/Appointment`); Quick actions (Add Pet, Book Consultation, Medical Records, Prescriptions)
2. **My Pets** — grid of `Card/Pet` (photo, name, species, age, View/Edit)
3. **Add Pet** — form: photo, name, species, breed, gender, DOB, weight, color, allergies, existing conditions, current medications (use `Input Field` variants + `Textarea`) — full-page version of `Modal/Add Pet`
4. **Pet Profile** — header (photo, name, breed, gender, age, weight, Edit Profile); tabs (Overview, Medical History, Vaccinations, Documents, Consultations, Prescriptions); Overview cards (Basic Information, Health Information, Next Follow-up)
5. **Veterinarian Search** — same as public Veterinarians but inside owner shell
6. **Doctor Profile** (owner context) — same as public Doctor Profile but inside owner shell, Book Consultation leads into booking flow
7. **Booking flow** (5 steps, one frame per step or a single scrollable multi-step frame with step indicator `1 Pet → 2 Type → 3 Date → 4 Problem → 5 Payment`):
   - Step 1: select pet (`Card/Pet` picker) or add new
   - Step 2: select Video/Audio/Chat
   - Step 3: calendar left, time slots right
   - Step 4: symptoms `Textarea`, onset, severity, upload (photo/video/PDF)
   - Step 5: summary, consultation fee, platform fee, total, payment method, Pay button
8. **Payment** — (may be same frame as booking step 5, or separate) payment method selection + Pay CTA
9. **Confirmation** — `Modal/Confirmation` content as full page: success indicator, doctor, pet, date/time, type, appointment ID, Add to Calendar / View Appointment / Back to Dashboard
10. **Appointments** — tabs Upcoming/Completed/Cancelled; `Card/Appointment` list with View Details + Join Consultation
11. **Consultation** — large video area + 320px patient-info sidebar (pet details, allergies, medical history, records); bottom controls (Mute, Camera, Chat, Files, More, End Consultation); chat drawer; emergency notice accessible
12. **Messages** — conversation list + thread view
13. **Prescriptions** — `Card/Prescription` list; detail view: doctor, pet, diagnosis, medicines (dosage/frequency/duration/instructions), additional instructions, follow-up, Download PDF
14. **Medical Records** — Upload Record CTA (`Modal/Upload Document`); filters (All/Reports/Prescriptions/Images/X-Rays); `Card/Medical Record` list with View/Download

_(Note: PDF lists 13 owner screens; the breakdown above yields 14 logical views because
Booking's 5 steps are one flow — treat "Booking flow" as a single inventory item worth 5
frames when counting toward the ~47 total, matching the PDF's ~13 count.)_

### Veterinarian (8) — section "Veterinarian", uses `Sidebar` (Role=Doctor) + `Header/Dashboard`

1. **Doctor Dashboard** — greeting; `Card/Statistic` × (Today, Completed, Upcoming, Earnings); today's appointment timeline/list
2. **Appointments** — pet info, appointment date/time/type, Start Consultation
3. **Patients** — patient list (search/filter)
4. **Patient Profile** — tabs: Overview, Medical History, Consultations, Prescriptions, Documents, Vaccinations
5. **Consultation** — doctor-side view of the consultation experience (§ below) + end-of-consultation form: Symptoms, Assessment/Diagnosis, Treatment Plan, Follow-up, Create Prescription, Complete Consultation
6. **Prescription** (create/edit) — same field set as owner Prescriptions detail, editable
7. **Availability** — weekly schedule, working hours, consultation duration, buffer time, Save Schedule
8. **Profile** — professional details, qualifications, experience, specializations, languages, consultation types

### Admin (9) — section "Admin", uses `Sidebar` (Role=Admin) + `Header/Dashboard`

1. **Admin Dashboard** — `Card/Statistic` × (Users, Doctors, Appointments, Revenue); appointments/revenue charts (placeholder blocks); recent appointments; recent users; pending doctor approvals
2. **Veterinarians** (table) — doctor, specialization, experience, status, action; Add Doctor; search; review/verification flow
3. **Users** (table) — name, email, pets, appointments, status, actions
4. **Pets** (table) — cross-owner pet directory
5. **Appointments** (table) — platform-wide appointments
6. **Consultations** — consultation history/oversight
7. **Payments** (table) — transaction ID, user, doctor, amount, status (Paid/Pending/Failed/Refunded), date
8. **Reviews** — review moderation list
9. **Settings** — platform settings (+ Notifications, Reports live here or as adjacent tabs per PDF sidebar)

### Mobile (10 key frames) — page `03 — Mobile Screens`, 390×844, 16px side padding, redesigned (not shrunk) layouts

Bottom nav (owner): Home, Appointments, Pets, Messages, Profile.

1. Mobile Home (public)
2. Mobile Login
3. Mobile Owner Dashboard
4. Mobile Booking (one step per screen — pick the pet-selection or date/time step as the representative frame)
5. Mobile Consultation (near-full-screen video, compact bottom controls, pet info as bottom sheet)
6. Mobile Appointments
7. Mobile Messages
8. Mobile Doctor Dashboard
9. Mobile Patients (doctor)
10. Mobile Profile

## 6. Reusable Components — Modal content (for the 4 not-yet-built modals)

Drafted in the failed/blocked script — rebuild using this content:

- **Modal/Confirmation** (400px): `[ICON]` circle, "Appointment Confirmed" title, body text
  with doctor/date/time, buttons: Secondary "View Appointment" + Primary "Back to Dashboard"
- **Modal/Cancel Appointment** (400px): title "Cancel this appointment?", appointment
  summary body text, `Input Field` (Text, "Reason (optional)"), buttons: Secondary
  "Keep Appointment" + Danger "Cancel Appointment"
- **Modal/Upload Document** (400px): title "Upload Medical Record", dashed dropzone
  (`[ICON]`, "Drag & drop or click to upload", "PDF, JPG, PNG up to 10MB"), buttons:
  Secondary "Cancel" + Primary "Upload"
- **Modal/Add Pet** (420px): title "Add a Pet", `[IMAGE]` circular avatar placeholder,
  two rows of paired `Input Field`s (Pet Name + Species dropdown; Breed + Date of Birth),
  buttons: Secondary "Cancel" + Primary "Add Pet"

## 7. Prototype Navigation

_Original plan. The built app's path is `Home → Login → Request form → Confirmation (→ WhatsApp)`;
see §0._

Primary clickable path (wire with Figma prototype connections once screens exist):

`Home → Login → Owner Dashboard → Find Vet → Doctor Profile → Select Pet → Select Date/Time → Consultation Info → Payment → Confirmation → Appointment → Join Consultation → Prescription`

Every screen needs an obvious back path (← Back). Each screen should have exactly one
primary CTA (Book Consultation, Continue, Pay, View Appointment, Join Consultation,
Complete Consultation, or Save Prescription).

## 8. Recommended Build Order

1. **Phase 1 (critical path)**: Homepage, Login, Owner Dashboard, Add Pet, Pet Profile,
   Veterinarian Search, Doctor Profile, Booking, Payment, Confirmation, Appointment,
   Consultation, Prescription
2. **Phase 2**: Appointments, Medical Records, Messages, Notifications, Profile, Settings
3. **Phase 3**: Doctor Dashboard, Appointments, Patients, Patient Profile, Consultation,
   Prescription, Availability, Profile
4. **Phase 4**: Admin Dashboard, Doctors, Users, Pets, Appointments, Payments, Reviews,
   Reports, Settings
5. **Phase 5**: Mobile versions of the key owner and consultation flows

## 9. Status / Next Steps (Figma wireframe track)

_The code track has moved past this plan; see §0 for what's built._

- [x] Design tokens (colors, type, spacing convention)
- [x] Core component library (buttons, inputs, cards, nav, feedback) — Default state only
- [ ] Modal components (4) — content drafted above, blocked on rate limit
- [ ] Public website screens (7)
- [ ] Pet Owner screens (13, incl. 5-step booking flow)
- [ ] Veterinarian screens (8)
- [ ] Admin screens (9)
- [ ] Mobile frames (10)
- [ ] Prototype connections for the primary clickable path
- [ ] Optional fast-follow: Hover/Focused/Error/Disabled states on components

**Blocker**: Figma Starter plan MCP quota (6 calls/month) exhausted. Resume once
upgraded (Professional+) or quota resets. When resuming, re-read this file — the node
ids in §2 let the build continue without re-inspecting the file from scratch.
