import type { ReactNode } from 'react'
import Link from 'next/link'
import { Sun } from 'lucide-react'

/**
 * Full-bleed hero background with the form card floating on top.
 * Backdrop photo: public/hero-solar.jpg — Rafael Moreno via Unsplash (see public/CREDITS.md).
 * Swap the file or pass a different `image` prop to change it; until a file exists the
 * amber/slate gradient underneath carries the design on its own.
 */
export function AuthShell({
  eyebrow,
  headline,
  headlineAccent,
  blurb,
  children,
  footer,
  image = '/hero-solar.jpg',
}: {
  eyebrow: string
  headline: string
  headlineAccent: string
  blurb: string
  children: ReactNode
  footer: ReactNode
  image?: string
}) {
  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-900">
      {/* layer 1 — themed gradient, always visible, also the fallback if the photo is absent */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-500 via-orange-600 to-slate-900" />

      {/* layer 2 — the photograph */}
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: `url('${image}')` }}
        aria-hidden="true"
      />

      {/* layer 3 — scrims that keep white text legible over any photo */}
      <div className="absolute inset-0 bg-slate-950/55" />
      <div className="absolute inset-0 bg-gradient-to-r from-slate-950/80 via-slate-950/40 to-transparent" />
      <div className="absolute inset-x-0 bottom-0 h-1/3 bg-gradient-to-t from-slate-950/80 to-transparent" />

      {/* ---------- content ---------- */}
      <div className="relative flex min-h-screen flex-col px-6 py-6 sm:px-10 lg:px-14">
        <header className="flex items-center">
          <Link href="/" className="flex items-center gap-2.5">
            <span className="flex size-9 items-center justify-center rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 text-white shadow-lg shadow-orange-900/30">
              <Sun className="size-5" />
            </span>
            <span className="text-lg font-bold tracking-tight text-white">EcoSync</span>
          </Link>
        </header>

        <div className="grid flex-1 items-center gap-12 py-12 lg:grid-cols-2 lg:gap-16">
          {/* headline over the image */}
          <div className="max-w-xl">
            <span className="inline-flex items-center gap-2 rounded-full bg-white/10 px-3.5 py-1.5 text-xs font-bold uppercase tracking-[0.14em] text-white ring-1 ring-white/25 backdrop-blur">
              <Sun className="size-3.5 text-amber-300" />
              {eyebrow}
            </span>

            <h1 className="mt-7 text-4xl font-bold leading-[1.05] tracking-tight text-white sm:text-5xl xl:text-6xl">
              {headline}
              <br />
              <span className="text-amber-400">{headlineAccent}</span>
            </h1>

            <p className="mt-6 max-w-md text-base leading-7 text-white/80 sm:text-lg sm:leading-8">
              {blurb}
            </p>

            <dl className="mt-10 hidden max-w-md grid-cols-3 gap-6 border-t border-white/20 pt-7 lg:grid">
              {[
                ['92%', 'Forecast accuracy'],
                ['48h', 'Look-ahead window'],
                ['5 min', 'Setup time'],
              ].map(([value, label]) => (
                <div key={label}>
                  <dt className="text-2xl font-bold tracking-tight text-white">{value}</dt>
                  <dd className="mt-1 text-xs font-medium text-white/65">{label}</dd>
                </div>
              ))}
            </dl>
          </div>

          {/* form card */}
          <div className="w-full justify-self-end lg:max-w-md">
            <div className="rounded-3xl bg-white p-7 shadow-2xl shadow-slate-950/40 ring-1 ring-white/10 sm:p-9">
              {children}
              <div className="mt-7 text-center text-sm text-slate-500">{footer}</div>
            </div>
          </div>
        </div>

        <footer className="flex flex-wrap items-center justify-between gap-3 text-xs text-white/50">
          <span>&copy; {new Date().getFullYear()} EcoSync</span>
          <span>Your data stays private</span>
        </footer>
      </div>
    </div>
  )
}
