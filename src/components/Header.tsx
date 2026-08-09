import { Link, NavLink } from "react-router-dom";
import { useState } from "react";
import { Button } from "./Button";
import { PawIcon } from "./icons";

const navLinks = [
  { label: "Home", href: "/" },
  { label: "How It Works", href: "/#how-it-works" },
  { label: "Services", href: "/#services" },
  { label: "Veterinarians", href: "/#veterinarians" },
  { label: "FAQs", href: "/#faqs" },
];

export function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-white/90 backdrop-blur">
      <div className="mx-auto flex h-[72px] max-w-7xl items-center justify-between px-6 lg:px-20">
        <Link to="/" className="flex items-center gap-2 text-lg font-bold text-ink">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-600 text-white">
            <PawIcon className="h-5 w-5" />
          </span>
          VetConsult
        </Link>

        <nav className="hidden items-center gap-8 lg:flex">
          {navLinks.map((link) => (
            <NavLink
              key={link.label}
              to={link.href}
              className="text-sm font-medium text-body transition-colors hover:text-ink"
            >
              {link.label}
            </NavLink>
          ))}
        </nav>

        <div className="hidden items-center gap-3 lg:flex">
          <Button variant="text" href="/login">
            Login
          </Button>
          <Button variant="primary" href="/login">
            Book Now
          </Button>
        </div>

        <button
          aria-label="Toggle menu"
          className="flex h-10 w-10 items-center justify-center rounded-lg border border-border lg:hidden"
          onClick={() => setMenuOpen((v) => !v)}
        >
          <span className="sr-only">Menu</span>
          <div className="flex flex-col gap-1">
            <span className="h-0.5 w-5 bg-ink" />
            <span className="h-0.5 w-5 bg-ink" />
            <span className="h-0.5 w-5 bg-ink" />
          </div>
        </button>
      </div>

      {menuOpen && (
        <div className="flex flex-col gap-1 border-t border-border bg-white px-6 py-4 lg:hidden">
          {navLinks.map((link) => (
            <a key={link.label} href={link.href} className="rounded-lg px-3 py-2 text-sm font-medium text-body hover:bg-gray-50">
              {link.label}
            </a>
          ))}
          <div className="mt-2 flex gap-3 px-3">
            <Button variant="secondary" href="/login" className="flex-1">
              Login
            </Button>
            <Button variant="primary" href="/login" className="flex-1">
              Book Now
            </Button>
          </div>
        </div>
      )}
    </header>
  );
}
