/**
 * Admin Hooks - хуки для админ-панели с TanStack Query
 */

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { adminApi } from '../api/admin'
import { toast } from 'sonner'
import type { TaskCreate, TaskUpdate, TaskDifficulty } from '@/types'

// ============ Пользователи ============

export interface UseAdminUsersParams {
  skip?: number
  limit?: number
  is_active?: boolean
}

/**
 * Хук для получения списка всех пользователей
 */
export function useAdminUsers(params?: UseAdminUsersParams) {
  return useQuery({
    queryKey: ['admin', 'users', params],
    queryFn: () => adminApi.getUsers(params),
    staleTime: 1 * 60 * 1000, // 1 минута
  })
}

/**
 * Хук для получения данных пользователя по ID
 */
export function useAdminUserDetails(userId: string) {
  return useQuery({
    queryKey: ['admin', 'users', userId],
    queryFn: () => adminApi.getUserById(userId),
    staleTime: 1 * 60 * 1000,
  })
}

/**
 * Хук для получения статистики прогресса пользователя по ID
 */
export function useAdminUserProgress(userId: string) {
  return useQuery({
    queryKey: ['admin', 'users', userId, 'progress'],
    queryFn: () => adminApi.getUserProgress(userId),
    staleTime: 1 * 60 * 1000,
  })
}

/**
 * Хук для получения списка заданий пользователя по ID
 */
export function useAdminUserAssignments(
  userId: string,
  params?: {
    skip?: number
    limit?: number
    status?: import('@/types').AssignmentStatus
  }
) {
  return useQuery({
    queryKey: ['admin', 'users', userId, 'assignments', params],
    queryFn: () => adminApi.getUserAssignments(userId, params),
    staleTime: 1 * 60 * 1000,
  })
}

// ============ Шаблоны заданий ============

export interface UseTaskTemplatesParams {
  skip?: number
  limit?: number
  category?: string
  difficulty?: TaskDifficulty
}

/**
 * Хук для получения списка шаблонов заданий
 */
export function useTaskTemplates(params?: UseTaskTemplatesParams) {
  return useQuery({
    queryKey: ['admin', 'tasks', 'templates', params],
    queryFn: () => adminApi.getTaskTemplates(params),
    staleTime: 2 * 60 * 1000, // 2 минуты
  })
}

/**
 * Хук для создания нового шаблона задания
 */
export function useCreateTemplate() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: TaskCreate) => adminApi.createTaskTemplate(data),
    onSuccess: (newTemplate) => {
      // Инвалидируем кеш шаблонов
      queryClient.invalidateQueries({
        queryKey: ['admin', 'tasks', 'templates'],
      })

      toast.success(`Шаблон "${newTemplate.title}" создан!`)
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Ошибка создания шаблона')
    },
  })
}

/**
 * Хук для обновления шаблона задания
 */
export function useUpdateTemplate() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      taskId,
      data,
    }: {
      taskId: string
      data: TaskUpdate
    }) => adminApi.updateTaskTemplate(taskId, data),
    onSuccess: (updatedTemplate) => {
      // Инвалидируем кеш шаблонов
      queryClient.invalidateQueries({
        queryKey: ['admin', 'tasks', 'templates'],
      })

      toast.success(`Шаблон "${updatedTemplate.title}" обновлён!`)
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Ошибка обновления шаблона')
    },
  })
}

/**
 * Хук для удаления шаблона задания
 */
export function useDeleteTemplate() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (taskId: string) => adminApi.deleteTaskTemplate(taskId),
    onSuccess: () => {
      // Инвалидируем кеш шаблонов
      queryClient.invalidateQueries({
        queryKey: ['admin', 'tasks', 'templates'],
      })

      toast.success('Шаблон удалён')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Ошибка удаления шаблона')
    },
  })
}

// ============ Назначение заданий ============

/**
 * Хук для назначения задания пользователю
 */
export function useAssignTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      userId,
      taskId,
    }: {
      userId: string
      taskId: string
    }) => adminApi.assignTaskToUser(userId, taskId),
    onSuccess: (assignment, variables) => {
      // Инвалидируем кеш заданий конкретного пользователя
      queryClient.invalidateQueries({
        queryKey: ['admin', 'users', variables.userId, 'assignments'],
      })
      // Инвалидируем прогресс пользователя
      queryClient.invalidateQueries({
        queryKey: ['admin', 'users', variables.userId, 'progress'],
      })
      // Инвалидируем общую историю (на случай если открыта страница истории)
      queryClient.invalidateQueries({
        queryKey: ['tasks', 'history'],
      })

      toast.success(`Задание "${assignment.task.title}" назначено!`)
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Ошибка назначения задания')
    },
  })
}
