import { Header } from "../components/Header";
import { Footer } from "../components/Footer";
import { Button } from "../components/Button";
import { DoctorCard } from "../components/DoctorCard";
import {
  PawIcon,
  SearchIcon,
  CalendarIcon,
  VideoIcon,
  HeartPulseIcon,
  LeafIcon,
  ToothIcon,
  ShieldIcon,
  ChatIcon,
  AlertIcon,
} from "../components/icons";
import type { ReactNode } from "react";

const steps = [
  {
    icon: <PawIcon className="h-6 w-6" />,
    title: "Add Pet",
    body: "Create a profile for your pet with their history and health details.",
  },
  {
    icon: <SearchIcon className="h-6 w-6" />,
    title: "Find Vet",
    body: "Browse licensed veterinarians by specialty, rating, and availability.",
  },
  {
    icon: <CalendarIcon className="h-6 w-6" />,
    title: "Book",
    body: "Pick a time that works and choose video, audio, or chat.",
  },
  {
    icon: <VideoIcon className="h-6 w-6" />,
    title: "Consult",
    body: "Talk to your vet from home and get a treatment plan.",
  },
];

const services = [
  { icon: <HeartPulseIcon className="h-6 w-6" />, title: "General Consultation", body: "Everyday health concerns and checkups." },
  { icon: <LeafIcon className="h-6 w-6" />, title: "Nutrition", body: "Diet plans tailored to your pet's needs." },
  { icon: <ShieldIcon className="h-6 w-6" />, title: "Skin & Allergy", body: "Diagnose and manage skin conditions." },
  { icon: <ToothIcon className="h-6 w-6" />, title: "Dental", body: "Oral health guidance and care plans." },
  { icon: <ChatIcon className="h-6 w-6" />, title: "Behaviour", body: "Support for anxiety, training, and habits." },
  { icon: <PawIcon className="h-6 w-6" />, title: "Puppy / Kitten", body: "New-pet checkups and vaccination guidance." },
];

const doctors = [
  { name: "Dr. Sarah Mitchell", specialty: "Small Animal · Nutrition", rating: 4.8, experience: "8 yrs experience", price: "$40 / consult", initials: "SM", emoji: "🐶" },
  { name: "Dr. James Carter", specialty: "Dermatology", rating: 4.9, experience: "12 yrs experience", price: "$45 / consult", initials: "JC", emoji: "🐱" },
  { name: "Dr. Priya Nair", specialty: "Behaviour & Training", rating: 4.7, experience: "6 yrs experience", price: "$35 / consult", initials: "PN", emoji: "🐰" },
  { name: "Dr. Omar Rashid", specialty: "Dentistry", rating: 4.9, experience: "10 yrs experience", price: "$50 / consult", initials: "OR", emoji: "🐦" },
];

function SectionHeading({ eyebrow, title, body }: { eyebrow: string; title: string; body?: ReactNode }) {
  return (
    <div className="mx-auto max-w-2xl text-center">
      <span className="text-xs font-semibold uppercase tracking-wide text-primary-600">{eyebrow}</span>
      <h2 className="mt-3 text-3xl font-bold text-ink">{title}</h2>
      {body && <p className="mt-3 text-base text-muted">{body}</p>}
    </div>
  );
}

export function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />

      <main className="flex-1">
        {/* Hero */}
        <section className="mx-auto grid max-w-7xl grid-cols-1 items-center gap-12 px-6 py-20 lg:grid-cols-2 lg:px-20">
          <div>
            <h1 className="text-4xl font-bold leading-tight text-ink lg:text-5xl">
              See a vet online, whenever your pet needs one.
            </h1>
            <p className="mt-6 text-lg text-body">
              Book a video, audio, or chat consultation with a licensed veterinarian in
              minutes. Get advice, prescriptions, and follow-up care without leaving home.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Button variant="primary" href="/login">
                Book Consultation
              </Button>
              <Button variant="secondary" href="/login">
                Find a Veterinarian
              </Button>
            </div>
          </div>
          <div className="flex h-80 items-center justify-center rounded-3xl bg-gradient-to-br from-primary-100 to-primary-50 text-8xl lg:h-96">
            🐕
          </div>
        </section>

        {/* How It Works */}
        <section id="how-it-works" className="bg-white py-20">
          <div className="mx-auto max-w-7xl px-6 lg:px-20">
            <SectionHeading
              eyebrow="How it works"
              title="Care for your pet in four simple steps"
            />
            <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {steps.map((step, i) => (
                <div key={step.title} className="rounded-2xl border border-border p-6">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-ink text-white">
                    {step.icon}
                  </div>
                  <div className="mt-4 text-xs font-semibold text-primary-600">Step {i + 1}</div>
                  <h3 className="mt-1 text-lg font-semibold text-ink">{step.title}</h3>
                  <p className="mt-2 text-sm text-muted">{step.body}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Services */}
        <section id="services" className="py-20">
          <div className="mx-auto max-w-7xl px-6 lg:px-20">
            <SectionHeading
              eyebrow="Services"
              title="Consultations for every kind of concern"
            />
            <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {services.map((service) => (
                <div key={service.title} className="flex items-start gap-4 rounded-2xl border border-border bg-white p-6">
                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary-50 text-primary-600">
                    {service.icon}
                  </div>
                  <div>
                    <h3 className="text-base font-semibold text-ink">{service.title}</h3>
                    <p className="mt-1 text-sm text-muted">{service.body}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Veterinarian Preview */}
        <section id="veterinarians" className="bg-white py-20">
          <div className="mx-auto max-w-7xl px-6 lg:px-20">
            <div className="flex flex-wrap items-end justify-between gap-4">
              <SectionHeading eyebrow="Veterinarians" title="Meet our licensed vets" />
            </div>
            <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {doctors.map((doctor) => (
                <DoctorCard key={doctor.name} {...doctor} />
              ))}
            </div>
            <div className="mt-10 flex justify-center">
              <Button variant="secondary" href="/login">
                View All Veterinarians
              </Button>
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
      </main>

      <Footer />
    </div>
  );
}
