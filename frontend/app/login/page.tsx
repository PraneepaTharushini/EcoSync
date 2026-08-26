import Link from 'next/link'
import { Sun } from 'lucide-react'
import { LoginForm } from '@/components/auth/LoginForm'

export default function LoginPage() {
  return (
    <main className="flex min-h-screen flex-col bg-gradient-to-b from-amber-50 via-white to-sky-50 px-6 py-8">
      <div className="mx-auto flex w-full max-w-md flex-1 flex-col">
        <div className="flex items-center gap-2 font-bold text-slate-900">
          <span className="flex size-8 items-center justify-center rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 text-white">
            <Sun className="size-5" />
          </span>
          SolarSense
        </div>

        <div className="mt-10">
          <p className="text-sm font-bold uppercase tracking-[0.18em] text-amber-600">Welcome back</p>
          <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">
            Let's check
            <br />
            <span className="text-amber-500">today's sun.</span>
          </h1>
          <p className="mt-5 max-w-sm text-base leading-7 text-slate-500">
            Sign in to see your forecast, log today's output, and keep your predictions accurate.
          </p>
        </div>

        <div className="mt-8">
          <LoginForm />
        </div>

        <p className="mt-6 text-center text-sm text-slate-500">
          New to SolarSense?{' '}
          <Link href="/signup" className="font-bold text-slate-900 underline decoration-amber-300 underline-offset-4">
            Create an account
          </Link>
        </p>
      </div>
    </main>
  )
}
