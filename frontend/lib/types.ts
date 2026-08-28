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

export interface HourlyPrediction {
  forecast_time: string
  predicted_kwh: number
  model_version: string
}

export interface PredictedForecastResponse {
  user_id: string
  capacity_kw: number
  orientation: string
  predicted_count: number
  hourly: HourlyPrediction[]
}

export interface ApiError {
  detail: string
}