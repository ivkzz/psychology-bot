/**
 * Admin Users Page - список всех пользователей
 */

'use client'

import { useState, useMemo } from 'react'
import Link from 'next/link'
import { useAdminUsers } from '@/lib/hooks/use-admin'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Users, Search, Eye, CheckCircle, XCircle } from 'lucide-react'
import { formatDate } from '@/lib/utils/formatters'

export default function AdminUsersPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [isActiveFilter, setIsActiveFilter] = useState<string>('all')

  const { data: users, isLoading } = useAdminUsers({ limit: 100 })

  // Фильтрация пользователей
  const filteredUsers = useMemo(() => {
    if (!users) return []

    let filtered = users

    // Фильтр по активности
    if (isActiveFilter === 'active') {
      filtered = filtered.filter((u) => u.is_active)
    } else if (isActiveFilter === 'inactive') {
      filtered = filtered.filter((u) => !u.is_active)
    }

    // Поиск по имени или email
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(
        (u) =>
          u.name.toLowerCase().includes(query) ||
          u.email?.toLowerCase().includes(query) ||
          u.id.toLowerCase().includes(query)
      )
    }

    return filtered
  }, [users, searchQuery, isActiveFilter])

  if (isLoading) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-10 w-96" />
        <Skeleton className="h-64" />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Заголовок */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          <Users className="h-8 w-8" />
          Управление пользователями
        </h1>
        <p className="text-muted-foreground mt-2">
          Просмотр и управление всеми пользователями системы
        </p>
      </div>

      {/* Фильтры и поиск */}
      <Card>
        <CardHeader>
          <CardTitle>Фильтры</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            {/* Поиск */}
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Поиск по имени, email или ID..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            {/* Фильтр по активности */}
            <div className="w-full sm:w-[200px]">
              <Select
                value={isActiveFilter}
                onValueChange={setIsActiveFilter}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Все пользователи" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Все пользователи</SelectItem>
                  <SelectItem value="active">Активные</SelectItem>
                  <SelectItem value="inactive">Неактивные</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Счетчик */}
            <div className="flex items-center text-sm text-muted-foreground">
              Найдено: {filteredUsers.length}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Таблица пользователей */}
      <Card>
        <CardHeader>
          <CardTitle>Пользователи</CardTitle>
          <CardDescription>
            {filteredUsers.length} пользователей из {users?.length || 0}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {filteredUsers.length > 0 ? (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Имя</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Telegram ID</TableHead>
                    <TableHead>Роль</TableHead>
                    <TableHead>Статус</TableHead>
                    <TableHead>Дата регистрации</TableHead>
                    <TableHead className="text-right">Действия</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredUsers.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell className="font-medium">{user.name}</TableCell>
                      <TableCell>
                        {user.email || (
                          <span className="text-muted-foreground">—</span>
                        )}
                      </TableCell>
                      <TableCell>
                        {user.telegram_id || (
                          <span className="text-muted-foreground">—</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            user.role === 'admin' ? 'default' : 'secondary'
                          }
                        >
                          {user.role === 'admin' ? 'Админ' : 'Пользователь'}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        {user.is_active ? (
                          <div className="flex items-center gap-1 text-green-600">
                            <CheckCircle className="h-4 w-4" />
                            <span className="text-sm">Активен</span>
                          </div>
                        ) : (
                          <div className="flex items-center gap-1 text-gray-400">
                            <XCircle className="h-4 w-4" />
                            <span className="text-sm">Неактивен</span>
                          </div>
                        )}
                      </TableCell>
                      <TableCell>{formatDate(user.created_at)}</TableCell>
                      <TableCell className="text-right">
                        <Link href={`/admin/users/${user.id}`}>
                          <Button variant="ghost" size="sm">
                            <Eye className="h-4 w-4 mr-1" />
                            Просмотр
                          </Button>
                        </Link>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          ) : (
            <div className="text-center py-8 text-muted-foreground">
              {searchQuery || isActiveFilter !== 'all'
                ? 'Пользователи не найдены'
                : 'Нет пользователей'}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
