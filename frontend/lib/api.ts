import type { AuthResponse, LoginPayload, SignupPayload, ApiError } from './types'

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

export const TOKEN_KEY = 'solarsense_token'

export async function login(payload: LoginPayload): Promise<AuthResponse> {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const err: ApiError = await res.json().catch(() => ({ detail: 'Something went wrong. Try again.' }))
    throw new Error(err.detail || 'Invalid email or password.')
  }

  return res.json()
}

export async function signup(payload: SignupPayload): Promise<AuthResponse> {
  const res = await fetch(`${API_URL}/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const err: ApiError = await res.json().catch(() => ({ detail: 'Could not create your account. Try again.' }))
    throw new Error(err.detail || 'Could not create your account. Try again.')
  }

  return res.json()
}

export function saveToken(token: string) {
  if (typeof window !== 'undefined') localStorage.setItem(TOKEN_KEY, token)
}

export function getToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem(TOKEN_KEY)
}

export function clearToken() {
  if (typeof window !== 'undefined') localStorage.removeItem(TOKEN_KEY)
}
