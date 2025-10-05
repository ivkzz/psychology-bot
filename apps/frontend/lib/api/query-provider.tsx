/**
 * TanStack Query Provider для управления серверным состоянием
 */

'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { useState, type ReactNode } from 'react'

export function QueryProvider({ children }: { children: ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // Данные считаются свежими 5 минут
            staleTime: 5 * 60 * 1000,
            // Кеш хранится 10 минут
            gcTime: 10 * 60 * 1000,
            // Не refetch при каждом focus окна (можно включить позже)
            refetchOnWindowFocus: false,
            // Retry 1 раз при ошибке
            retry: 1,
          },
          mutations: {
            // Retry 0 раз для mutations (не повторяем POST/PATCH/DELETE)
            retry: 0,
          },
        },
      })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {/* Devtools только в development */}
      {process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  )
}
