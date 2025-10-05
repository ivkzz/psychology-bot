/**
 * Tasks API methods
 */

import apiClient from './client'
import type { Assignment, AssignmentComplete } from '@/types'

export const tasksApi = {
  /**
   * Получить задание на сегодня
   */
  getTodayTask: async (): Promise<Assignment> => {
    const response = await apiClient.get<Assignment>('/api/v1/tasks/today')
    return response.data
  },

  /**
   * Отметить задание как выполненное
   */
  completeTask: async (
    assignmentId: string,
    data: AssignmentComplete
  ): Promise<Assignment> => {
    const response = await apiClient.post<Assignment>(
      `/api/v1/tasks/${assignmentId}/complete`,
      data
    )
    return response.data
  },

  /**
   * Получить историю заданий
   */
  getTaskHistory: async (params?: {
    limit?: number
    offset?: number
  }): Promise<Assignment[]> => {
    const response = await apiClient.get<Assignment[]>(
      '/api/v1/tasks/history',
      { params }
    )
    return response.data
  },
}
