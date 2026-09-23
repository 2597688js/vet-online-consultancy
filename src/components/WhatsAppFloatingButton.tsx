import { useLocation } from "react-router-dom";
import { WhatsAppIcon } from "./icons";
import { doctorWhatsAppLink } from "../lib/whatsapp";

export function WhatsAppFloatingButton() {
  const { pathname } = useLocation();
  const href = doctorWhatsAppLink();
  if (!href || pathname.startsWith("/admin")) return null;

  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      aria-label="Chat with Dr. Sarkar on WhatsApp"
      className="fixed bottom-5 right-5 z-50 flex items-center gap-2 rounded-full bg-[#25D366] px-4 py-3 text-sm font-semibold text-white shadow-lg transition-transform hover:scale-105 sm:bottom-6 sm:right-6"
    >
      <WhatsAppIcon className="h-6 w-6" />
      <span className="hidden sm:inline">Chat on WhatsApp</span>
    </a>
  );
}
