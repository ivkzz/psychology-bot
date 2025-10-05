/**
 * Home Page - перенаправление на dashboard или login
 */

import { redirect } from 'next/navigation'

export default function Home() {
  // Редиректим на login, middleware обработает логику
  redirect('/login')
}
