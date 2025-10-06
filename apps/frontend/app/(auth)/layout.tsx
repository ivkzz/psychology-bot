/**
 * Auth Layout - layout для защищенных страниц
 */

import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1 container mx-auto max-w-7xl py-8 px-4">
        {children}
      </main>
      <Footer />
    </div>
  )
}
