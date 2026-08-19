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

export class ApiError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`/api${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
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
  return request<User>("/auth/me", { headers: { Authorization: `Bearer ${token}` } });
}
