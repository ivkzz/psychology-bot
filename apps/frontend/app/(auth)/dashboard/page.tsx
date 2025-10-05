/**
 * Dashboard Page - главная страница после входа
 */

'use client'

import { useCurrentUser, useLogout } from '@/lib/hooks/use-auth'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'

export default function DashboardPage() {
  const { data: user, isLoading } = useCurrentUser()
  const logoutMutation = useLogout()

  if (isLoading) {
    return (
      <div className="container mx-auto p-8">
        <Skeleton className="h-8 w-64 mb-4" />
        <Skeleton className="h-32 w-full" />
      </div>
    )
  }

  return (
    <div className="container mx-auto p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">
          Добро пожаловать, {user?.name}!
        </h1>
        <Button
          variant="outline"
          onClick={() => logoutMutation.mutate()}
          disabled={logoutMutation.isPending}
        >
          Выйти
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Профиль</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">Email: {user?.email}</p>
            <p className="text-sm text-gray-600">Роль: {user?.role}</p>
            <p className="text-sm text-gray-600">
              Telegram ID: {user?.telegram_id || 'Не привязан'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Задания</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">
              Здесь будут отображаться ваши задания
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Статистика</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600">
              Здесь будет отображаться ваш прогресс
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4">Sprint 1 завершен! ✅</h2>
        <p className="text-gray-600">
          Инфраструктура настроена:
        </p>
        <ul className="list-disc list-inside text-gray-600 mt-2 space-y-1">
          <li>✅ TypeScript типы</li>
          <li>✅ Axios client с interceptors</li>
          <li>✅ TanStack Query Provider</li>
          <li>✅ Zustand Auth Store</li>
          <li>✅ API методы (auth, users, tasks, admin)</li>
          <li>✅ Auth Hooks</li>
          <li>✅ Login/Register страницы</li>
          <li>✅ Middleware для защиты роутов</li>
        </ul>
      </div>
    </div>
  )
}
