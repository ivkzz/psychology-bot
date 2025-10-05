import type { Metadata } from 'next'
import './globals.css'
import { QueryProvider } from '@/lib/api/query-provider'
import { Toaster } from '@/components/ui/sonner'

export const metadata: Metadata = {
  title: 'Psychology Bot - Психологический помощник',
  description:
    'Ежедневные психологические упражнения для улучшения эмоционального состояния',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="ru">
      <body className="antialiased">
        <QueryProvider>
          {children}
          <Toaster />
        </QueryProvider>
      </body>
    </html>
  )
}
