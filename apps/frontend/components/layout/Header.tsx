/**
 * Header - серверный компонент шапки сайта
 */

import Link from 'next/link'
import { Brain } from 'lucide-react'
import { Navigation } from './Navigation'
import { UserMenu } from './UserMenu'

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 shadow-sm">
      <div className="container mx-auto max-w-7xl flex h-16 items-center justify-between px-4">
        {/* Логотип */}
        <Link href="/dashboard" className="flex items-center gap-2">
          <Brain className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold">Psychology Bot</span>
        </Link>

        {/* Навигация (клиентский компонент) */}
        <Navigation />

        {/* Меню пользователя (клиентский компонент) */}
        <UserMenu />
      </div>
    </header>
  )
}
