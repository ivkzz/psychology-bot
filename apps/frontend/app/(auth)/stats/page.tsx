/**
 * Stats Page - страница статистики
 */

'use client'

import { useMemo } from 'react'
import { useUserProgress, useTaskHistory } from '@/lib/hooks/use-tasks'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Skeleton } from '@/components/ui/skeleton'
import { Badge } from '@/components/ui/badge'
import {
  BarChart3,
  CheckSquare,
  TrendingUp,
  Flame,
  Calendar,
} from 'lucide-react'

export default function StatsPage() {
  const { data: progress, isLoading: progressLoading } = useUserProgress()
  const { data: allTasks, isLoading: tasksLoading } = useTaskHistory({
    limit: 100,
  })

  // Группировка по категориям
  const categoryStats = useMemo(() => {
    if (!allTasks) return []

    const categories = allTasks.reduce(
      (acc, task) => {
        const category = task.task.category
        if (!acc[category]) {
          acc[category] = { total: 0, completed: 0 }
        }
        acc[category].total++
        if (task.status === 'completed') {
          acc[category].completed++
        }
        return acc
      },
      {} as Record<string, { total: number; completed: number }>
    )

    return Object.entries(categories)
      .map(([category, stats]) => ({
        category,
        total: stats.total,
        completed: stats.completed,
        completionRate: (stats.completed / stats.total) * 100,
      }))
      .sort((a, b) => b.total - a.total)
  }, [allTasks])

  if (progressLoading || tasksLoading) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-10 w-64" />
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
      <div>
        <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          <BarChart3 className="h-8 w-8" />
          Статистика
        </h1>
        <p className="text-muted-foreground mt-2">
          Отслеживайте свой прогресс и достижения
        </p>
      </div>

      {/* Основные показатели */}
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
            <div className="text-2xl font-bold">{progress?.total_tasks || 0}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Назначено вам
            </p>
          </CardContent>
        </Card>

        {/* Выполнено */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Выполнено</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {progress?.completed_tasks || 0}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Успешно завершено
            </p>
          </CardContent>
        </Card>

        {/* Процент выполнения */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Успешность
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {progress?.completion_rate?.toFixed(0) || 0}%
            </div>
            <Progress
              value={progress?.completion_rate || 0}
              className="mt-2"
            />
          </CardContent>
        </Card>

        {/* Серия дней */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Серия дней</CardTitle>
            <Flame className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold flex items-center gap-2">
              {progress?.streak_days || 0}
              {(progress?.streak_days || 0) > 0 && (
                <Flame className="h-5 w-5 text-orange-500" />
              )}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Дней подряд
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Статистика по категориям */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Calendar className="h-5 w-5" />
            <CardTitle>Статистика по категориям</CardTitle>
          </div>
          <CardDescription>
            Распределение заданий по категориям и их выполнение
          </CardDescription>
        </CardHeader>
        <CardContent>
          {categoryStats.length > 0 ? (
            <div className="space-y-4">
              {categoryStats.map((stat) => (
                <div
                  key={stat.category}
                  className="flex items-center justify-between gap-4"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge variant="outline">{stat.category}</Badge>
                      <span className="text-sm text-muted-foreground">
                        {stat.completed} / {stat.total}
                      </span>
                    </div>
                    <Progress value={stat.completionRate} className="h-2" />
                  </div>
                  <div className="text-sm font-medium">
                    {stat.completionRate.toFixed(0)}%
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-muted-foreground py-8">
              Нет данных для отображения
            </p>
          )}
        </CardContent>
      </Card>

      {/* Достижения */}
      <Card>
        <CardHeader>
          <CardTitle>Ваши достижения</CardTitle>
          <CardDescription>
            Отслеживайте свои успехи и мотивируйте себя
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            {/* Первое задание */}
            {(progress?.total_tasks || 0) >= 1 && (
              <div className="flex items-start gap-3 p-4 border rounded-lg">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                  <CheckSquare className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="font-medium">Первые шаги</p>
                  <p className="text-sm text-muted-foreground">
                    Получено первое задание
                  </p>
                </div>
              </div>
            )}

            {/* Первое выполненное */}
            {(progress?.completed_tasks || 0) >= 1 && (
              <div className="flex items-start gap-3 p-4 border rounded-lg">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-100">
                  <CheckSquare className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="font-medium">Начало пути</p>
                  <p className="text-sm text-muted-foreground">
                    Выполнено первое задание
                  </p>
                </div>
              </div>
            )}

            {/* 5 заданий */}
            {(progress?.completed_tasks || 0) >= 5 && (
              <div className="flex items-start gap-3 p-4 border rounded-lg">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100">
                  <TrendingUp className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="font-medium">Целеустремлённость</p>
                  <p className="text-sm text-muted-foreground">
                    Выполнено 5 заданий
                  </p>
                </div>
              </div>
            )}

            {/* Серия 3 дня */}
            {(progress?.streak_days || 0) >= 3 && (
              <div className="flex items-start gap-3 p-4 border rounded-lg">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-orange-100">
                  <Flame className="h-5 w-5 text-orange-500" />
                </div>
                <div>
                  <p className="font-medium">Постоянство</p>
                  <p className="text-sm text-muted-foreground">
                    Серия 3 дня подряд
                  </p>
                </div>
              </div>
            )}
          </div>

          {(progress?.total_tasks || 0) === 0 && (
            <p className="text-center text-muted-foreground py-8">
              Начните выполнять задания, чтобы получать достижения!
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
