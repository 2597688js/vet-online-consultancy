import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Header } from "../components/Header";
import { Footer } from "../components/Footer";
import { Button } from "../components/Button";
import { CameraIcon, CheckCircleIcon, PawIcon, XIcon } from "../components/icons";
import { useAuth } from "../context/AuthContext";
import * as api from "../lib/api";
import { ApiError } from "../lib/api";

const MAX_PHOTOS = 6;
const MAX_PHOTO_MB = 5;
const BOOKING_HORIZON_DAYS = 30;

function todayInputValue(): string {
  const d = new Date();
  const offset = d.getTimezoneOffset();
  const local = new Date(d.getTime() - offset * 60_000);
  return local.toISOString().slice(0, 10);
}

function maxDateInputValue(): string {
  const d = new Date();
  d.setDate(d.getDate() + BOOKING_HORIZON_DAYS);
  const offset = d.getTimezoneOffset();
  const local = new Date(d.getTime() - offset * 60_000);
  return local.toISOString().slice(0, 10);
}

function formatSlotTime(iso: string): string {
  return new Date(iso).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
}

interface PetFormState {
  name: string;
  species: string;
  breed: string;
  gender: api.PetGender;
  dateOfBirth: string;
  weightKg: string;
  color: string;
  allergies: string;
  existingConditions: string;
  currentMedications: string;
}

const initialPetForm: PetFormState = {
  name: "",
  species: "",
  breed: "",
  gender: "UNKNOWN",
  dateOfBirth: "",
  weightKg: "",
  color: "",
  allergies: "",
  existingConditions: "",
  currentMedications: "",
};

interface PhotoDraft {
  file: File;
  previewUrl: string;
}

export function Book() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  const [pet, setPet] = useState<PetFormState>(initialPetForm);
  const [photos, setPhotos] = useState<PhotoDraft[]>([]);
  const [photoError, setPhotoError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [date, setDate] = useState(todayInputValue());
  const [slots, setSlots] = useState<api.Slot[]>([]);
  const [slotsLoading, setSlotsLoading] = useState(false);
  const [slotsError, setSlotsError] = useState<string | null>(null);
  const [selectedSlot, setSelectedSlot] = useState<api.Slot | null>(null);

  const [symptoms, setSymptoms] = useState("");

  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [confirmed, setConfirmed] = useState<api.Appointment | null>(null);

  useEffect(() => {
    if (!loading && !user) {
      navigate("/login");
    }
  }, [loading, user, navigate]);

  useEffect(() => {
    const token = api.getToken();
    if (!token || !date) return;
    setSlotsLoading(true);
    setSlotsError(null);
    setSelectedSlot(null);
    api
      .getSlots(token, date)
      .then(setSlots)
      .catch((err) => setSlotsError(err instanceof ApiError ? err.message : "Couldn't load available slots."))
      .finally(() => setSlotsLoading(false));
  }, [date]);

  useEffect(() => {
    return () => {
      photos.forEach((p) => URL.revokeObjectURL(p.previewUrl));
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const afternoonSlots = useMemo(() => slots.filter((s) => new Date(s.start).getHours() < 17), [slots]);
  const eveningSlots = useMemo(() => slots.filter((s) => new Date(s.start).getHours() >= 17), [slots]);

  function updatePetField<K extends keyof PetFormState>(field: K, value: PetFormState[K]) {
    setPet((prev) => ({ ...prev, [field]: value }));
  }

  function handleFilesSelected(fileList: FileList | null) {
    if (!fileList) return;
    setPhotoError(null);
    const incoming = Array.from(fileList);

    const accepted: PhotoDraft[] = [];
    for (const file of incoming) {
      if (!file.type.startsWith("image/")) {
        setPhotoError("Only image files are allowed.");
        continue;
      }
      if (file.size > MAX_PHOTO_MB * 1024 * 1024) {
        setPhotoError(`Each image must be under ${MAX_PHOTO_MB}MB.`);
        continue;
      }
      accepted.push({ file, previewUrl: URL.createObjectURL(file) });
    }

    setPhotos((prev) => {
      const combined = [...prev, ...accepted];
      if (combined.length > MAX_PHOTOS) {
        setPhotoError(`You can upload up to ${MAX_PHOTOS} photos.`);
        return combined.slice(0, MAX_PHOTOS);
      }
      return combined;
    });

    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  function removePhoto(index: number) {
    setPhotos((prev) => {
      const target = prev[index];
      if (target) URL.revokeObjectURL(target.previewUrl);
      return prev.filter((_, i) => i !== index);
    });
  }

  const canSubmit = pet.name.trim().length > 0 && pet.species.trim().length > 0 && photos.length > 0 && selectedSlot !== null;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!pet.name.trim() || !pet.species.trim()) {
      setError("Please fill in your pet's name and species.");
      return;
    }
    if (photos.length === 0) {
      setError("Please upload at least one photo of your pet.");
      return;
    }
    if (!selectedSlot) {
      setError("Please select an appointment slot.");
      return;
    }

    const token = api.getToken();
    if (!token) {
      navigate("/login");
      return;
    }

    setSubmitting(true);
    try {
      const createdPet = await api.createPet(token, {
        name: pet.name.trim(),
        species: pet.species.trim(),
        breed: pet.breed.trim() || undefined,
        gender: pet.gender,
        date_of_birth: pet.dateOfBirth || undefined,
        weight_kg: pet.weightKg || undefined,
        color: pet.color.trim() || undefined,
        allergies: pet.allergies.trim() || undefined,
        existing_conditions: pet.existingConditions.trim() || undefined,
        current_medications: pet.currentMedications.trim() || undefined,
      });

      await api.uploadPetPhotos(
        token,
        createdPet.id,
        photos.map((p) => p.file)
      );

      const appointment = await api.createAppointment(token, {
        pet_id: createdPet.id,
        scheduled_start: selectedSlot.start,
        symptoms: symptoms.trim() || undefined,
      });

      setConfirmed(appointment);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading || !user) {
    return (
      <div className="flex min-h-screen flex-col">
        <Header />
        <main className="flex flex-1 items-center justify-center">
          <p className="text-sm text-muted">Loading…</p>
        </main>
        <Footer />
      </div>
    );
  }

  if (confirmed) {
    return (
      <div className="flex min-h-screen flex-col">
        <Header />
        <main className="flex flex-1 items-center justify-center px-6 py-20">
          <div className="w-full max-w-lg rounded-2xl border border-border bg-white p-10 text-center">
            <CheckCircleIcon className="mx-auto h-12 w-12 text-primary-600" />
            <h1 className="mt-5 text-2xl font-bold text-ink">Consultation booked</h1>
            <p className="mt-2 text-sm text-muted">
              We've booked {confirmed.pet.name}'s consultation with Dr. Nituparna Sarkar. Once confirmed, she'll reach
              out to you on WhatsApp video at your scheduled time for the consultation.
            </p>
            <div className="mt-6 rounded-xl bg-bg p-5 text-left text-sm">
              <div className="flex justify-between py-1">
                <span className="text-muted">Pet</span>
                <span className="font-semibold text-ink">{confirmed.pet.name}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-muted">Date</span>
                <span className="font-semibold text-ink">
                  {new Date(confirmed.scheduled_start).toLocaleDateString([], {
                    weekday: "short",
                    month: "short",
                    day: "numeric",
                  })}
                </span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-muted">Time</span>
                <span className="font-semibold text-ink">
                  {formatSlotTime(confirmed.scheduled_start)} – {formatSlotTime(confirmed.scheduled_end)}
                </span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-muted">Status</span>
                <span className="font-semibold text-ink">Pending confirmation</span>
              </div>
            </div>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Button variant="secondary" href="/" className="flex-1">
                Back to home
              </Button>
              <Button variant="secondary" href="/appointments" className="flex-1">
                View my appointments
              </Button>
              <Button
                variant="primary"
                className="flex-1"
                onClick={() => {
                  setConfirmed(null);
                  setPet(initialPetForm);
                  setPhotos([]);
                  setSymptoms("");
                  setSelectedSlot(null);
                }}
              >
                Book another
              </Button>
            </div>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-bg">
      <Header />
      <main className="flex-1">
        <div className="mx-auto max-w-3xl px-6 py-12 lg:px-0">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-600 text-white">
              <PawIcon className="h-5 w-5" />
            </span>
            <div>
              <h1 className="text-2xl font-bold text-ink">Book a consultation</h1>
              <p className="text-sm text-muted">with Dr. Nituparna Sarkar</p>
            </div>
          </div>

          <form className="mt-8 flex flex-col gap-8" onSubmit={handleSubmit}>
            {error && <p className="rounded-lg bg-danger-50 px-4 py-3 text-sm font-medium text-danger-600">{error}</p>}

            {/* Pet details */}
            <section className="rounded-2xl border border-border bg-white p-6">
              <h2 className="text-lg font-semibold text-ink">Pet details</h2>
              <p className="mt-1 text-sm text-muted">Tell us about the pet you'd like Dr. Sarkar to see.</p>

              <div className="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Pet name</span>
                  <input
                    className="h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink placeholder-placeholder outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                    placeholder="e.g. Bruno"
                    required
                    value={pet.name}
                    onChange={(e) => updatePetField("name", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Species</span>
                  <input
                    className="h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink placeholder-placeholder outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                    placeholder="e.g. Dog, Cat"
                    required
                    value={pet.species}
                    onChange={(e) => updatePetField("species", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Breed (optional)</span>
                  <input
                    className="h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink placeholder-placeholder outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                    placeholder="e.g. Labrador"
                    value={pet.breed}
                    onChange={(e) => updatePetField("breed", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Gender</span>
                  <select
                    className="h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                    value={pet.gender}
                    onChange={(e) => updatePetField("gender", e.target.value as api.PetGender)}
                  >
                    <option value="UNKNOWN">Unknown</option>
                    <option value="MALE">Male</option>
                    <option value="FEMALE">Female</option>
                  </select>
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Date of birth (optional)</span>
                  <input
                    type="date"
                    max={todayInputValue()}
                    className="h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                    value={pet.dateOfBirth}
                    onChange={(e) => updatePetField("dateOfBirth", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Weight in kg (optional)</span>
                  <input
                    type="number"
                    min="0"
                    step="0.1"
                    className="h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink placeholder-placeholder outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                    placeholder="e.g. 12.5"
                    value={pet.weightKg}
                    onChange={(e) => updatePetField("weightKg", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2 sm:col-span-2">
                  <span className="text-sm font-semibold text-ink">Color / markings (optional)</span>
                  <input
                    className="h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink placeholder-placeholder outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                    placeholder="e.g. Brown with white patch"
                    value={pet.color}
                    onChange={(e) => updatePetField("color", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2 sm:col-span-2">
                  <span className="text-sm font-semibold text-ink">Allergies (optional)</span>
                  <textarea
                    rows={2}
                    className="w-full resize-none rounded-lg border border-border bg-white px-4 py-3 text-base text-ink placeholder-placeholder outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                    value={pet.allergies}
                    onChange={(e) => updatePetField("allergies", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2 sm:col-span-2">
                  <span className="text-sm font-semibold text-ink">Existing conditions (optional)</span>
                  <textarea
                    rows={2}
                    className="w-full resize-none rounded-lg border border-border bg-white px-4 py-3 text-base text-ink placeholder-placeholder outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                    value={pet.existingConditions}
                    onChange={(e) => updatePetField("existingConditions", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2 sm:col-span-2">
                  <span className="text-sm font-semibold text-ink">Current medications (optional)</span>
                  <textarea
                    rows={2}
                    className="w-full resize-none rounded-lg border border-border bg-white px-4 py-3 text-base text-ink placeholder-placeholder outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                    value={pet.currentMedications}
                    onChange={(e) => updatePetField("currentMedications", e.target.value)}
                  />
                </label>
              </div>
            </section>

            {/* Photos */}
            <section className="rounded-2xl border border-border bg-white p-6">
              <h2 className="text-lg font-semibold text-ink">Photos</h2>
              <p className="mt-1 text-sm text-muted">
                Upload a few clear photos of your pet (up to {MAX_PHOTOS}, {MAX_PHOTO_MB}MB each).
              </p>

              {photoError && <p className="mt-3 text-sm font-medium text-danger-600">{photoError}</p>}

              <div className="mt-4 flex flex-wrap gap-4">
                {photos.map((photo, index) => (
                  <div key={photo.previewUrl} className="group relative h-24 w-24 overflow-hidden rounded-xl border border-border">
                    <img src={photo.previewUrl} alt="" className="h-full w-full object-cover" />
                    <button
                      type="button"
                      aria-label="Remove photo"
                      onClick={() => removePhoto(index)}
                      className="absolute right-1 top-1 flex h-6 w-6 items-center justify-center rounded-full bg-ink/70 text-white"
                    >
                      <XIcon className="h-3.5 w-3.5" />
                    </button>
                  </div>
                ))}

                {photos.length < MAX_PHOTOS && (
                  <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    className="flex h-24 w-24 flex-col items-center justify-center gap-1 rounded-xl border border-dashed border-border text-muted hover:border-ink hover:text-ink"
                  >
                    <CameraIcon className="h-6 w-6" />
                    <span className="text-xs font-medium">Add photo</span>
                  </button>
                )}
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                multiple
                className="hidden"
                onChange={(e) => handleFilesSelected(e.target.files)}
              />
            </section>

            {/* Slot picker */}
            <section className="rounded-2xl border border-border bg-white p-6">
              <h2 className="text-lg font-semibold text-ink">Pick a slot</h2>
              <p className="mt-1 text-sm text-muted">Available every day, 12:00 PM – 9:00 PM, in 30-minute slots.</p>

              <label className="mt-4 flex flex-col gap-2 sm:w-64">
                <span className="text-sm font-semibold text-ink">Date</span>
                <input
                  type="date"
                  min={todayInputValue()}
                  max={maxDateInputValue()}
                  className="h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                />
              </label>

              <div className="mt-5">
                {slotsLoading && <p className="text-sm text-muted">Loading slots…</p>}
                {slotsError && <p className="text-sm font-medium text-danger-600">{slotsError}</p>}
                {!slotsLoading && !slotsError && slots.length > 0 && (
                  <div className="flex flex-col gap-5">
                    <SlotGroup label="Afternoon" slots={afternoonSlots} selectedSlot={selectedSlot} onSelect={setSelectedSlot} />
                    <SlotGroup label="Evening" slots={eveningSlots} selectedSlot={selectedSlot} onSelect={setSelectedSlot} />
                  </div>
                )}
              </div>
            </section>

            {/* Reason for visit */}
            <section className="rounded-2xl border border-border bg-white p-6">
              <h2 className="text-lg font-semibold text-ink">Reason for visit (optional)</h2>
              <textarea
                rows={3}
                className="mt-4 w-full resize-none rounded-lg border border-border bg-white px-4 py-3 text-base text-ink placeholder-placeholder outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                placeholder="Briefly describe what's going on with your pet…"
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
              />
            </section>

            <Button type="submit" variant="primary" className="w-full" disabled={!canSubmit || submitting}>
              {submitting ? "Booking…" : "Confirm booking"}
            </Button>

            <p className="text-center text-sm text-muted">
              Need help?{" "}
              <Link to="/#faqs" className="font-semibold text-primary-600 hover:text-primary-700">
                Check our FAQs
              </Link>
            </p>
          </form>
        </div>
      </main>
      <Footer />
    </div>
  );
}

function SlotGroup({
  label,
  slots,
  selectedSlot,
  onSelect,
}: {
  label: string;
  slots: api.Slot[];
  selectedSlot: api.Slot | null;
  onSelect: (slot: api.Slot) => void;
}) {
  if (slots.length === 0) return null;
  return (
    <div>
      <h3 className="text-sm font-semibold text-muted">{label}</h3>
      <div className="mt-2 grid grid-cols-3 gap-2 sm:grid-cols-4">
        {slots.map((slot) => {
          const isSelected = selectedSlot?.start === slot.start;
          return (
            <button
              key={slot.start}
              type="button"
              disabled={!slot.available}
              onClick={() => onSelect(slot)}
              className={`h-11 rounded-lg border text-sm font-medium transition-colors ${
                isSelected
                  ? "border-ink bg-ink text-white"
                  : slot.available
                    ? "border-border bg-white text-ink hover:border-ink"
                    : "cursor-not-allowed border-border bg-gray-50 text-placeholder line-through"
              }`}
            >
              {formatSlotTime(slot.start)}
            </button>
          );
        })}
      </div>
    </div>
  );
}
