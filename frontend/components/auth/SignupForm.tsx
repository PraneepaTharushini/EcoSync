'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Eye, EyeOff, Lock, Mail } from 'lucide-react'
import { signup, saveToken } from '@/lib/api'

export function SignupForm() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)

    if (!email.trim() || !password) {
      setError('Enter your email and a password.')
      return
    }
    if (password.length < 8) {
      setError('Password needs at least 8 characters.')
      return
    }
    if (password !== confirmPassword) {
      setError('Passwords don\u2019t match.')
      return
    }

    setLoading(true)
    try {
      const { token } = await signup({ email: email.trim(), password })
      saveToken(token)
      router.push('/')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not create your account. Try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4" noValidate>
      <label className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-100">
        <span className="flex items-center gap-2 text-xs font-bold text-slate-500">
          <Mail className="size-4 text-amber-500" /> Email
        </span>
        <input
          type="email"
          autoComplete="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          className="mt-2 w-full bg-transparent text-sm font-semibold text-slate-900 outline-none placeholder:font-normal placeholder:text-slate-400"
        />
      </label>

      <label className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-100">
        <span className="flex items-center justify-between text-xs font-bold text-slate-500">
          <span className="flex items-center gap-2">
            <Lock className="size-4 text-amber-500" /> Password
          </span>
        </span>
        <span className="mt-2 flex items-center gap-2">
          <input
            type={showPassword ? 'text' : 'password'}
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="At least 8 characters"
            className="w-full bg-transparent text-sm font-semibold text-slate-900 outline-none placeholder:font-normal placeholder:text-slate-400"
          />
          <button
            type="button"
            onClick={() => setShowPassword((v) => !v)}
            className="text-slate-400"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? <EyeOff className="size-4" /> : <Eye className="size-4" />}
          </button>
        </span>
      </label>

      <label className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-100">
        <span className="flex items-center gap-2 text-xs font-bold text-slate-500">
          <Lock className="size-4 text-amber-500" /> Confirm password
        </span>
        <input
          type={showPassword ? 'text' : 'password'}
          autoComplete="new-password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Re-enter your password"
          className="mt-2 w-full bg-transparent text-sm font-semibold text-slate-900 outline-none placeholder:font-normal placeholder:text-slate-400"
        />
      </label>

      {error && (
        <p role="alert" className="rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-600">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={loading}
        className="mt-2 flex w-full items-center justify-center gap-2 rounded-2xl bg-slate-900 py-4 font-bold text-white shadow-xl shadow-slate-200 disabled:opacity-60"
      >
        {loading ? 'Creating your account…' : 'Create Account'}
      </button>
    </form>
  )
}
