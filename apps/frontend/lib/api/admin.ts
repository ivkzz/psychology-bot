/**
 * Admin API methods
 */

import apiClient from './client'
import type {
  User,
  Task,
  TaskCreate,
  TaskUpdate,
  Assignment,
  TaskDifficulty,
} from '@/types'

export const adminApi = {
  // ========== Users ==========

  /**
   * Получить список всех пользователей
   */
  getUsers: async (params?: {
    skip?: number
    limit?: number
    is_active?: boolean
  }): Promise<User[]> => {
    const response = await apiClient.get<User[]>('/api/v1/admin/users', {
      params,
    })
    return response.data
  },

  /**
   * Получить данные пользователя по ID
   */
  getUserById: async (userId: string): Promise<User> => {
    const response = await apiClient.get<User>(`/api/v1/admin/users/${userId}`)
    return response.data
  },

  // ========== Task Templates ==========

  /**
   * Получить список всех шаблонов заданий
   */
  getTaskTemplates: async (params?: {
    skip?: number
    limit?: number
    category?: string
    difficulty?: TaskDifficulty
  }): Promise<Task[]> => {
    const response = await apiClient.get<Task[]>(
      '/api/v1/admin/tasks/templates',
      { params }
    )
    return response.data
  },

  /**
   * Создать новый шаблон задания
   */
  createTaskTemplate: async (data: TaskCreate): Promise<Task> => {
    const response = await apiClient.post<Task>(
      '/api/v1/admin/tasks/templates',
      data
    )
    return response.data
  },

  /**
   * Обновить шаблон задания
   */
  updateTaskTemplate: async (
    taskId: string,
    data: TaskUpdate
  ): Promise<Task> => {
    const response = await apiClient.patch<Task>(
      `/api/v1/admin/tasks/templates/${taskId}`,
      data
    )
    return response.data
  },

  /**
   * Удалить шаблон задания
   */
  deleteTaskTemplate: async (taskId: string): Promise<void> => {
    await apiClient.delete(`/api/v1/admin/tasks/templates/${taskId}`)
  },

  /**
   * Назначить задание пользователю вручную
   */
  assignTaskToUser: async (
    userId: string,
    taskId: string
  ): Promise<Assignment> => {
    const response = await apiClient.post<Assignment>(
      `/api/v1/admin/users/${userId}/assign-task`,
      null,
      { params: { task_id: taskId } }
    )
    return response.data
  },
}
