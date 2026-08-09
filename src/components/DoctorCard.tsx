import type { ReactNode } from "react";
import { Button } from "./Button";
import { StarIcon } from "./icons";

interface DoctorCardProps {
  name: string;
  specialty: string;
  rating: number;
  experience: string;
  price: string;
  initials: string;
  emoji: ReactNode;
}

export function DoctorCard({ name, specialty, rating, experience, price, initials, emoji }: DoctorCardProps) {
  return (
    <div className="flex flex-col gap-4 rounded-2xl border border-border bg-white p-6">
      <div className="flex h-40 items-center justify-center rounded-xl bg-primary-50 text-5xl" aria-hidden>
        {emoji}
      </div>
      <div>
        <h3 className="text-lg font-semibold text-ink">{name}</h3>
        <p className="text-sm text-muted">{specialty}</p>
      </div>
      <div className="flex items-center gap-3 text-sm text-muted">
        <span className="flex items-center gap-1 font-medium text-ink">
          <StarIcon className="h-4 w-4 text-amber-400" />
          {rating}
        </span>
        <span aria-hidden>·</span>
        <span>{experience}</span>
      </div>
      <div className="flex items-center justify-between">
        <span className="text-base font-semibold text-ink">{price}</span>
        <span className="flex h-9 w-9 items-center justify-center rounded-full bg-gray-100 text-xs font-semibold text-muted">
          {initials}
        </span>
      </div>
      <Button variant="secondary" href="/login" className="w-full">
        View Profile
      </Button>
    </div>
  );
}
