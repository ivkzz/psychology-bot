/**
 * UserMenu - клиентский компонент меню пользователя
 */

'use client'

import Link from 'next/link'
import { useCurrentUser, useLogout } from '@/lib/hooks/use-auth'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Badge } from '@/components/ui/badge'
import { User, LogOut } from 'lucide-react'

export function UserMenu() {
  const { data: user } = useCurrentUser()
  const logoutMutation = useLogout()

  const handleLogout = () => {
    logoutMutation.mutate()
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="sm" className="gap-2">
          <User className="h-4 w-4" />
          <span className="hidden md:inline">{user?.name || 'Пользователь'}</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel>
          <div className="flex flex-col gap-1">
            <p className="text-sm font-medium">{user?.name}</p>
            <p className="text-xs text-muted-foreground">{user?.email}</p>
            {user?.role === 'admin' && (
              <Badge variant="secondary" className="w-fit">
                Администратор
              </Badge>
            )}
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem asChild>
          <Link href="/profile" className="cursor-pointer">
            <User className="mr-2 h-4 w-4" />
            Профиль
          </Link>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          onClick={handleLogout}
          disabled={logoutMutation.isPending}
          className="cursor-pointer text-red-600"
        >
          <LogOut className="mr-2 h-4 w-4" />
          Выйти
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
