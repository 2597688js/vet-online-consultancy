import { Header } from "../components/Header";
import { Footer } from "../components/Footer";
import { Button } from "../components/Button";
import { AlertIcon, StarIcon } from "../components/icons";
import { useAuth } from "../context/AuthContext";

const doctor = {
  name: "Dr. Nituparna Sarkar",
  specialty: "Pet Animal Care · Veterinary Pathology",
  experience: "BVSc & A.H, MVSc (Pursuing)",
  rating: 5.0,
  price: "Consultation fee on booking",
  bio: "Dr. Nituparna Sarkar offers online veterinary consultations for dogs, cats, and other companion animals — from everyday health concerns to nutrition, skin, dental, and behaviour guidance. She currently practices as an Assistant Veterinary Doctor at Progressive Pet Clinic, Guwahati, and is pursuing her Masters in Veterinary Pathology at the College of Veterinary Science, AAU, Khanapara.",
};

const education = [
  { period: "2026 – Present", title: "Masters of Veterinary Pathology (MVSc)", place: "College of Veterinary Science, AAU, Khanapara" },
  { period: "2025", title: "Bachelors of Veterinary Science & Animal Husbandry (BVSc & A.H)", place: "College of Veterinary Science, AAU, Khanapara" },
];

const experience = [
  {
    period: "Jan 2026 – Present",
    title: "Assistant Veterinary Doctor",
    place: "Progressive Pet Clinic, VIP Road, Guwahati (with Dr. Arup Das, Surgeon)",
    body: "Diagnosis, management & treatment of clinical cases, surgical management, post-operative care, and laboratory testing.",
  },
  {
    period: "Feb 2026 – Present",
    title: "Postgraduate Student, Veterinary Pathology",
    place: "College of Veterinary Science, AAU, Khanapara",
    body: "Post-mortem investigation of large and small animals, field work with wildlife and domestic animals, laboratory techniques and sample handling.",
  },
  {
    period: "Jan – Dec 2025",
    title: "Intern Doctor",
    place: "Advanced Animal Disease Diagnosis & Management Consortium (ADMaC-DBT)",
    body: "Rotations across the Teaching Veterinary Clinical Complex, Assam State Zoo cum Botanical Garden, Goat Research Station (Burnihat), and Rural Dispensary, Jagiroad.",
  },
];

const expertiseAreas = [
  "Pet animal care (Dog & Cat)",
  "Small & large ruminant diagnosis and treatment",
  "Hospital & field work",
  "Laboratory techniques",
  "Post-mortem of domestic & wild animals",
];

const languages = ["Assamese", "English", "Hindi", "Bengali"];

const stats = [
  { value: "200+", label: "Clinical cases managed" },
  { value: "8+", label: "Elephant post-mortems (wild)" },
  { value: "25+", label: "Pet & large-animal post-mortems" },
];

const faqs = [
  {
    q: "How does an online consultation work?",
    a: "Book a slot, choose a time, and join Dr. Sarkar over video, audio, or chat from the browser at your scheduled time. No app download needed.",
  },
  {
    q: "Which pets can I book a consultation for?",
    a: "Dogs, cats, and other companion animals. For large or farm animals, please contact us directly so we can advise on the best way to help.",
  },
  {
    q: "Do I need to create an account to book?",
    a: "Yes. Registering takes under a minute and lets you keep a record of your pet's profile, past consultations, and prescriptions in one place.",
  },
  {
    q: "How much does a consultation cost?",
    a: "The consultation fee is shown at the time of booking and depends on the type of consultation you choose (video, audio, or chat).",
  },
  {
    q: "What should I have ready before the consultation?",
    a: "Have your pet nearby if possible, along with any recent symptoms, medication history, or prior reports you can describe or show on camera.",
  },
  {
    q: "Can Dr. Sarkar prescribe medication online?",
    a: "Yes, where appropriate for the condition. If an in-person examination, diagnostic test, or procedure is needed, you'll be advised to visit a clinic.",
  },
  {
    q: "What if my pet needs emergency care?",
    a: "Online consultation is not a substitute for emergency care. If your pet is in a life-threatening situation, please go to your nearest emergency animal hospital immediately.",
  },
  {
    q: "Can I reschedule or cancel a booked appointment?",
    a: "Yes, you can manage your upcoming appointments from your account. We recommend rescheduling as early as possible so the slot can be offered to another pet parent.",
  },
  {
    q: "What happens if I miss my appointment?",
    a: "If you don't join within a few minutes of the scheduled time, the consultation may be marked as missed. You're welcome to book a new slot.",
  },
  {
    q: "Is there a follow-up after the consultation?",
    a: "Dr. Sarkar may recommend a follow-up consultation to track your pet's progress, especially for ongoing conditions or after starting a new treatment.",
  },
  {
    q: "What languages does Dr. Sarkar consult in?",
    a: "Consultations are available in Assamese, English, Hindi, and Bengali.",
  },
  {
    q: "What are the available consultation hours?",
    a: "Slots are generally open between 12:00 PM and 9:00 PM. Exact availability for a given day is shown when you book.",
  },
  {
    q: "Is my pet's information kept private?",
    a: "Yes. Your account details and your pet's medical information are used only to provide and improve your consultations, and are not shared with third parties.",
  },
  {
    q: "How do I pay for a consultation?",
    a: "Payment details and options are presented during the booking flow before your appointment is confirmed.",
  },
  {
    q: "Who do I contact if I have an issue with my booking?",
    a: "Reach out through the Contact link in the footer and we'll help resolve it as quickly as possible.",
  },
];

export function Home() {
  const { user } = useAuth();
  const bookHref = user ? "/book" : "/login";

  return (
    <div className="flex min-h-screen flex-col">
      <Header />

      <main className="flex-1">
        {/* Hero */}
        <section className="mx-auto grid max-w-7xl grid-cols-1 items-center gap-12 px-6 py-20 lg:grid-cols-2 lg:px-20">
          <div>
            <h1 className="text-4xl font-bold leading-tight text-ink lg:text-5xl">
              See Dr. Nituparna Sarkar online, whenever your pet needs care.
            </h1>
            <p className="mt-6 text-lg text-body">
              Book a video, audio, or chat consultation with Dr. Sarkar in minutes. Get
              advice, prescriptions, and follow-up care without leaving home.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Button variant="primary" href={bookHref}>
                Book Consultation
              </Button>
              <Button variant="secondary" href="/#about">
                Meet Dr. Sarkar
              </Button>
            </div>
          </div>
          <div className="flex h-80 items-center justify-center rounded-3xl bg-gradient-to-br from-primary-100 to-primary-50 text-8xl lg:h-96">
            🐕
          </div>
        </section>

        {/* About the doctor */}
        <section id="about" className="scroll-mt-[88px] bg-white py-20">
          <div className="mx-auto max-w-5xl px-6 lg:px-20">
            <div className="grid grid-cols-1 items-center gap-12 lg:grid-cols-[280px_1fr]">
              <div className="mx-auto flex h-56 w-56 items-center justify-center rounded-3xl bg-gradient-to-br from-primary-100 to-primary-50 text-7xl lg:mx-0">
                🩺
              </div>
              <div>
                <span className="text-xs font-semibold uppercase tracking-wide text-primary-600">
                  About your vet
                </span>
                <h2 className="mt-3 text-3xl font-bold text-ink">{doctor.name}</h2>
                <p className="mt-1 text-sm font-medium text-muted">
                  {doctor.specialty} · {doctor.experience}
                </p>
                <p className="mt-4 text-base text-body">{doctor.bio}</p>
                <div className="mt-4 flex flex-wrap items-center gap-3 text-sm text-muted">
                  <span className="flex items-center gap-1 font-medium text-ink">
                    <StarIcon className="h-4 w-4 text-amber-400" />
                    {doctor.rating.toFixed(1)}
                  </span>
                  <span aria-hidden>·</span>
                  <span>{doctor.price}</span>
                </div>
                <div className="mt-4 flex flex-wrap gap-2">
                  {languages.map((lang) => (
                    <span key={lang} className="rounded-full bg-primary-50 px-3 py-1 text-xs font-medium text-primary-600">
                      {lang}
                    </span>
                  ))}
                </div>
                <div className="mt-6">
                  <Button variant="primary" href={bookHref}>
                    Book a Consultation
                  </Button>
                </div>
              </div>
            </div>

            {/* Stats */}
            <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-3">
              {stats.map((stat) => (
                <div key={stat.label} className="rounded-2xl border border-border p-6 text-center">
                  <div className="text-3xl font-bold text-ink">{stat.value}</div>
                  <div className="mt-1 text-sm text-muted">{stat.label}</div>
                </div>
              ))}
            </div>

            {/* Education & Experience */}
            <div className="mt-16 grid grid-cols-1 gap-12 lg:grid-cols-2">
              <div>
                <h3 className="text-lg font-semibold text-ink">Education</h3>
                <div className="mt-4 space-y-5">
                  {education.map((item) => (
                    <div key={item.title} className="border-l-2 border-primary-100 pl-4">
                      <div className="text-xs font-semibold uppercase tracking-wide text-primary-600">{item.period}</div>
                      <div className="mt-1 text-sm font-semibold text-ink">{item.title}</div>
                      <div className="text-sm text-muted">{item.place}</div>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-ink">Experience</h3>
                <div className="mt-4 space-y-5">
                  {experience.map((item) => (
                    <div key={item.title} className="border-l-2 border-primary-100 pl-4">
                      <div className="text-xs font-semibold uppercase tracking-wide text-primary-600">{item.period}</div>
                      <div className="mt-1 text-sm font-semibold text-ink">{item.title}</div>
                      <div className="text-sm text-muted">{item.place}</div>
                      <p className="mt-1 text-sm text-body">{item.body}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Areas of expertise */}
            <div className="mt-16">
              <h3 className="text-lg font-semibold text-ink">Areas of Expertise</h3>
              <ul className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
                {expertiseAreas.map((area) => (
                  <li key={area} className="flex items-start gap-2 text-sm text-body">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary-600" />
                    {area}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        {/* Emergency notice */}
        <section className="py-12">
          <div className="mx-auto flex max-w-7xl items-start gap-4 rounded-2xl border border-danger-600/30 bg-danger-50 px-6 py-5 lg:mx-20">
            <AlertIcon className="mt-0.5 h-5 w-5 shrink-0 text-danger-600" />
            <p className="text-sm text-body">
              <span className="font-semibold text-ink">Online consultation is not a replacement for emergency veterinary care.</span>{" "}
              If your pet is experiencing a life-threatening emergency, contact your nearest emergency animal
              hospital immediately.
            </p>
          </div>
        </section>

        {/* FAQs */}
        <section id="faqs" className="scroll-mt-[88px] bg-white py-20">
          <div className="mx-auto max-w-3xl px-6 lg:px-20">
            <div className="text-center">
              <span className="text-xs font-semibold uppercase tracking-wide text-primary-600">FAQs</span>
              <h2 className="mt-3 text-3xl font-bold text-ink">Frequently asked questions</h2>
              <p className="mt-3 text-base text-body">
                Everything you need to know before booking an online consultation.
              </p>
            </div>
            <div className="mt-10 space-y-3">
              {faqs.map((faq) => (
                <details
                  key={faq.q}
                  className="group rounded-2xl border border-border px-5 py-4 open:bg-primary-50/40"
                >
                  <summary className="flex cursor-pointer list-none items-center justify-between gap-4 text-sm font-semibold text-ink marker:content-none">
                    {faq.q}
                    <span className="shrink-0 text-lg leading-none text-primary-600 transition-transform group-open:rotate-45">
                      +
                    </span>
                  </summary>
                  <p className="mt-3 text-sm text-body">{faq.a}</p>
                </details>
              ))}
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
