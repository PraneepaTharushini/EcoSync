import Link from 'next/link'
import { Sun } from 'lucide-react'
import { SignupForm } from '@/components/auth/SignupForm'

export default function SignupPage() {
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
          <p className="text-sm font-bold uppercase tracking-[0.18em] text-amber-600">Get started</p>
          <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">
            Make the sun
            <br />
            <span className="text-amber-500">work for you.</span>
          </h1>
          <p className="mt-5 max-w-sm text-base leading-7 text-slate-500">
            Create an account to get a personalized 48-hour forecast for your panels.
          </p>
        </div>

        <div className="mt-8">
          <SignupForm />
        </div>

        <p className="mt-6 text-center text-sm text-slate-500">
          Already have an account?{' '}
          <Link href="/login" className="font-bold text-slate-900 underline decoration-amber-300 underline-offset-4">
            Sign in
          </Link>
        </p>
      </div>
    </main>
  )
}
