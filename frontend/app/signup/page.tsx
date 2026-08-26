import Link from 'next/link'
import { AuthShell } from '@/components/auth/AuthShell'
import { SignupForm } from '@/components/auth/SignupForm'

export const metadata = {
  title: 'Create your account — EcoSync',
  description: 'Create an EcoSync account to get a personalized 48-hour solar forecast for your panels.',
}

export default function SignupPage() {
  return (
    <AuthShell
      eyebrow="Get started"
      headline="Make the sun"
      headlineAccent="work for you."
      blurb="Create an account to get a personalized 48-hour forecast built around your panel capacity, tilt and orientation."
      footer={
        <>
          Already have an account?{' '}
          <Link
            href="/login"
            className="font-bold text-slate-900 underline decoration-amber-300 decoration-2 underline-offset-4 hover:decoration-amber-500"
          >
            Sign in
          </Link>
        </>
      }
    >
      <div className="mb-7">
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">Create account</h2>
        <p className="mt-1.5 text-sm text-slate-500">Start forecasting your solar output today.</p>
      </div>
      <SignupForm />
    </AuthShell>
  )
}
