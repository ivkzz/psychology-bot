/**
 * Dashboard Page - главная страница пользовательского кабинета
 */

'use client'

import Link from 'next/link'
import { useCurrentUser } from '@/lib/hooks/use-auth'
import { useTodayTask, useUserProgress } from '@/lib/hooks/use-tasks'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { Badge } from '@/components/ui/badge'
import {
  CheckSquare,
  Clock,
  TrendingUp,
  Flame,
  ArrowRight,
} from 'lucide-react'
import { formatDate, formatDifficulty, getDifficultyColor } from '@/lib/utils/formatters'

export default function DashboardPage() {
  const { data: user, isLoading: userLoading } = useCurrentUser()
  const { data: todayTask, isLoading: taskLoading } = useTodayTask()
  const { data: progress, isLoading: progressLoading } = useUserProgress()

  if (userLoading) {
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
      {/* Приветствие */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          Добро пожаловать, {user?.name}!
        </h1>
        <p className="text-muted-foreground mt-2">
          Вот краткая информация о вашем прогрессе
        </p>
      </div>

      {/* Статистика в карточках */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {/* Всего заданий */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Всего заданий
            </CardTitle>
            <CheckSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {progressLoading ? (
              <Skeleton className="h-8 w-16" />
            ) : (
              <div className="text-2xl font-bold">{progress?.total_tasks || 0}</div>
            )}
          </CardContent>
        </Card>

        {/* Выполнено */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Выполнено</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {progressLoading ? (
              <Skeleton className="h-8 w-16" />
            ) : (
              <div className="text-2xl font-bold">
                {progress?.completed_tasks || 0}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Процент выполнения */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Процент выполнения
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {progressLoading ? (
              <Skeleton className="h-8 w-16" />
            ) : (
              <div className="text-2xl font-bold">
                {progress?.completion_rate?.toFixed(0) || 0}%
              </div>
            )}
          </CardContent>
        </Card>

        {/* Серия дней */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Серия дней</CardTitle>
            <Flame className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            {progressLoading ? (
              <Skeleton className="h-8 w-16" />
            ) : (
              <div className="text-2xl font-bold flex items-center gap-2">
                {progress?.streak_days || 0}
                {(progress?.streak_days || 0) > 0 && (
                  <Flame className="h-5 w-5 text-orange-500" />
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Задание на сегодня */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Задание на сегодня</CardTitle>
              <CardDescription>
                Выполните задание, чтобы продолжить серию
              </CardDescription>
            </div>
            <Clock className="h-5 w-5 text-muted-foreground" />
          </div>
        </CardHeader>
        <CardContent>
          {taskLoading ? (
            <div className="space-y-4">
              <Skeleton className="h-6 w-3/4" />
              <Skeleton className="h-20 w-full" />
              <Skeleton className="h-10 w-32" />
            </div>
          ) : todayTask ? (
            <div className="space-y-4">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2">
                    {todayTask.task.title}
                  </h3>
                  <p className="text-muted-foreground mb-4">
                    {todayTask.task.description}
                  </p>
                  <div className="flex items-center gap-2">
                    <Badge variant="outline">{todayTask.task.category}</Badge>
                    <Badge variant={getDifficultyColor(todayTask.task.difficulty)}>
                      {formatDifficulty(todayTask.task.difficulty)}
                    </Badge>
                    <span className="text-sm text-muted-foreground">
                      Назначено: {formatDate(todayTask.assigned_date)}
                    </span>
                  </div>
                </div>
              </div>

              {todayTask.status === 'completed' ? (
                <div className="flex items-center gap-2 text-green-600">
                  <CheckSquare className="h-5 w-5" />
                  <span className="font-medium">Выполнено!</span>
                  {todayTask.completed_at && (
                    <span className="text-sm text-muted-foreground">
                      {formatDate(todayTask.completed_at)}
                    </span>
                  )}
                </div>
              ) : (
                <Link href="/tasks">
                  <Button>
                    Выполнить задание
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              )}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-muted-foreground">
                На сегодня заданий нет. Возвращайтесь завтра!
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Быстрые ссылки */}
      <div className="grid gap-6 md:grid-cols-3">
        <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
          <Link href="/tasks">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckSquare className="h-5 w-5" />
                Задания
              </CardTitle>
              <CardDescription>Посмотреть все задания</CardDescription>
            </CardHeader>
          </Link>
        </Card>

        <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
          <Link href="/history">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                История
              </CardTitle>
              <CardDescription>История выполненных заданий</CardDescription>
            </CardHeader>
          </Link>
        </Card>

        <Card className="hover:bg-accent/50 transition-colors cursor-pointer">
          <Link href="/stats">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Статистика
              </CardTitle>
              <CardDescription>Подробная статистика прогресса</CardDescription>
            </CardHeader>
          </Link>
        </Card>
      </div>
    </div>
  )
}
