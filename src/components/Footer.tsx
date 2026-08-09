import { PawIcon } from "./icons";

const columns = [
  {
    title: "Company",
    links: ["About Us", "Careers", "Press", "Contact"],
  },
  {
    title: "Services",
    links: ["General Consultation", "Nutrition", "Skin & Allergy", "Dental"],
  },
  {
    title: "Support",
    links: ["Help Center", "FAQs", "Privacy Policy", "Terms of Service"],
  },
  {
    title: "Social",
    links: ["Instagram", "Facebook", "X (Twitter)", "LinkedIn"],
  },
];

export function Footer() {
  return (
    <footer className="border-t border-border bg-white">
      <div className="mx-auto max-w-7xl px-6 py-16 lg:px-20">
        <div className="grid grid-cols-2 gap-10 sm:grid-cols-3 lg:grid-cols-5">
          <div className="col-span-2 lg:col-span-1">
            <div className="flex items-center gap-2 text-lg font-bold text-ink">
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-600 text-white">
                <PawIcon className="h-5 w-5" />
              </span>
              VetConsult
            </div>
            <p className="mt-4 text-sm text-muted">
              Trusted online veterinary consultations, whenever your pet needs care.
            </p>
          </div>
          {columns.map((col) => (
            <div key={col.title}>
              <h4 className="text-sm font-semibold text-ink">{col.title}</h4>
              <ul className="mt-4 flex flex-col gap-3">
                {col.links.map((link) => (
                  <li key={link}>
                    <a href="#" className="text-sm text-muted hover:text-ink">
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-12 border-t border-border pt-6 text-sm text-muted">
          © {new Date().getFullYear()} VetConsult. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
