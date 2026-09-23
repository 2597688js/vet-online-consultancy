import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import * as api from "../lib/api";

interface AuthContextValue {
  user: api.User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<api.User>;
  register: (input: { fullName: string; email: string; phone: string; password: string }) => Promise<void>;
  loginWithGoogle: (credential: string) => Promise<api.User>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<api.User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = api.getToken();
    if (!token) {
      setLoading(false);
      return;
    }
    api
      .fetchMe(token)
      .then(setUser)
      .catch(() => api.clearToken())
      .finally(() => setLoading(false));
  }, []);

  async function login(email: string, password: string) {
    const res = await api.login({ email, password });
    api.setToken(res.access_token);
    setUser(res.user);
    return res.user;
  }

  async function register(input: { fullName: string; email: string; phone: string; password: string }) {
    const res = await api.registerMember({
      full_name: input.fullName,
      email: input.email,
      phone: input.phone,
      password: input.password,
    });
    api.setToken(res.access_token);
    setUser(res.user);
  }

  async function loginWithGoogle(credential: string) {
    const res = await api.googleAuth(credential);
    api.setToken(res.access_token);
    setUser(res.user);
    return res.user;
  }

  function logout() {
    api.clearToken();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, loginWithGoogle, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
