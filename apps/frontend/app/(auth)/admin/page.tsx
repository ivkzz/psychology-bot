/**
 * Admin Dashboard Page - главная страница админ-панели
 */

'use client'

import Link from 'next/link'
import { useAdminUsers, useTaskTemplates } from '@/lib/hooks/use-admin'
import { useTaskHistory } from '@/lib/hooks/use-tasks'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { Badge } from '@/components/ui/badge'
import {
  Users,
  FileText,
  CheckSquare,
  TrendingUp,
  ArrowRight,
  UserPlus,
  FilePlus,
} from 'lucide-react'
import { formatDate } from '@/lib/utils/formatters'
import { useMemo } from 'react'

export default function AdminDashboardPage() {
  const { data: users, isLoading: usersLoading } = useAdminUsers({
    limit: 100,
  })
  const { data: templates, isLoading: templatesLoading } = useTaskTemplates({
    limit: 100,
  })
  const { data: allAssignments, isLoading: assignmentsLoading } =
    useTaskHistory({ limit: 100 })

  // Статистика
  const stats = useMemo(() => {
    const totalUsers = users?.length || 0
    const activeUsers =
      users?.filter((u) => u.is_active).length || 0
    const totalTemplates = templates?.length || 0
    const completedTasks =
      allAssignments?.filter((a) => a.status === 'completed').length || 0

    return {
      totalUsers,
      activeUsers,
      totalTemplates,
      completedTasks,
    }
  }, [users, templates, allAssignments])

  // Последние зарегистрированные пользователи
  const recentUsers = useMemo(() => {
    if (!users) return []
    return [...users]
      .sort(
        (a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      )
      .slice(0, 5)
  }, [users])

  // Популярные категории
  const popularCategories = useMemo(() => {
    if (!allAssignments) return []

    const categoryCount = allAssignments.reduce(
      (acc, assignment) => {
        const category = assignment.task.category
        acc[category] = (acc[category] || 0) + 1
        return acc
      },
      {} as Record<string, number>
    )

    return Object.entries(categoryCount)
      .map(([category, count]) => ({ category, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5)
  }, [allAssignments])

  const isLoading = usersLoading || templatesLoading || assignmentsLoading

  if (isLoading) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-10 w-96" />
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <Skeleton className="h-32" />
          <Skeleton className="h-32" />
          <Skeleton className="h-32" />
          <Skeleton className="h-32" />
        </div>
        <Skeleton className="h-64" />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Заголовок */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Админ-панель</h1>
          <p className="text-muted-foreground mt-2">
            Управление пользователями и заданиями
          </p>
        </div>
      </div>

      {/* Статистика */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {/* Всего пользователей */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Всего пользователей
            </CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalUsers}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Активных: {stats.activeUsers}
            </p>
          </CardContent>
        </Card>

        {/* Шаблонов заданий */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Шаблонов заданий
            </CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalTemplates}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Доступно для назначения
            </p>
          </CardContent>
        </Card>

        {/* Выполнено заданий */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Выполнено заданий
            </CardTitle>
            <CheckSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.completedTasks}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Всеми пользователями
            </p>
          </CardContent>
        </Card>

        {/* Средний процент выполнения */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Активность</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {stats.activeUsers > 0
                ? Math.round((stats.activeUsers / stats.totalUsers) * 100)
                : 0}
              %
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Активных пользователей
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Последние регистрации */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Последние регистрации</CardTitle>
                <CardDescription>
                  Недавно зарегистрированные пользователи
                </CardDescription>
              </div>
              <Link href="/admin/users">
                <Button variant="ghost" size="sm">
                  Все
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {recentUsers.length > 0 ? (
              <div className="space-y-4">
                {recentUsers.map((user) => (
                  <div
                    key={user.id}
                    className="flex items-center justify-between border-b pb-3 last:border-0 last:pb-0"
                  >
                    <div className="flex-1">
                      <p className="font-medium">{user.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {user.email || 'Без email'}
                      </p>
                    </div>
                    <div className="text-right">
                      <Badge variant={user.role === 'admin' ? 'default' : 'secondary'}>
                        {user.role === 'admin' ? 'Админ' : 'Пользователь'}
                      </Badge>
                      <p className="text-xs text-muted-foreground mt-1">
                        {formatDate(user.created_at)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-center text-muted-foreground py-8">
                Нет пользователей
              </p>
            )}
          </CardContent>
        </Card>

        {/* Популярные категории */}
        <Card>
          <CardHeader>
            <CardTitle>Популярные категории</CardTitle>
            <CardDescription>
              Наиболее часто назначаемые категории заданий
            </CardDescription>
          </CardHeader>
          <CardContent>
            {popularCategories.length > 0 ? (
              <div className="space-y-4">
                {popularCategories.map((item) => (
                  <div
                    key={item.category}
                    className="flex items-center justify-between"
                  >
                    <Badge variant="outline">{item.category}</Badge>
                    <span className="text-sm font-medium">{item.count} заданий</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-center text-muted-foreground py-8">
                Нет данных
              </p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Быстрые действия */}
      <Card>
        <CardHeader>
          <CardTitle>Быстрые действия</CardTitle>
          <CardDescription>Часто используемые функции</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <Link href="/admin/users">
              <Button>
                <Users className="mr-2 h-4 w-4" />
                Управление пользователями
              </Button>
            </Link>
            <Link href="/admin/tasks">
              <Button>
                <FileText className="mr-2 h-4 w-4" />
                Управление шаблонами
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
