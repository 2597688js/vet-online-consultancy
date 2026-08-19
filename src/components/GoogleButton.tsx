import { useEffect, useRef } from "react";

interface GoogleCredentialResponse {
  credential: string;
}

declare global {
  interface Window {
    google?: {
      accounts: {
        id: {
          initialize: (config: {
            client_id: string;
            callback: (response: GoogleCredentialResponse) => void;
          }) => void;
          renderButton: (parent: HTMLElement, options: Record<string, unknown>) => void;
        };
      };
    };
  }
}

const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
const GSI_SCRIPT_SRC = "https://accounts.google.com/gsi/client";

interface GoogleButtonProps {
  onCredential: (credential: string) => void;
  text?: "signin_with" | "signup_with" | "continue_with";
}

export function GoogleButton({ onCredential, text = "continue_with" }: GoogleButtonProps) {
  const buttonRef = useRef<HTMLDivElement>(null);
  const onCredentialRef = useRef(onCredential);
  onCredentialRef.current = onCredential;

  useEffect(() => {
    if (!CLIENT_ID) return;

    function render() {
      if (!window.google || !buttonRef.current) return;
      window.google.accounts.id.initialize({
        client_id: CLIENT_ID,
        callback: (response) => onCredentialRef.current(response.credential),
      });
      window.google.accounts.id.renderButton(buttonRef.current, {
        theme: "outline",
        size: "large",
        width: 360,
        text,
      });
    }

    if (window.google) {
      render();
      return;
    }

    const script = document.querySelector<HTMLScriptElement>(`script[src="${GSI_SCRIPT_SRC}"]`);
    script?.addEventListener("load", render, { once: true });
    return () => script?.removeEventListener("load", render);
  }, [text]);

  if (!CLIENT_ID) return null;

  return <div ref={buttonRef} className="flex w-full justify-center" />;
}
