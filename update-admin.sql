-- SQL скрипт для обновления данных администратора
-- Использование: выполните через PgAdmin или docker exec

-- Обновить email, имя и активность админа
UPDATE users
SET
    email = 'klevin.ivan.ivk@yandex.ru',
    name = 'IVKZ',
    is_active = true,
    updated_at = CURRENT_TIMESTAMP
WHERE role = 'ADMIN';

-- Показать результат
SELECT id, name, email, role, is_active, created_at
FROM users
WHERE role = 'ADMIN';
