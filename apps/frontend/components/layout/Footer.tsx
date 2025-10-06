/**
 * Footer - подвал сайта
 */

import Link from 'next/link'
import { Brain } from 'lucide-react'

export function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-t bg-muted/30">
      <div className="container mx-auto max-w-7xl py-8 px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Логотип и описание */}
          <div className="flex flex-col gap-4">
            <div className="flex items-center gap-2">
              <Brain className="h-5 w-5 text-primary" />
              <span className="text-lg font-bold">Psychology Bot</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Ежедневные психологические упражнения для улучшения эмоционального
              состояния
            </p>
          </div>

          {/* Навигация */}
          <div className="flex flex-col gap-2">
            <h3 className="font-semibold">Навигация</h3>
            <Link
              href="/dashboard"
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              Главная
            </Link>
            <Link
              href="/tasks"
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              Задания
            </Link>
            <Link
              href="/history"
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              История
            </Link>
            <Link
              href="/stats"
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              Статистика
            </Link>
          </div>

          {/* Дополнительно */}
          <div className="flex flex-col gap-2">
            <h3 className="font-semibold">Поддержка</h3>
            <Link
              href="/profile"
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              Профиль
            </Link>
            <a
              href="mailto:support@psychologybot.com"
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              Связаться с нами
            </a>
          </div>
        </div>

        {/* Копирайт */}
        <div className="mt-8 pt-8 border-t text-center text-sm text-muted-foreground">
          © {currentYear} Psychology Bot. Все права защищены.
        </div>
      </div>
    </footer>
  )
}
