import { Link } from "react-router-dom";
import { Input } from "../components/Input";
import { Button } from "../components/Button";
import { PawIcon } from "../components/icons";

export function Login() {
  return (
    <div className="flex min-h-screen flex-col bg-bg">
      <div className="flex flex-1 items-center justify-center px-6 py-16">
        <div className="w-full max-w-[420px] rounded-2xl border border-border bg-white p-10">
          <div className="flex flex-col items-center text-center">
            <Link to="/" className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary-600 text-white">
              <PawIcon className="h-6 w-6" />
            </Link>
            <h1 className="mt-5 text-2xl font-bold text-ink">Welcome Back</h1>
            <p className="mt-2 text-sm text-muted">Log in to manage your pets and appointments.</p>
          </div>

          <form
            className="mt-8 flex flex-col gap-5"
            onSubmit={(e) => e.preventDefault()}
          >
            <Input label="Email" type="email" name="email" placeholder="you@example.com" autoComplete="email" required />

            <div className="flex flex-col gap-2">
              <Input label="Password" type="password" name="password" placeholder="••••••••" autoComplete="current-password" required />
              <div className="flex justify-end">
                <a href="#" className="text-sm font-medium text-primary-600 hover:text-primary-700">
                  Forgot password?
                </a>
              </div>
            </div>

            <Button type="submit" variant="primary" className="w-full">
              Login
            </Button>
          </form>

          <div className="my-6 flex items-center gap-4">
            <span className="h-px flex-1 bg-border" />
            <span className="text-xs font-medium uppercase text-placeholder">or</span>
            <span className="h-px flex-1 bg-border" />
          </div>

          <button className="flex h-12 w-full items-center justify-center gap-3 rounded-lg border border-border text-sm font-semibold text-ink transition-colors hover:bg-gray-50">
            <GoogleIcon className="h-5 w-5" />
            Continue with Google
          </button>

          <p className="mt-8 text-center text-sm text-muted">
            Don&apos;t have an account?{" "}
            <Link to="/register" className="font-semibold text-primary-600 hover:text-primary-700">
              Register
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

function GoogleIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" {...props}>
      <path
        fill="#4285F4"
        d="M23.49 12.27c0-.79-.07-1.54-.19-2.27H12v4.51h6.47c-.29 1.48-1.14 2.73-2.43 3.58v3h3.93c2.3-2.12 3.52-5.24 3.52-8.82z"
      />
      <path
        fill="#34A853"
        d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.93-3c-1.09.73-2.5 1.16-4 1.16-3.08 0-5.68-2.08-6.61-4.87H1.34v3.09C3.31 21.3 7.33 24 12 24z"
      />
      <path
        fill="#FBBC05"
        d="M5.39 14.38A7.2 7.2 0 0 1 5 12c0-.83.14-1.63.39-2.38V6.53H1.34A11.98 11.98 0 0 0 0 12c0 1.94.46 3.77 1.34 5.47z"
      />
      <path
        fill="#EA4335"
        d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.45-3.45C17.94 1.19 15.24 0 12 0 7.33 0 3.31 2.7 1.34 6.53l4.05 3.09C6.32 6.83 8.92 4.75 12 4.75z"
      />
    </svg>
  );
}
