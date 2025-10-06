/**
 * Navigation - клиентский компонент навигации
 */

'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useCurrentUser } from '@/lib/hooks/use-auth'
import { LayoutDashboard, CheckSquare, History, BarChart3, Shield } from 'lucide-react'
import { cn } from '@/lib/utils'

export function Navigation() {
  const pathname = usePathname()
  const { data: user } = useCurrentUser()

  const navItems = [
    { href: '/dashboard', label: 'Главная', icon: LayoutDashboard },
    { href: '/tasks', label: 'Задания', icon: CheckSquare },
    { href: '/history', label: 'История', icon: History },
    { href: '/stats', label: 'Статистика', icon: BarChart3 },
  ]

  return (
    <nav className="hidden md:flex items-center gap-6">
      {navItems.map((item) => {
        const Icon = item.icon
        return (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              'flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary',
              pathname === item.href
                ? 'text-primary'
                : 'text-muted-foreground'
            )}
          >
            <Icon className="h-4 w-4" />
            {item.label}
          </Link>
        )
      })}

      {/* Админ-панель (только для админов) */}
      {user?.role === 'admin' && (
        <Link
          href="/admin"
          className={cn(
            'flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary',
            pathname.startsWith('/admin')
              ? 'text-primary'
              : 'text-muted-foreground'
          )}
        >
          <Shield className="h-4 w-4" />
          Админ-панель
        </Link>
      )}
    </nav>
  )
}
