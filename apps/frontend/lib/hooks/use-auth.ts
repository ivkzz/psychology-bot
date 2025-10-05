/**
 * Auth Hooks - хуки для аутентификации с TanStack Query
 */

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'
import { authApi } from '../api/auth'
import { usersApi } from '../api/users'
import { useAuthStore } from '../stores/auth-store'
import type { LoginRequest, RegisterRequest } from '@/types'

/**
 * Хук для получения данных текущего пользователя
 */
export function useCurrentUser() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  return useQuery({
    queryKey: ['users', 'me'],
    queryFn: usersApi.getCurrentUser,
    enabled: isAuthenticated, // Запрашиваем только если авторизован
    staleTime: 5 * 60 * 1000, // 5 минут
  })
}

/**
 * Хук для входа в систему
 */
export function useLogin() {
  const router = useRouter()
  const queryClient = useQueryClient()
  const setTokens = useAuthStore((state) => state.setTokens)

  return useMutation({
    mutationFn: (data: LoginRequest) => authApi.login(data),
    onSuccess: (response) => {
      // Сохраняем токены в Zustand (и localStorage)
      setTokens(response.access_token, response.refresh_token)

      // Инвалидируем кеш пользователя чтобы загрузить данные
      queryClient.invalidateQueries({ queryKey: ['users', 'me'] })

      // Редирект на dashboard
      router.push('/dashboard')
    },
  })
}

/**
 * Хук для регистрации
 */
export function useRegister() {
  const router = useRouter()
  const queryClient = useQueryClient()
  const setTokens = useAuthStore((state) => state.setTokens)

  return useMutation({
    mutationFn: (data: RegisterRequest) => authApi.register(data),
    onSuccess: (response) => {
      // Сохраняем токены в Zustand (и localStorage)
      setTokens(response.access_token, response.refresh_token)

      // Сохраняем user data в кеше TanStack Query
      queryClient.setQueryData(['users', 'me'], response.user)

      // Редирект на dashboard
      router.push('/dashboard')
    },
  })
}

/**
 * Хук для выхода из системы
 */
export function useLogout() {
  const router = useRouter()
  const queryClient = useQueryClient()
  const clearTokens = useAuthStore((state) => state.clearTokens)

  return useMutation({
    mutationFn: () => authApi.logout(),
    onSuccess: () => {
      // Очищаем токены из Zustand (и localStorage)
      clearTokens()

      // Очищаем весь кеш TanStack Query
      queryClient.clear()

      // Редирект на login
      router.push('/login')
    },
    onError: () => {
      // Даже при ошибке очищаем токены и редиректим
      clearTokens()
      queryClient.clear()
      router.push('/login')
    },
  })
}
