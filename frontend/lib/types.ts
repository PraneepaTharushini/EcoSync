// Shared types — keep in sync with backend/app/schemas/*.py and docs/data-contract.md

export interface User {
  id: string
  email: string
  createdAt: string
}

export interface AuthResponse {
  token: string
  user: User
}

export interface LoginPayload {
  email: string
  password: string
}

export interface SignupPayload {
  email: string
  password: string
}

export interface ApiError {
  detail: string
}
