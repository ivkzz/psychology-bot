/**
 * Tasks Hooks - хуки для работы с заданиями
 */

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { tasksApi } from '../api/tasks'
import { usersApi } from '../api/users'
import type { AssignmentComplete } from '@/types'
import { toast } from 'sonner'

/**
 * Хук для получения задания на сегодня
 */
export function useTodayTask() {
  return useQuery({
    queryKey: ['tasks', 'today'],
    queryFn: tasksApi.getTodayTask,
    staleTime: 0, // Всегда обновлять при запросе
    retry: 1,
  })
}

/**
 * Хук для выполнения задания
 */
export function useCompleteTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      assignmentId,
      data,
    }: {
      assignmentId: string
      data: AssignmentComplete
    }) => tasksApi.completeTask(assignmentId, data),
    onSuccess: (updatedAssignment) => {
      // Обновляем задание на сегодня
      queryClient.setQueryData(['tasks', 'today'], updatedAssignment)

      // Инвалидируем всю историю заданий
      queryClient.invalidateQueries({
        queryKey: ['tasks', 'history'],
        refetchType: 'all'
      })

      // Инвалидируем статистику пользователя
      queryClient.invalidateQueries({
        queryKey: ['users', 'me', 'progress']
      })

      toast.success(`Задание "${updatedAssignment.task.title}" выполнено!`)
    },
    onError: (error) => {
      const message =
        (error as { response?: { data?: { detail?: string } } }).response?.data
          ?.detail || 'Ошибка при выполнении задания'
      toast.error(message)
    },
  })
}

/**
 * Хук для получения истории заданий
 */
export function useTaskHistory(params?: { limit?: number; offset?: number }) {
  return useQuery({
    queryKey: ['tasks', 'history', params],
    queryFn: () => tasksApi.getTaskHistory(params),
    staleTime: 0, // Всегда обновлять при запросе
  })
}

/**
 * Хук для получения статистики пользователя
 */
export function useUserProgress() {
  return useQuery({
    queryKey: ['users', 'me', 'progress'],
    queryFn: usersApi.getUserProgress,
    staleTime: 0, // Всегда обновлять при запросе
  })
}
