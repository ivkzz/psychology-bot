/**
 * Admin User Details Page - детальная информация о пользователе
 */

'use client'

import { useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import {
  useAdminUserDetails,
  useAdminUserProgress,
  useAdminUserAssignments,
  useAssignTask,
  useTaskTemplates,
} from '@/lib/hooks/use-admin'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { TaskCard } from '@/components/tasks/TaskCard'
import {
  User,
  ArrowLeft,
  CheckSquare,
  TrendingUp,
  Flame,
  Calendar,
  Mail,
  MessageSquare,
  Shield,
  CheckCircle,
  XCircle,
  Plus,
} from 'lucide-react'
import { formatDate, formatDifficulty } from '@/lib/utils/formatters'

export default function AdminUserDetailsPage() {
  const params = useParams()
  const userId = params.id as string

  const [selectedTaskId, setSelectedTaskId] = useState<string>('')

  const { data: user, isLoading: userLoading } = useAdminUserDetails(userId)
  const { data: progress, isLoading: progressLoading } = useAdminUserProgress(userId)
  const { data: history, isLoading: historyLoading } = useAdminUserAssignments(userId, {
    limit: 100,
  })
  const { data: templates } = useTaskTemplates({ limit: 100 })

  const assignTask = useAssignTask()

  const handleAssignTask = () => {
    if (!selectedTaskId) return

    assignTask.mutate(
      { userId, taskId: selectedTaskId },
      {
        onSuccess: () => {
          setSelectedTaskId('')
        },
      }
    )
  }

  if (userLoading) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-10 w-96" />
        <Skeleton className="h-64" />
      </div>
    )
  }

  if (!user) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">Пользователь не найден</p>
        <Link href="/admin/users">
          <Button className="mt-4">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Назад к списку
          </Button>
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Заголовок */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/admin/users">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="h-4 w-4" />
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
              <User className="h-8 w-8" />
              {user.name}
            </h1>
            <p className="text-muted-foreground mt-2">
              Детальная информация о пользователе
            </p>
          </div>
        </div>
      </div>

      {/* Информация о пользователе */}
      <Card>
        <CardHeader>
          <CardTitle>Информация о пользователе</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            {/* ID */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-muted-foreground">ID</p>
              <p className="font-mono text-sm">{user.id}</p>
            </div>

            {/* Имя */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-muted-foreground">Имя</p>
              <p className="text-sm">{user.name}</p>
            </div>

            {/* Email */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                <Mail className="h-4 w-4" />
                Email
              </p>
              <p className="text-sm">
                {user.email || (
                  <span className="text-muted-foreground">Не указан</span>
                )}
              </p>
            </div>

            {/* Telegram ID */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                <MessageSquare className="h-4 w-4" />
                Telegram ID
              </p>
              <p className="text-sm">
                {user.telegram_id || (
                  <span className="text-muted-foreground">Не указан</span>
                )}
              </p>
            </div>

            {/* Роль */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                <Shield className="h-4 w-4" />
                Роль
              </p>
              <Badge variant={user.role === 'admin' ? 'default' : 'secondary'}>
                {user.role === 'admin' ? 'Администратор' : 'Пользователь'}
              </Badge>
            </div>

            {/* Статус */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-muted-foreground">Статус</p>
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
            </div>

            {/* Дата регистрации */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                Дата регистрации
              </p>
              <p className="text-sm">{formatDate(user.created_at)}</p>
            </div>

            {/* Последнее обновление */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-muted-foreground">
                Последнее обновление
              </p>
              <p className="text-sm">{formatDate(user.updated_at)}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Статистика пользователя */}
      <Card>
        <CardHeader>
          <CardTitle>Статистика</CardTitle>
        </CardHeader>
        <CardContent>
          {progressLoading ? (
            <div className="grid gap-6 md:grid-cols-4">
              <Skeleton className="h-20" />
              <Skeleton className="h-20" />
              <Skeleton className="h-20" />
              <Skeleton className="h-20" />
            </div>
          ) : (
            <div className="grid gap-6 md:grid-cols-4">
              {/* Всего заданий */}
              <div className="flex flex-col items-center justify-center p-4 border rounded-lg">
                <CheckSquare className="h-8 w-8 text-muted-foreground mb-2" />
                <p className="text-2xl font-bold">{progress?.total_tasks || 0}</p>
                <p className="text-xs text-muted-foreground">Всего заданий</p>
              </div>

              {/* Выполнено */}
              <div className="flex flex-col items-center justify-center p-4 border rounded-lg">
                <TrendingUp className="h-8 w-8 text-green-600 mb-2" />
                <p className="text-2xl font-bold">{progress?.completed_tasks || 0}</p>
                <p className="text-xs text-muted-foreground">Выполнено</p>
              </div>

              {/* Процент */}
              <div className="flex flex-col items-center justify-center p-4 border rounded-lg">
                <TrendingUp className="h-8 w-8 text-blue-600 mb-2" />
                <p className="text-2xl font-bold">
                  {progress?.completion_rate?.toFixed(0) || 0}%
                </p>
                <p className="text-xs text-muted-foreground">Успешность</p>
              </div>

              {/* Серия */}
              <div className="flex flex-col items-center justify-center p-4 border rounded-lg">
                <Flame className="h-8 w-8 text-orange-500 mb-2" />
                <p className="text-2xl font-bold flex items-center gap-1">
                  {progress?.streak_days || 0}
                  {(progress?.streak_days || 0) > 0 && (
                    <Flame className="h-5 w-5 text-orange-500" />
                  )}
                </p>
                <p className="text-xs text-muted-foreground">Серия дней</p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Назначить задание */}
      <Card>
        <CardHeader>
          <CardTitle>Назначить задание вручную</CardTitle>
          <CardDescription>
            Выберите шаблон задания для назначения пользователю
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <div className="flex-1">
              <Select value={selectedTaskId} onValueChange={setSelectedTaskId}>
                <SelectTrigger>
                  <SelectValue placeholder="Выберите шаблон задания..." />
                </SelectTrigger>
                <SelectContent>
                  {templates?.map((template) => (
                    <SelectItem key={template.id} value={template.id}>
                      {template.title} ({template.category} - {formatDifficulty(template.difficulty)})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <Button
              onClick={handleAssignTask}
              disabled={!selectedTaskId || assignTask.isPending}
            >
              <Plus className="mr-2 h-4 w-4" />
              {assignTask.isPending ? 'Назначение...' : 'Назначить'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* История заданий */}
      <Card>
        <CardHeader>
          <CardTitle>История заданий</CardTitle>
          <CardDescription>
            Последние назначенные задания пользователя
          </CardDescription>
        </CardHeader>
        <CardContent>
          {historyLoading ? (
            <div className="space-y-4">
              <Skeleton className="h-32" />
              <Skeleton className="h-32" />
            </div>
          ) : history && history.length > 0 ? (
            <div className="space-y-4">
              {history.slice(0, 10).map((assignment) => (
                <TaskCard key={assignment.id} assignment={assignment} />
              ))}
            </div>
          ) : (
            <p className="text-center text-muted-foreground py-8">
              Нет назначенных заданий
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
