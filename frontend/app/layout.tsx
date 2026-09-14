import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'AutoBook Publisher Agent Dashboard',
  description: 'Automated AI Publishing Suite & Direct Sales Bundle Generator',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body class="min-h-screen flex flex-col bg-[#FAF8F5] text-stone-900">
        <header class="border-b border-stone-200 bg-white/80 backdrop-blur px-8 py-4 flex justify-between items-center shadow-sm">
          <div class="flex items-center space-x-3">
            <span class="text-amber-700 text-2xl font-serif">❖</span>
            <span class="text-xl font-bold tracking-tight text-stone-900 font-serif">AUTOBOOK PUBLISHER</span>
          </div>
          <div class="text-xs font-sans uppercase tracking-widest text-stone-500 bg-amber-50 px-3 py-1 rounded-full border border-amber-200">
            Plough Aesthetic Engine v1.0
          </div>
        </header>

        <main class="flex-1 max-w-6xl w-full mx-auto px-6 py-10">
          {children}
        </main>

        <footer class="border-t border-stone-200 py-6 text-center text-xs text-stone-500 font-sans">
          © 2025 AutoBook Publisher Suite. All rights reserved.
        </footer>
      </body>
    </html>
  )
}
