// Best-effort: registration only collects a bare phone number (no country
// code field anywhere in the app), and the business operates in India. A
// 10-digit number is assumed to be a local Indian mobile number and gets
// "91" prepended; anything else is passed through as-is.
export function buildWhatsAppLink(phone: string, message?: string): string {
  const digits = phone.replace(/\D/g, "");
  const normalized = digits.length === 10 ? `91${digits}` : digits;
  const query = message ? `?text=${encodeURIComponent(message)}` : "";
  return `https://wa.me/${normalized}${query}`;
}

const DOCTOR_WHATSAPP = import.meta.env.VITE_DOCTOR_WHATSAPP?.trim() ?? "";

const DEFAULT_DOCTOR_MESSAGE = "Hi Dr. Sarkar, I'd like to consult you about my pet.";

// Link for pet owners to message Dr. Sarkar directly. Null when VITE_DOCTOR_WHATSAPP isn't set,
// so callers can hide the link instead of pointing at a broken number.
export function doctorWhatsAppLink(message = DEFAULT_DOCTOR_MESSAGE): string | null {
  return DOCTOR_WHATSAPP ? buildWhatsAppLink(DOCTOR_WHATSAPP, message) : null;
}
