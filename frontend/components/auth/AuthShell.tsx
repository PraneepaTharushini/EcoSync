import type { ReactNode } from 'react'
import Link from 'next/link'
import { BarChart3, CloudSun, ShieldCheck, Sun } from 'lucide-react'

const highlights = [
  { icon: BarChart3, title: '48-hour output forecast', body: 'Hour-by-hour predictions tuned to your panel capacity, tilt and orientation.' },
  { icon: CloudSun, title: 'Live weather intelligence', body: 'Cloud cover, temperature and irradiance folded into every estimate.' },
  { icon: ShieldCheck, title: 'Accuracy that improves', body: 'Log your real output and the model keeps calibrating to your roof.' },
]

const stats = [
  { value: '92%', label: 'Forecast accuracy' },
  { value: '48h', label: 'Look-ahead window' },
  { value: '5 min', label: 'Setup time' },
]

export function AuthShell({
  eyebrow,
  title,
  titleAccent,
  subtitle,
  navPrompt,
  navLabel,
  navHref,
  children,
  footer,
}: {
  eyebrow: string
  title: string
  titleAccent: string
  subtitle: string
  navPrompt: string
  navLabel: string
  navHref: string
  children: ReactNode
  footer: ReactNode
}) {
  return (
    <div className="min-h-screen bg-white lg:grid lg:grid-cols-[1fr_1.1fr]">
      {/* ---------- left: form column ---------- */}
      <div className="flex min-h-screen flex-col px-6 py-7 sm:px-10 lg:px-14 xl:px-20">
        <header className="flex items-center justify-between gap-4">
          <Link href="/" className="flex items-center gap-2.5">
            <span className="flex size-9 items-center justify-center rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 text-white shadow-md shadow-amber-200">
              <Sun className="size-5" />
            </span>
            <span className="text-lg font-bold tracking-tight text-slate-900">EcoSync</span>
          </Link>

          <p className="hidden text-sm text-slate-500 sm:block">
            {navPrompt}{' '}
            <Link
              href={navHref}
              className="font-bold text-slate-900 underline decoration-amber-300 decoration-2 underline-offset-4 hover:decoration-amber-500"
            >
              {navLabel}
            </Link>
          </p>
        </header>

        <div className="flex flex-1 items-center py-10 lg:py-14">
          <div className="mx-auto w-full max-w-md">
            <p className="text-xs font-bold uppercase tracking-[0.18em] text-amber-600">{eyebrow}</p>
            <h1 className="mt-3 text-4xl font-bold leading-[1.1] tracking-tight text-slate-900">
              {title}
              <br />
              <span className="text-amber-500">{titleAccent}</span>
            </h1>
            <p className="mt-4 text-base leading-7 text-slate-500">{subtitle}</p>

            <div className="mt-8">{children}</div>

            <div className="mt-7 text-center text-sm text-slate-500">{footer}</div>
          </div>
        </div>

        <footer className="flex flex-wrap items-center justify-between gap-3 text-xs text-slate-400">
          <span>&copy; {new Date().getFullYear()} EcoSync</span>
          <span className="flex items-center gap-1.5">
            <ShieldCheck className="size-3.5 text-amber-500" />
            Your data stays private
          </span>
        </footer>
      </div>

      {/* ---------- right: brand panel ---------- */}
      <aside className="relative hidden overflow-hidden bg-slate-900 lg:block">
        {/* warm gradient wash, same amber/orange family as the app */}
        <div className="absolute inset-0 bg-gradient-to-br from-amber-400 via-orange-500 to-amber-600" />
        <div className="absolute -left-24 top-1/4 size-[28rem] rounded-full bg-amber-200/40 blur-3xl" />
        <div className="absolute -bottom-32 -right-16 size-[32rem] rounded-full bg-orange-700/40 blur-3xl" />
        <div className="absolute inset-x-0 bottom-0 h-2/3 bg-gradient-to-t from-slate-900/70 to-transparent" />

        <div className="relative flex h-full flex-col justify-between px-12 py-14 xl:px-16">
          <div>
            <span className="inline-flex items-center gap-2 rounded-full bg-white/15 px-3.5 py-1.5 text-xs font-bold uppercase tracking-[0.14em] text-white ring-1 ring-white/25 backdrop-blur">
              <Sun className="size-3.5" />
              Solar forecasting
            </span>

            <h2 className="mt-8 max-w-lg text-[2.75rem] font-bold leading-[1.08] tracking-tight text-white xl:text-5xl">
              Brighter days begin with better forecasts.
            </h2>
            <p className="mt-5 max-w-md text-base leading-7 text-white/85">
              EcoSync turns local weather into a clear picture of what your rooftop will generate,
              so you can plan the wash, the charge and the bill around the sun.
            </p>
          </div>

          <ul className="my-10 flex max-w-md flex-col gap-5">
            {highlights.map(({ icon: Icon, title: t, body }) => (
              <li key={t} className="flex gap-3.5">
                <span className="mt-0.5 flex size-9 shrink-0 items-center justify-center rounded-xl bg-white/15 text-white ring-1 ring-white/20 backdrop-blur">
                  <Icon className="size-[18px]" />
                </span>
                <div>
                  <p className="text-sm font-bold text-white">{t}</p>
                  <p className="mt-0.5 text-sm leading-6 text-white/75">{body}</p>
                </div>
              </li>
            ))}
          </ul>

          <div className="grid max-w-md grid-cols-3 gap-4 border-t border-white/20 pt-7">
            {stats.map((s) => (
              <div key={s.label}>
                <p className="text-2xl font-bold tracking-tight text-white">{s.value}</p>
                <p className="mt-1 text-xs font-medium text-white/70">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </aside>
    </div>
  )
}
