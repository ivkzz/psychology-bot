/**
 * Axios HTTP client с interceptors для автоматической обработки токенов
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'
import type { ApiError } from '@/types'

// Создаем axios instance
export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 секунд
})

// Request interceptor - добавляем токен к каждому запросу
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Получаем токен из localStorage
    const token = typeof window !== 'undefined'
      ? localStorage.getItem('accessToken')
      : null

    // Добавляем токен в headers если он есть
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - обрабатываем ошибки и автообновление токена
apiClient.interceptors.response.use(
  (response) => {
    // Успешный ответ - возвращаем как есть
    return response
  },
  async (error: AxiosError<ApiError>) => {
    const originalRequest = error.config

    // Если ошибка 401 и это не запрос на refresh/login
    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest.url?.includes('/auth/login') &&
      !originalRequest.url?.includes('/auth/refresh')
    ) {
      try {
        // Пытаемся обновить токен
        const refreshToken = typeof window !== 'undefined'
          ? localStorage.getItem('refreshToken')
          : null

        if (!refreshToken) {
          // Нет refresh token - редирект на login
          if (typeof window !== 'undefined') {
            localStorage.removeItem('accessToken')
            localStorage.removeItem('refreshToken')
            document.cookie = 'accessToken=; path=/; max-age=0'
            document.cookie = 'refreshToken=; path=/; max-age=0'
            window.location.href = '/login'
          }
          return Promise.reject(error)
        }

        // Запрос на обновление токена
        const response = await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/refresh`,
          { refresh_token: refreshToken }
        )

        const { access_token, refresh_token } = response.data

        // Сохраняем новые токены в localStorage и cookies
        if (typeof window !== 'undefined') {
          localStorage.setItem('accessToken', access_token)
          localStorage.setItem('refreshToken', refresh_token)
          document.cookie = `accessToken=${access_token}; path=/; max-age=${15 * 60}; SameSite=Lax`
          document.cookie = `refreshToken=${refresh_token}; path=/; max-age=${7 * 24 * 60 * 60}; SameSite=Lax`
        }

        // Повторяем оригинальный запрос с новым токеном
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`
        }

        return apiClient(originalRequest)
      } catch (refreshError) {
        // Ошибка при обновлении токена - редирект на login
        if (typeof window !== 'undefined') {
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          document.cookie = 'accessToken=; path=/; max-age=0'
          document.cookie = 'refreshToken=; path=/; max-age=0'
          window.location.href = '/login'
        }
        return Promise.reject(refreshError)
      }
    }

    // Для других ошибок - возвращаем как есть
    return Promise.reject(error)
  }
)

export default apiClient
