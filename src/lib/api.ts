export interface User {
  id: string;
  full_name: string;
  email: string;
  phone: string | null;
  role: "OWNER" | "VET" | "ADMIN";
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export type PetGender = "MALE" | "FEMALE" | "UNKNOWN";

export interface PetPhoto {
  id: string;
  url: string;
  created_at: string;
}

export interface Pet {
  id: string;
  name: string;
  species: string;
  breed: string | null;
  gender: PetGender;
  date_of_birth: string | null;
  weight_kg: string | null;
  color: string | null;
  allergies: string | null;
  existing_conditions: string | null;
  current_medications: string | null;
  photos: PetPhoto[];
  created_at: string;
}

export interface Slot {
  start: string;
  end: string;
  available: boolean;
}

export type AppointmentStatus = "PENDING" | "CONFIRMED" | "COMPLETED" | "CANCELLED";

export interface Appointment {
  id: string;
  pet: Pet;
  consultation_type: "VIDEO" | "AUDIO" | "CHAT";
  duration_minutes: number;
  price_at_booking: string;
  currency: string;
  scheduled_start: string;
  scheduled_end: string;
  symptoms: string | null;
  status: AppointmentStatus;
  confirmed_at: string | null;
  cancellation_reason: string | null;
  created_at: string;
}

export interface AppointmentAdmin extends Appointment {
  owner_name: string;
  owner_email: string;
  owner_phone: string | null;
}

export class ApiError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ApiError";
  }
}

const TOKEN_KEY = "vet_consult_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

function authHeaders(token: string): HeadersInit {
  return { Authorization: `Bearer ${token}` };
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const isFormData = options.body instanceof FormData;
  const res = await fetch(`/api${path}`, {
    ...options,
    headers: {
      ...(isFormData ? {} : { "Content-Type": "application/json" }),
      ...options.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => null);
    const message = body?.detail ?? "Something went wrong. Please try again.";
    throw new ApiError(typeof message === "string" ? message : "Something went wrong. Please try again.");
  }

  return res.json() as Promise<T>;
}

export function registerMember(input: { full_name: string; email: string; phone: string; password: string }) {
  return request<AuthResponse>("/auth/register", { method: "POST", body: JSON.stringify(input) });
}

export function login(input: { email: string; password: string }) {
  return request<AuthResponse>("/auth/login", { method: "POST", body: JSON.stringify(input) });
}

export function googleAuth(credential: string) {
  return request<AuthResponse>("/auth/google", { method: "POST", body: JSON.stringify({ credential }) });
}

export function fetchMe(token: string) {
  return request<User>("/auth/me", { headers: authHeaders(token) });
}

export interface PetInput {
  name: string;
  species: string;
  breed?: string;
  gender?: PetGender;
  date_of_birth?: string;
  weight_kg?: string;
  color?: string;
  allergies?: string;
  existing_conditions?: string;
  current_medications?: string;
}

export function createPet(token: string, input: PetInput) {
  return request<Pet>("/pets", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(input),
  });
}

export function uploadPetPhotos(token: string, petId: string, files: File[]) {
  const form = new FormData();
  files.forEach((file) => form.append("files", file));
  return request<Pet>(`/pets/${petId}/photos`, {
    method: "POST",
    headers: authHeaders(token),
    body: form,
  });
}

export function deletePetPhoto(token: string, petId: string, photoId: string) {
  return request<Pet>(`/pets/${petId}/photos/${photoId}`, {
    method: "DELETE",
    headers: authHeaders(token),
  });
}

export function getSlots(token: string, bookingDate: string) {
  return request<Slot[]>(`/appointments/slots?booking_date=${bookingDate}`, {
    headers: authHeaders(token),
  });
}

export function createAppointment(token: string, input: { pet_id: string; scheduled_start: string; symptoms?: string }) {
  return request<Appointment>("/appointments", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(input),
  });
}

export function listMyAppointments(token: string) {
  return request<Appointment[]>("/appointments/me", {
    headers: authHeaders(token),
  });
}

export function listAdminAppointments(token: string, status?: AppointmentStatus) {
  const qs = status ? `?status=${status}` : "";
  return request<AppointmentAdmin[]>(`/admin/appointments${qs}`, {
    headers: authHeaders(token),
  });
}

export function updateAppointmentStatus(
  token: string,
  appointmentId: string,
  input: { status: AppointmentStatus; cancellation_reason?: string }
) {
  return request<AppointmentAdmin>(`/admin/appointments/${appointmentId}/status`, {
    method: "PATCH",
    headers: authHeaders(token),
    body: JSON.stringify(input),
  });
}
