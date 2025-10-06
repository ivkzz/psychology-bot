/**
 * Tasks Page - страница заданий
 */

'use client'

import { useTodayTask, useTaskHistory } from '@/lib/hooks/use-tasks'
import { Skeleton } from '@/components/ui/skeleton'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { TaskCard } from '@/components/tasks/TaskCard'
import { CheckSquare, AlertCircle } from 'lucide-react'

export default function TasksPage() {
  const { data: todayTask, isLoading: todayLoading, error: todayError } = useTodayTask()
  const { data: recentTasks, isLoading: historyLoading } = useTaskHistory({
    limit: 7,
  })

  if (todayLoading) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64" />
        <Skeleton className="h-10 w-64" />
        <div className="space-y-4">
          <Skeleton className="h-32" />
          <Skeleton className="h-32" />
          <Skeleton className="h-32" />
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Заголовок */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          <CheckSquare className="h-8 w-8" />
          Задания
        </h1>
        <p className="text-muted-foreground mt-2">
          Выполняйте ежедневные задания для улучшения вашего психологического
          состояния
        </p>
      </div>

      {/* Задание на сегодня */}
      <div>
        <h2 className="text-2xl font-semibold mb-4">Задание на сегодня</h2>

        {todayError ? (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Ошибка</AlertTitle>
            <AlertDescription>
              {(todayError as { response?: { data?: { detail?: string } } }).response?.data?.detail ||
                'Не удалось загрузить задание на сегодня'}
            </AlertDescription>
          </Alert>
        ) : todayTask ? (
          <TaskCard assignment={todayTask} showCompleteButton={true} />
        ) : (
          <Alert>
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Нет задания</AlertTitle>
            <AlertDescription>
              На сегодня заданий нет. Возвращайтесь завтра!
            </AlertDescription>
          </Alert>
        )}
      </div>

      {/* Последние задания */}
      <div>
        <h2 className="text-2xl font-semibold mb-4">Последние задания</h2>

        {historyLoading ? (
          <div className="space-y-4">
            <Skeleton className="h-32" />
            <Skeleton className="h-32" />
            <Skeleton className="h-32" />
          </div>
        ) : recentTasks && recentTasks.length > 0 ? (
          <div className="space-y-4">
            {recentTasks.map((assignment) => (
              <TaskCard key={assignment.id} assignment={assignment} />
            ))}
          </div>
        ) : (
          <Alert>
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Нет заданий</AlertTitle>
            <AlertDescription>
              У вас пока нет выполненных заданий
            </AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  )
}
