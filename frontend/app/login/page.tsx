import Link from 'next/link'
import { AuthShell } from '@/components/auth/AuthShell'
import { LoginForm } from '@/components/auth/LoginForm'

export const metadata = {
  title: 'Sign in — EcoSync',
  description: 'Sign in to see your solar forecast, log today’s output and keep your predictions accurate.',
}

export default function LoginPage() {
  return (
    <AuthShell
      eyebrow="Welcome back"
      headline="Brighter days begin"
      headlineAccent="with clean power."
      blurb="EcoSync turns local weather into a clear picture of what your rooftop will generate — so you can plan the wash, the charge and the bill around the sun."
      footer={
        <>
          New to EcoSync?{' '}
          <Link
            href="/signup"
            className="font-bold text-slate-900 underline decoration-amber-300 decoration-2 underline-offset-4 hover:decoration-amber-500"
          >
            Create an account
          </Link>
        </>
      }
    >
      <div className="mb-7">
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">Sign in</h2>
        <p className="mt-1.5 text-sm text-slate-500">Welcome back — let’s check today’s sun.</p>
      </div>
      <LoginForm />
    </AuthShell>
  )
}
