/**
 * Middleware - защита роутов и проверка аутентификации
 */

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Получаем токен из cookies или localStorage (проверяем через header)
  const accessToken = request.cookies.get('accessToken')?.value

  // Защищенные роуты (требуют авторизации)
  const protectedRoutes = ['/dashboard', '/admin', '/tasks', '/history', '/stats', '/profile']
  const isProtectedRoute = protectedRoutes.some((route) =>
    pathname.startsWith(route)
  )

  // Публичные роуты (только для неавторизованных)
  const authRoutes = ['/login', '/register']
  const isAuthRoute = authRoutes.some((route) => pathname.startsWith(route))

  // Если пользователь не авторизован и пытается зайти на защищенный роут
  if (isProtectedRoute && !accessToken) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Если пользователь авторизован и пытается зайти на login/register
  if (isAuthRoute && accessToken) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  // Во всех остальных случаях пропускаем
  return NextResponse.next()
}

// Конфигурация - на каких роутах запускать middleware
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
