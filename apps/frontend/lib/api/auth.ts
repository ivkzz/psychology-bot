/**
 * Auth API methods
 */

import apiClient from './client'
import type {
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  RegisterResponse,
} from '@/types'

export const authApi = {
  /**
   * Регистрация нового пользователя
   */
  register: async (data: RegisterRequest): Promise<RegisterResponse> => {
    const response = await apiClient.post<RegisterResponse>(
      '/api/v1/auth/register',
      data
    )
    return response.data
  },

  /**
   * Вход в систему
   */
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>(
      '/api/v1/auth/login',
      data
    )
    return response.data
  },

  /**
   * Обновление access token через refresh token
   */
  refresh: async (refreshToken: string): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>(
      '/api/v1/auth/refresh',
      { refresh_token: refreshToken }
    )
    return response.data
  },

  /**
   * Выход из системы (информационный эндпоинт)
   */
  logout: async (): Promise<void> => {
    await apiClient.post('/api/v1/auth/logout')
  },
}
