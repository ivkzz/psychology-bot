/**
 * History Page - страница истории заданий
 */

'use client'

import { useState, useMemo } from 'react'
import { useTaskHistory } from '@/lib/hooks/use-tasks'
import { Skeleton } from '@/components/ui/skeleton'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { TaskCard } from '@/components/tasks/TaskCard'
import { History, AlertCircle, ChevronLeft, ChevronRight } from 'lucide-react'
import type { AssignmentStatus } from '@/types'

const ITEMS_PER_PAGE = 10

export default function HistoryPage() {
  const [page, setPage] = useState(0)
  const [statusFilter, setStatusFilter] = useState<
    AssignmentStatus | 'ALL'
  >('ALL')

  const offset = page * ITEMS_PER_PAGE

  const { data: tasks, isLoading } = useTaskHistory({
    limit: 100, // Получаем много заданий для фильтрации на клиенте
    offset: 0,
  })

  // Фильтрация и пагинация на клиенте
  const filteredTasks = useMemo(() => {
    if (!tasks) return []

    const filtered =
      statusFilter === 'ALL'
        ? tasks
        : tasks.filter((task) => task.status === statusFilter)

    // Пагинация
    return filtered.slice(offset, offset + ITEMS_PER_PAGE)
  }, [tasks, statusFilter, offset])

  const totalFiltered = useMemo(() => {
    if (!tasks) return 0
    return statusFilter === 'ALL'
      ? tasks.length
      : tasks.filter((task) => task.status === statusFilter).length
  }, [tasks, statusFilter])

  const totalPages = Math.ceil(totalFiltered / ITEMS_PER_PAGE)

  if (isLoading) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-10 w-64" />
        <div className="flex gap-4">
          <Skeleton className="h-10 w-32" />
        </div>
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
          <History className="h-8 w-8" />
          История заданий
        </h1>
        <p className="text-muted-foreground mt-2">
          Просмотрите все ваши задания и их статус
        </p>
      </div>

      {/* Фильтры */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium">Статус:</span>
          <Select
            value={statusFilter}
            onValueChange={(value) => {
              setStatusFilter(value as AssignmentStatus | 'ALL')
              setPage(0) // Сбрасываем страницу при изменении фильтра
            }}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Все задания" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="ALL">Все задания</SelectItem>
              <SelectItem value="pending">Ожидает</SelectItem>
              <SelectItem value="completed">Выполнено</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="text-sm text-muted-foreground flex items-center">
          Найдено заданий: {totalFiltered}
        </div>
      </div>

      {/* Список заданий */}
      {filteredTasks.length > 0 ? (
        <div className="space-y-4">
          {filteredTasks.map((assignment) => (
            <TaskCard key={assignment.id} assignment={assignment} />
          ))}
        </div>
      ) : (
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Нет заданий</AlertTitle>
          <AlertDescription>
            {statusFilter === 'ALL'
              ? 'У вас пока нет заданий'
              : `Нет заданий со статусом "${statusFilter}"`}
          </AlertDescription>
        </Alert>
      )}

      {/* Пагинация */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={page === 0}
          >
            <ChevronLeft className="h-4 w-4 mr-1" />
            Назад
          </Button>

          <span className="text-sm text-muted-foreground">
            Страница {page + 1} из {totalPages}
          </span>

          <Button
            variant="outline"
            size="sm"
            onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
            disabled={page >= totalPages - 1}
          >
            Вперёд
            <ChevronRight className="h-4 w-4 ml-1" />
          </Button>
        </div>
      )}
    </div>
  )
}
