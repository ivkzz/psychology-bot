/**
 * Users API methods
 */

import apiClient from './client'
import type { User, UserUpdate, UserProgress } from '@/types'

export const usersApi = {
  /**
   * Получить данные текущего пользователя
   */
  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>('/api/v1/users/me')
    return response.data
  },

  /**
   * Обновить данные текущего пользователя
   */
  updateCurrentUser: async (data: UserUpdate): Promise<User> => {
    const response = await apiClient.patch<User>('/api/v1/users/me', data)
    return response.data
  },

  /**
   * Получить статистику прогресса текущего пользователя
   */
  getUserProgress: async (): Promise<UserProgress> => {
    const response = await apiClient.get<UserProgress>(
      '/api/v1/users/me/progress'
    )
    return response.data
  },
}
