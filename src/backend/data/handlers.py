import asyncio
from supabase import AsyncClient
from .database import get_async_client
from src.backend.schemas import User, UserInDB


class DatabaseHandlers:
    """Клас для зручної роботи з хендлерами і уникненю пошуку роботи функції."""
    def __init__(self):
        self.async_client = None

    async def init(self):
        if not self.async_client:
            self.async_client = await get_async_client()

    # async def get_all(self):
    #     """Проста функція для перевірки чи є під'єднання до БД(з часом можливо видалю)."""
    #     response = await self.async_client.table("users").select("*").execute()

    async def check_if_user_exists(self, email: str):
        """Функція для перевірки чи є користувач у БД"""
        if not self.async_client:
            await self.init()

        try:
            response = await self.async_client.table("users").select("*").eq("email", email).execute()
            return bool(response.data and len(response.data) > 0)
        except Exception as e:
            raise ValueError(f"Database error {e}")

    async def add_new_user(self, user: UserInDB) -> dict:
        """Функція для додавання нового користувача у БД, з данних потрібно тільки email і password."""
        if not self.async_client:
            await self.init()

        try:
            info = {
                "email": user.email,
                "password": user.password
            }
            response = await self.async_client.table("users").insert(info).execute()
            return response.data[0]
        except Exception as e:
            raise ValueError(f"Database error {e}")

    async def get_hashed_password_by_email(self, email: str) -> str:
        """Функція планується для перевірки дійсності паролю
         шляхом витягування захешованого пароля з БД і порівняння з введеним щойно користувачем,
         return -> hashed_password"""
        if not self.async_client:
            await self.init()

        try:
            response = await self.async_client.table("users").select("password").eq("email", email).execute()

            if not response.data or response.data is None:
                raise ValueError('User not found')

            return response.data[0]["password"]

        except Exception as e:
            raise ValueError(f"Database error {e}")

    # async def delete_user_by_email(self, email: str):
    #     """Функція для видалення користувача по ел. пошті."""
    #     response = await self.async_client.table("users").delete().eq("email", email).execute()


handlers_manager = DatabaseHandlers()
