"""
HTTP клиент для взаимодействия с Backend API.
Все запросы к Backend должны проходить через этот клиент.
"""

import logging
from typing import Optional, Dict, Any, List
import httpx
from bot.config import bot_settings

logger = logging.getLogger(__name__)


class BackendAPIClient:
    """
    Асинхронный HTTP клиент для взаимодействия с Backend API.
    """

    def __init__(self):
        """Инициализация клиента."""
        self.base_url = bot_settings.BACKEND_API_URL
        self.api_prefix = "/api/v1"
        self.timeout = 30.0

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        token: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Выполняет HTTP запрос к Backend API.

        Args:
            method: HTTP метод (GET, POST, PUT, DELETE)
            endpoint: API endpoint (например, "/users/me")
            data: Данные для отправки в теле запроса
            params: Query параметры
            token: JWT токен для авторизации

        Returns:
            Optional[Dict[str, Any]]: Ответ от API или None при ошибке
        """
        url = f"{self.base_url}{self.api_prefix}{endpoint}"
        headers = {}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

    # Authentication methods
    async def register_user(
        self,
        name: str,
        email: str,
        password: str,
        telegram_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Регистрация нового пользователя.

        Args:
            name: Имя пользователя
            email: Email пользователя
            password: Пароль для веб-версии
            telegram_id: Telegram ID пользователя

        Returns:
            Dict с access_token и user данными или None при ошибке
        """
        data = {
            "name": name,
            "email": email,
            "password": password,
            "telegram_id": telegram_id
        }
        return await self._make_request("POST", "/auth/register", data=data)

    async def login(
        self,
        telegram_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Авторизация пользователя по Telegram ID.

        Args:
            telegram_id: Telegram ID пользователя

        Returns:
            Dict с access_token или None при ошибке
        """
        data = {"telegram_id": telegram_id}
        return await self._make_request("POST", "/auth/login", data=data)

    async def get_user_by_telegram_id(
        self,
        telegram_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Получение пользователя по Telegram ID.

        Args:
            telegram_id: Telegram ID пользователя

        Returns:
            Dict с данными пользователя или None если не найден
        """
        try:
            # Сначала логинимся чтобы получить токен
            login_result = await self.login(telegram_id)
            if not login_result or "access_token" not in login_result:
                return None

            token = login_result["access_token"]
            user_data = await self.get_current_user(token)

            if user_data:
                user_data["access_token"] = token

            return user_data
        except Exception as e:
            logger.error(f"Error getting user by telegram_id: {str(e)}")
            return None

    # User methods
    async def get_user_info(
        self,
        user_id: str,
        token: str
    ) -> Optional[Dict[str, Any]]:
        """Получение информации о пользователе."""
        return await self._make_request(
            "GET",
            f"/users/{user_id}",
            token=token
        )

    async def get_current_user(
        self,
        token: str
    ) -> Optional[Dict[str, Any]]:
        """Получение информации о текущем пользователе."""
        return await self._make_request("GET", "/users/me", token=token)

    # Task methods
    async def get_user_tasks(
        self,
        token: str,
        status: Optional[str] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """Получение списка заданий пользователя."""
        params = {"status": status} if status else None
        return await self._make_request("GET", "/tasks", params=params, token=token)

    async def get_today_task(
        self,
        token: str
    ) -> Optional[Dict[str, Any]]:
        """
        Получение задания на сегодня.

        Args:
            token: JWT токен пользователя

        Returns:
            Dict с заданием на сегодня, или dict с ключом 'already_completed', или None при ошибке
        """
        url = f"{self.base_url}{self.api_prefix}/tasks/today"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)

                # Если 409 - пользователь уже выполнил задание
                if response.status_code == 409:
                    return {"already_completed": True, "detail": response.json().get("detail", "Вы уже выполнили задание на сегодня")}

                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

    async def get_task(
        self,
        task_id: str,
        token: str
    ) -> Optional[Dict[str, Any]]:
        """Получение детальной информации о задании."""
        return await self._make_request("GET", f"/tasks/{task_id}", token=token)

    async def complete_task(
        self,
        assignment_id: str,
        answer_text: Optional[str],
        token: str
    ) -> Optional[Dict[str, Any]]:
        """
        Отметить задание как выполненное.

        Args:
            assignment_id: ID назначения задания
            answer_text: Текст ответа пользователя (опционально)
            token: JWT токен пользователя

        Returns:
            Dict с результатом или None при ошибке
        """
        data = {"answer_text": answer_text} if answer_text else {}
        return await self._make_request(
            "POST",
            f"/tasks/{assignment_id}/complete",
            data=data,
            token=token
        )

    async def update_task_status(
        self,
        task_id: str,
        status: str,
        token: str
    ) -> Optional[Dict[str, Any]]:
        """Обновление статуса задания."""
        data = {"status": status}
        return await self._make_request(
            "PUT",
            f"/tasks/{task_id}/status",
            data=data,
            token=token
        )

    async def submit_task_answer(
        self,
        task_id: str,
        answer: str,
        token: str
    ) -> Optional[Dict[str, Any]]:
        """Отправка ответа на задание."""
        data = {"answer": answer}
        return await self._make_request(
            "POST",
            f"/tasks/{task_id}/submit",
            data=data,
            token=token
        )

    async def get_user_progress(
        self,
        token: str
    ) -> Optional[Dict[str, Any]]:
        """
        Получение статистики прогресса пользователя.

        Args:
            token: JWT токен пользователя

        Returns:
            Dict со статистикой или None при ошибке
        """
        return await self._make_request("GET", "/users/me/progress", token=token)

    # Admin methods
    async def get_all_users(
        self,
        admin_token: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Получение списка всех пользователей (для планировщика).

        Args:
            admin_token: Админский JWT токен

        Returns:
            Список пользователей или None при ошибке
        """
        return await self._make_request("GET", "/admin/users", token=admin_token)

    # Health check
    async def health_check(self) -> bool:
        """Проверка доступности Backend API."""
        try:
            response = await self._make_request("GET", "/health")
            return response is not None
        except Exception:
            return False


# Глобальный экземпляр клиента
api_client = BackendAPIClient()
