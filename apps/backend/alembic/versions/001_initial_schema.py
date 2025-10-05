"""Initial schema with seed data

Revision ID: 001
Revises:
Create Date: 2025-10-05 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime
import uuid
from passlib.context import CryptContext

# Импорт settings для получения admin credentials
from app.core.config import settings

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Создание всех таблиц и добавление seed данных.
    """
    # Создаем таблицу users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('telegram_id', sa.BigInteger(), nullable=True, unique=True, index=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True, unique=True, index=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=True),
        sa.Column('role', sa.Enum('USER', 'ADMIN', name='userrole'), nullable=False, server_default='USER'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    # Создаем таблицу tasks
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False, index=True),
        sa.Column('difficulty', sa.Enum('EASY', 'MEDIUM', 'HARD', name='taskdifficulty'), nullable=False, server_default='MEDIUM'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    # Создаем таблицу assignments
    op.create_table(
        'assignments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assigned_date', sa.Date(), nullable=False, server_default=sa.text('CURRENT_DATE'), index=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'COMPLETED', name='assignmentstatus'), nullable=False, server_default='PENDING', index=True),
        sa.Column('answer_text', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
    )

    # Создаем композитные индексы для assignments
    op.create_index('ix_assignments_user_date', 'assignments', ['user_id', 'assigned_date'])
    op.create_index('ix_assignments_user_status', 'assignments', ['user_id', 'status'])

    # ========== SEED DATA ==========

    # 1. Создаем администратора из настроек окружения
    admin_password_hash = pwd_context.hash(settings.ADMIN_PASSWORD)

    op.execute(f"""
        INSERT INTO users (id, name, email, hashed_password, role, is_active, created_at, updated_at)
        VALUES (
            '{uuid.uuid4()}',
            '{settings.ADMIN_NAME}',
            '{settings.ADMIN_EMAIL}',
            '{admin_password_hash}',
            'ADMIN',
            true,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        );
    """)

    # 2. Seed данные для tasks (шаблоны упражнений)
    tasks_seed_data = [
        # Медитация
        (uuid.uuid4(), 'Утренняя медитация осознанности',
         'Найдите тихое место. Сядьте удобно, закройте глаза. Сосредоточьтесь на своем дыхании. Наблюдайте за вдохами и выдохами в течение 10 минут. Если мысли отвлекают вас, мягко возвращайте внимание к дыханию.',
         'медитация', 'EASY'),

        (uuid.uuid4(), 'Медитация благодарности',
         'Вспомните 3 вещи, за которые вы благодарны сегодня. Сосредоточьтесь на чувстве благодарности. Почувствуйте, как оно наполняет вас теплом. Посвятите этому 5 минут.',
         'медитация', 'EASY'),

        (uuid.uuid4(), 'Сканирование тела',
         'Лягте на спину. Закройте глаза. Медленно перемещайте внимание от пальцев ног к макушке головы. Замечайте ощущения в каждой части тела. Расслабляйте напряженные зоны. 15 минут.',
         'медитация', 'MEDIUM'),

        # Дыхательные упражнения
        (uuid.uuid4(), 'Дыхание 4-7-8',
         'Вдохните через нос на счет 4. Задержите дыхание на счет 7. Выдохните через рот на счет 8. Повторите 4 раза. Это упражнение помогает успокоиться и снизить стресс.',
         'дыхание', 'EASY'),

        (uuid.uuid4(), 'Диафрагмальное дыхание',
         'Положите одну руку на грудь, другую на живот. Дышите так, чтобы двигалась только рука на животе. Это активирует парасимпатическую нервную систему. 5 минут.',
         'дыхание', 'EASY'),

        (uuid.uuid4(), 'Квадратное дыхание',
         'Вдох на 4 счета. Задержка на 4 счета. Выдох на 4 счета. Задержка на 4 счета. Повторите 10 циклов. Помогает сосредоточиться и снизить тревожность.',
         'дыхание', 'MEDIUM'),

        # Ведение дневника
        (uuid.uuid4(), 'Дневник благодарности',
         'Запишите 5 вещей, за которые вы благодарны сегодня. Они могут быть большими или маленькими. Опишите, почему вы за них благодарны и как они повлияли на ваш день.',
         'дневник', 'EASY'),

        (uuid.uuid4(), 'Анализ дня',
         'Ответьте на вопросы: Что было хорошего сегодня? Что было сложным? Чему я научился? Что я могу улучшить завтра? Пишите свободно, без самоцензуры.',
         'дневник', 'MEDIUM'),

        (uuid.uuid4(), 'Письмо себе из будущего',
         'Представьте себя через 5 лет. Напишите письмо себе настоящему от лица будущего "я". Какие советы вы бы дали? О чем бы предупредили? Что бы похвалили?',
         'дневник', 'HARD'),

        # Аффирмации
        (uuid.uuid4(), 'Утренние аффирмации',
         'Встаньте перед зеркалом. Посмотрите себе в глаза. Произнесите вслух 3 раза: "Я достоин любви и уважения", "Я справлюсь с любыми трудностями", "Я выбираю радость сегодня".',
         'аффирмации', 'EASY'),

        (uuid.uuid4(), 'Аффирмации для уверенности',
         'Запишите 5 ваших сильных сторон. Для каждой создайте аффирмацию в настоящем времени. Например: "Я обладаю творческим мышлением". Повторяйте их в течение дня.',
         'аффирмации', 'MEDIUM'),

        # Физическая активность
        (uuid.uuid4(), '10-минутная растяжка',
         'Выполните мягкую растяжку всего тела. Особое внимание уделите шее, плечам, спине и ногам. Двигайтесь медленно и осознанно. Дышите глубоко и ровно.',
         'физическая_активность', 'EASY'),

        (uuid.uuid4(), 'Прогулка на природе',
         'Прогуляйтесь на свежем воздухе минимум 20 минут. Обращайте внимание на звуки, запахи, ощущения. Отложите телефон. Просто присутствуйте в моменте.',
         'физическая_активность', 'EASY'),

        # Самопознание
        (uuid.uuid4(), 'Колесо жизненного баланса',
         'Оцените по шкале от 1 до 10 свою удовлетворенность в областях: здоровье, отношения, карьера, финансы, личностный рост, отдых, творчество, духовность. Определите 2 области для развития.',
         'самопознание', 'MEDIUM'),

        (uuid.uuid4(), 'Исследование эмоций',
         'Выберите эмоцию, которую вы часто испытываете. Опишите: Где в теле вы ее чувствуете? Какие мысли ее сопровождают? Что может быть ее причиной? Как она влияет на ваше поведение?',
         'самопознание', 'HARD'),
    ]

    # Вставляем задания
    for task_id, title, description, category, difficulty in tasks_seed_data:
        op.execute(f"""
            INSERT INTO tasks (id, title, description, category, difficulty, created_at)
            VALUES (
                '{task_id}',
                $${title}$$,
                $${description}$$,
                '{category}',
                '{difficulty}',
                CURRENT_TIMESTAMP
            );
        """)


def downgrade() -> None:
    """
    Откат миграции - удаление всех таблиц.
    """
    op.drop_index('ix_assignments_user_status', table_name='assignments')
    op.drop_index('ix_assignments_user_date', table_name='assignments')
    op.drop_table('assignments')
    op.drop_table('tasks')
    op.drop_table('users')

    # Удаляем enum типы
    op.execute('DROP TYPE IF EXISTS assignmentstatus;')
    op.execute('DROP TYPE IF EXISTS taskdifficulty;')
    op.execute('DROP TYPE IF EXISTS userrole;')
