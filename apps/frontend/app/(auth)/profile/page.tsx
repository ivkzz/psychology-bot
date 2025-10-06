/**
 * Profile Page - страница профиля пользователя
 */

'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useCurrentUser } from '@/lib/hooks/use-auth'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { usersApi } from '@/lib/api/users'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { User, Calendar, Mail, Hash } from 'lucide-react'
import { formatDate } from '@/lib/utils/formatters'
import { toast } from 'sonner'

// Zod схема валидации
const profileSchema = z.object({
  name: z.string().min(1, 'Имя обязательно').max(100, 'Слишком длинное имя'),
  email: z.string().email('Неверный формат email'),
})

type ProfileFormData = z.infer<typeof profileSchema>

export default function ProfilePage() {
  const { data: user, isLoading } = useCurrentUser()
  const queryClient = useQueryClient()

  const updateProfileMutation = useMutation({
    mutationFn: (data: ProfileFormData) => usersApi.updateCurrentUser(data),
    onSuccess: (updatedUser) => {
      // Обновляем кеш пользователя
      queryClient.setQueryData(['users', 'me'], updatedUser)
      toast.success('Профиль успешно обновлён!')
    },
    onError: (error) => {
      const message =
        (error as { response?: { data?: { detail?: string } } }).response?.data
          ?.detail || 'Ошибка при обновлении профиля'
      toast.error(message)
    },
  })

  const {
    register,
    handleSubmit,
    formState: { errors, isDirty },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      name: user?.name || '',
      email: user?.email || '',
    },
    values: {
      name: user?.name || '',
      email: user?.email || '',
    },
  })

  const onSubmit = async (data: ProfileFormData) => {
    await updateProfileMutation.mutateAsync(data)
  }

  if (isLoading) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-10 w-64" />
        <div className="grid gap-6 md:grid-cols-2">
          <Skeleton className="h-96" />
          <Skeleton className="h-96" />
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Заголовок */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          <User className="h-8 w-8" />
          Профиль
        </h1>
        <p className="text-muted-foreground mt-2">
          Управляйте вашим профилем и настройками
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Информация о профиле */}
        <Card>
          <CardHeader>
            <CardTitle>Информация о профиле</CardTitle>
            <CardDescription>
              Основная информация о вашем аккаунте
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-2">
              <User className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Имя:</span>
              <span className="text-sm">{user?.name}</span>
            </div>

            <div className="flex items-center gap-2">
              <Mail className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Email:</span>
              <span className="text-sm">{user?.email || 'Не указан'}</span>
            </div>

            <div className="flex items-center gap-2">
              <Hash className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Telegram ID:</span>
              <span className="text-sm">
                {user?.telegram_id || 'Не привязан'}
              </span>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-sm font-medium">Роль:</span>
              <Badge variant={user?.role === 'ADMIN' ? 'default' : 'secondary'}>
                {user?.role === 'ADMIN' ? 'Администратор' : 'Пользователь'}
              </Badge>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-sm font-medium">Статус:</span>
              <Badge variant={user?.is_active ? 'default' : 'destructive'}>
                {user?.is_active ? 'Активен' : 'Неактивен'}
              </Badge>
            </div>

            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Дата регистрации:</span>
              <span className="text-sm">
                {user?.created_at ? formatDate(user.created_at) : '-'}
              </span>
            </div>
          </CardContent>
        </Card>

        {/* Редактирование профиля */}
        <Card>
          <CardHeader>
            <CardTitle>Редактирование профиля</CardTitle>
            <CardDescription>
              Обновите информацию о вашем профиле
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Имя</Label>
                <Input
                  id="name"
                  type="text"
                  placeholder="Ваше имя"
                  {...register('name')}
                  disabled={updateProfileMutation.isPending}
                />
                {errors.name && (
                  <p className="text-sm text-red-500">{errors.name.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="example@email.com"
                  {...register('email')}
                  disabled={updateProfileMutation.isPending}
                />
                {errors.email && (
                  <p className="text-sm text-red-500">{errors.email.message}</p>
                )}
              </div>

              <Button
                type="submit"
                disabled={!isDirty || updateProfileMutation.isPending}
                className="w-full"
              >
                {updateProfileMutation.isPending
                  ? 'Сохранение...'
                  : 'Сохранить изменения'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>

      {/* Дополнительная информация */}
      <Card>
        <CardHeader>
          <CardTitle>Telegram интеграция</CardTitle>
          <CardDescription>
            Свяжите ваш аккаунт с Telegram для получения уведомлений
          </CardDescription>
        </CardHeader>
        <CardContent>
          {user?.telegram_id ? (
            <div className="flex items-center gap-2">
              <Badge variant="default">Привязан</Badge>
              <span className="text-sm text-muted-foreground">
                Telegram ID: {user.telegram_id}
              </span>
            </div>
          ) : (
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">
                Для привязки Telegram отправьте команду /start боту
                @PsychologyBot
              </p>
              <Badge variant="outline">Не привязан</Badge>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
