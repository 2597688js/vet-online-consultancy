import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Header } from "../components/Header";
import { Footer } from "../components/Footer";
import { Button } from "../components/Button";
import { PawIcon } from "../components/icons";
import { useAuth } from "../context/AuthContext";
import * as api from "../lib/api";
import { ApiError } from "../lib/api";
import { petLabel } from "../lib/pet";

const STATUS_BADGE_CLASSES: Record<api.AppointmentStatus, string> = {
  PENDING: "bg-amber-50 text-amber-700",
  CONFIRMED: "bg-blue-50 text-blue-700",
  COMPLETED: "bg-primary-50 text-primary-700",
  CANCELLED: "bg-danger-50 text-danger-600",
};

const STATUS_LABELS: Record<api.AppointmentStatus, string> = {
  PENDING: "Pending confirmation",
  CONFIRMED: "Confirmed",
  COMPLETED: "Completed",
  CANCELLED: "Cancelled",
};

function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString([], {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

export function MyAppointments() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  const [appointments, setAppointments] = useState<api.Appointment[]>([]);
  const [listLoading, setListLoading] = useState(false);
  const [listError, setListError] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && !user) {
      navigate("/login");
    }
  }, [loading, user, navigate]);

  useEffect(() => {
    const token = api.getToken();
    if (!user || !token) return;
    setListLoading(true);
    setListError(null);
    api
      .listMyAppointments(token)
      .then(setAppointments)
      .catch((err) => setListError(err instanceof ApiError ? err.message : "Couldn't load your appointments."))
      .finally(() => setListLoading(false));
  }, [user]);

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
              <h1 className="text-2xl font-bold text-ink">My appointments</h1>
              <p className="text-sm text-muted">Consultations with Dr. Nituparna Sarkar</p>
            </div>
          </div>

          <div className="mt-8 flex flex-col gap-4">
            {listLoading && <p className="text-sm text-muted">Loading…</p>}
            {listError && <p className="text-sm font-medium text-danger-600">{listError}</p>}
            {!listLoading && !listError && appointments.length === 0 && (
              <div className="rounded-2xl border border-dashed border-border bg-white p-8 text-center">
                <p className="text-sm text-muted">You haven't booked a consultation yet.</p>
                <Button variant="primary" href="/book" className="mt-4">
                  Book a consultation
                </Button>
              </div>
            )}

            {appointments.map((appointment) => (
              <div key={appointment.id} className="rounded-2xl border border-border bg-white p-6">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <h2 className="text-lg font-semibold text-ink">
                        {petLabel(appointment.pet)} <span className="font-normal text-muted">({appointment.pet.species})</span>
                      </h2>
                      <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${STATUS_BADGE_CLASSES[appointment.status]}`}>
                        {STATUS_LABELS[appointment.status]}
                      </span>
                    </div>
                    <p className="mt-1 text-sm text-muted">
                      {appointment.scheduled_start
                      ? formatDateTime(appointment.scheduled_start)
                      : `Requested ${formatDateTime(appointment.created_at)}`}
                    </p>
                    {appointment.symptoms && <p className="mt-2 text-sm text-body">"{appointment.symptoms}"</p>}
                    {appointment.status === "CONFIRMED" && (
                      <p className="mt-2 text-sm text-body">Dr. Sarkar will call you on WhatsApp video.</p>
                    )}
                    {appointment.status === "CANCELLED" && appointment.cancellation_reason && (
                      <p className="mt-2 text-sm text-danger-600">Cancelled — {appointment.cancellation_reason}</p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
