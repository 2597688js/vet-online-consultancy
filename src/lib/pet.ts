import type { Pet, PetGender } from "./api";

export const SEX_LABELS: Record<PetGender, string> = {
  MALE: "Male",
  FEMALE: "Female",
  UNKNOWN: "Not sure",
};

export function petLabel(pet: Pet): string {
  return pet.name || `Unnamed ${pet.species.toLowerCase()}`;
}

// Owners give an age, which is stored as an approximate date of birth so it stays correct over time.
export function dateOfBirthFromAge(years: number, months: number): string {
  const d = new Date();
  d.setMonth(d.getMonth() - (years * 12 + months));
  const offset = d.getTimezoneOffset();
  return new Date(d.getTime() - offset * 60_000).toISOString().slice(0, 10);
}

export function formatAge(dateOfBirth: string | null): string | null {
  if (!dateOfBirth) return null;
  const dob = new Date(dateOfBirth);
  const now = new Date();
  let totalMonths = (now.getFullYear() - dob.getFullYear()) * 12 + (now.getMonth() - dob.getMonth());
  if (now.getDate() < dob.getDate()) totalMonths -= 1;
  totalMonths = Math.max(0, totalMonths);
  const years = Math.floor(totalMonths / 12);
  const months = totalMonths % 12;
  const parts = [];
  if (years > 0) parts.push(`${years} yr${years === 1 ? "" : "s"}`);
  if (months > 0 || years === 0) parts.push(`${months} mo`);
  return parts.join(" ");
}
