import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Header } from "../components/Header";
import { Footer } from "../components/Footer";
import { Button } from "../components/Button";
import { CameraIcon, CheckCircleIcon, PawIcon, XIcon } from "../components/icons";
import { useAuth } from "../context/AuthContext";
import * as api from "../lib/api";
import { ApiError } from "../lib/api";
import { SEX_LABELS, dateOfBirthFromAge, petLabel } from "../lib/pet";

const MAX_PHOTOS = 6;
const MAX_PHOTO_MB = 5;
const SPECIES_SUGGESTIONS = ["Dog", "Cat", "Bird", "Rabbit", "Guinea pig", "Hamster", "Fish", "Turtle", "Cow", "Goat"];

const inputClass =
  "h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink placeholder-placeholder outline-none focus:border-ink focus:ring-1 focus:ring-ink";
const textareaClass =
  "w-full resize-none rounded-lg border border-border bg-white px-4 py-3 text-base text-ink placeholder-placeholder outline-none focus:border-ink focus:ring-1 focus:ring-ink";

interface PetFormState {
  name: string;
  species: string;
  breed: string;
  gender: api.PetGender | "";
  ageYears: string;
  ageMonths: string;
  weightKg: string;
  color: string;
  medicalHistory: string;
  allergies: string;
  currentMedications: string;
}

const initialPetForm: PetFormState = {
  name: "",
  species: "",
  breed: "",
  gender: "",
  ageYears: "",
  ageMonths: "0",
  weightKg: "",
  color: "",
  medicalHistory: "",
  allergies: "",
  currentMedications: "",
};

interface PhotoDraft {
  file: File;
  previewUrl: string;
}

export function Book() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  const [ownerName, setOwnerName] = useState("");
  const [ownerPhone, setOwnerPhone] = useState("");
  const [pet, setPet] = useState<PetFormState>(initialPetForm);
  const [photos, setPhotos] = useState<PhotoDraft[]>([]);
  const [photoError, setPhotoError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

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
    if (!user) return;
    setOwnerName((prev) => prev || user.full_name);
    setOwnerPhone((prev) => prev || user.phone || "");
  }, [user]);

  useEffect(() => {
    return () => {
      photos.forEach((p) => URL.revokeObjectURL(p.previewUrl));
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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

  const ageYears = Number(pet.ageYears);
  const ageMonths = Number(pet.ageMonths);
  const ageValid = pet.ageYears !== "" && ageYears >= 0 && (ageYears > 0 || ageMonths > 0);

  const missingField = !ownerName.trim()
    ? "Please enter the owner's name."
    : ownerPhone.trim().length < 7
      ? "Please enter a valid contact number."
      : !pet.species.trim()
        ? "Please enter your pet's species."
        : !pet.breed.trim()
          ? "Please enter your pet's breed (or \"Mixed\" / \"Not sure\")."
          : !ageValid
            ? "Please enter your pet's age."
            : !pet.gender
              ? "Please select your pet's sex."
              : !symptoms.trim()
                ? "Please describe the main problem."
                : photos.length === 0
                  ? "Please upload at least one photo of your pet."
                  : null;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (missingField || !pet.gender) {
      setError(missingField);
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
        name: pet.name.trim() || undefined,
        species: pet.species.trim(),
        breed: pet.breed.trim(),
        gender: pet.gender,
        date_of_birth: dateOfBirthFromAge(ageYears, ageMonths),
        weight_kg: pet.weightKg || undefined,
        color: pet.color.trim() || undefined,
        medical_history: pet.medicalHistory.trim() || undefined,
        allergies: pet.allergies.trim() || undefined,
        current_medications: pet.currentMedications.trim() || undefined,
      });

      await api.uploadPetPhotos(
        token,
        createdPet.id,
        photos.map((p) => p.file)
      );

      const appointment = await api.createAppointment(token, {
        pet_id: createdPet.id,
        symptoms: symptoms.trim(),
        contact_name: ownerName.trim(),
        contact_phone: ownerPhone.trim(),
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
            <h1 className="mt-5 text-2xl font-bold text-ink">Consultation request sent</h1>
            <p className="mt-2 text-sm text-muted">
              We've booked {confirmed.pet.name ? `${confirmed.pet.name}'s` : "your pet's"} consultation request. Dr. Nituparna Sarkar will contact you
              on WhatsApp at {confirmed.contact_phone} to arrange the consultation.
            </p>
            <div className="mt-6 rounded-xl bg-bg p-5 text-left text-sm">
              <div className="flex justify-between py-1">
                <span className="text-muted">Pet</span>
                <span className="font-semibold text-ink">
                  {petLabel(confirmed.pet)} ({confirmed.pet.species})
                </span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-muted">Status</span>
                <span className="font-semibold text-ink">Waiting for Dr. Sarkar</span>
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

            {/* Owner details */}
            <section className="rounded-2xl border border-border bg-white p-6">
              <h2 className="text-lg font-semibold text-ink">Owner details</h2>
              <p className="mt-1 text-sm text-muted">Dr. Sarkar will call this number on WhatsApp video.</p>

              <div className="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Owner name</span>
                  <input
                    className={inputClass}
                    placeholder="e.g. Priya Das"
                    autoComplete="name"
                    required
                    value={ownerName}
                    onChange={(e) => setOwnerName(e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Contact number (WhatsApp)</span>
                  <input
                    type="tel"
                    className={inputClass}
                    placeholder="e.g. +91 98765 43210"
                    autoComplete="tel"
                    required
                    minLength={7}
                    maxLength={30}
                    value={ownerPhone}
                    onChange={(e) => setOwnerPhone(e.target.value)}
                  />
                </label>
              </div>
            </section>

            {/* Pet details */}
            <section className="rounded-2xl border border-border bg-white p-6">
              <h2 className="text-lg font-semibold text-ink">Pet details</h2>
              <p className="mt-1 text-sm text-muted">Tell us about the pet you'd like Dr. Sarkar to see.</p>

              <div className="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Pet name (optional)</span>
                  <input
                    className={inputClass}
                    placeholder="e.g. Bruno"
                    value={pet.name}
                    onChange={(e) => updatePetField("name", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Species</span>
                  <input
                    className={inputClass}
                    placeholder="e.g. Dog, Cat"
                    list="species-suggestions"
                    required
                    value={pet.species}
                    onChange={(e) => updatePetField("species", e.target.value)}
                  />
                  <datalist id="species-suggestions">
                    {SPECIES_SUGGESTIONS.map((species) => (
                      <option key={species} value={species} />
                    ))}
                  </datalist>
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Breed</span>
                  <input
                    className={inputClass}
                    placeholder="e.g. Labrador, or Mixed / Not sure"
                    required
                    value={pet.breed}
                    onChange={(e) => updatePetField("breed", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Sex</span>
                  <select
                    className="h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                    required
                    value={pet.gender}
                    onChange={(e) => updatePetField("gender", e.target.value as api.PetGender | "")}
                  >
                    <option value="" disabled>
                      Select sex
                    </option>
                    {(["MALE", "FEMALE", "UNKNOWN"] as const).map((gender) => (
                      <option key={gender} value={gender}>
                        {SEX_LABELS[gender]}
                      </option>
                    ))}
                  </select>
                </label>

                <fieldset className="flex flex-col gap-2">
                  <legend className="mb-2 text-sm font-semibold text-ink">Age</legend>
                  <div className="grid grid-cols-2 gap-3">
                    <label className="relative">
                      <span className="sr-only">Years</span>
                      <input
                        type="number"
                        min="0"
                        max="50"
                        step="1"
                        className={`${inputClass} pr-14`}
                        placeholder="0"
                        required
                        value={pet.ageYears}
                        onChange={(e) => updatePetField("ageYears", e.target.value)}
                      />
                      <span className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-sm text-muted">
                        years
                      </span>
                    </label>
                    <label>
                      <span className="sr-only">Months</span>
                      <select
                        className="h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink outline-none focus:border-ink focus:ring-1 focus:ring-ink"
                        value={pet.ageMonths}
                        onChange={(e) => updatePetField("ageMonths", e.target.value)}
                      >
                        {Array.from({ length: 12 }, (_, m) => (
                          <option key={m} value={String(m)}>
                            {m} {m === 1 ? "month" : "months"}
                          </option>
                        ))}
                      </select>
                    </label>
                  </div>
                </fieldset>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Weight in kg (optional)</span>
                  <input
                    type="number"
                    min="0"
                    step="0.1"
                    className={inputClass}
                    placeholder="e.g. 12.5"
                    value={pet.weightKg}
                    onChange={(e) => updatePetField("weightKg", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2 sm:col-span-2">
                  <span className="text-sm font-semibold text-ink">Color / markings (optional)</span>
                  <input
                    className={inputClass}
                    placeholder="e.g. Brown with white patch"
                    value={pet.color}
                    onChange={(e) => updatePetField("color", e.target.value)}
                  />
                </label>
              </div>
            </section>

            {/* Health */}
            <section className="rounded-2xl border border-border bg-white p-6">
              <h2 className="text-lg font-semibold text-ink">Health information</h2>
              <p className="mt-1 text-sm text-muted">The more Dr. Sarkar knows beforehand, the more useful the call.</p>

              <div className="mt-5 flex flex-col gap-5">
                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Main problem</span>
                  <textarea
                    rows={3}
                    className={textareaClass}
                    placeholder="What's wrong, since when, and any changes in eating, drinking, or behaviour…"
                    required
                    value={symptoms}
                    onChange={(e) => setSymptoms(e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Medical history (optional)</span>
                  <textarea
                    rows={3}
                    className={textareaClass}
                    placeholder="Past illnesses, surgeries, vaccinations, deworming, neutering…"
                    value={pet.medicalHistory}
                    onChange={(e) => updatePetField("medicalHistory", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Current medications (optional)</span>
                  <textarea
                    rows={2}
                    className={textareaClass}
                    value={pet.currentMedications}
                    onChange={(e) => updatePetField("currentMedications", e.target.value)}
                  />
                </label>

                <label className="flex flex-col gap-2">
                  <span className="text-sm font-semibold text-ink">Allergies (optional)</span>
                  <textarea
                    rows={2}
                    className={textareaClass}
                    value={pet.allergies}
                    onChange={(e) => updatePetField("allergies", e.target.value)}
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

            <Button type="submit" variant="primary" className="w-full" disabled={submitting}>
              {submitting ? "Submitting…" : "Submit consultation request"}
            </Button>
          </form>
        </div>
      </main>
      <Footer />
    </div>
  );
}

