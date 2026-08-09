import type { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

export function Input({ label, id, ...rest }: InputProps) {
  const inputId = id ?? label.toLowerCase().replace(/\s+/g, "-");
  return (
    <label htmlFor={inputId} className="flex flex-col gap-2">
      <span className="text-sm font-semibold text-ink">{label}</span>
      <input
        id={inputId}
        {...rest}
        className="h-12 w-full rounded-lg border border-border bg-white px-4 text-base text-ink placeholder-placeholder outline-none transition-colors focus:border-ink focus:ring-1 focus:ring-ink"
      />
    </label>
  );
}
