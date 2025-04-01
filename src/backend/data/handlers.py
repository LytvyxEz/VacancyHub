import asyncio
from supabase import AsyncClient
from .database import get_async_client
from src.backend.schemas import UserInDB


class DatabaseHandlers:
    """Клас для зручної роботи з хендлерами і уникненю пошуку роботи функції."""
    def __init__(self, async_client: AsyncClient):
        """Ініціалізація об'єкту класу і отримання з'єднання з БД"""
        self.async_client = async_client

    # async def get_all(self):
    #     """Проста функція для перевірки чи є під'єднання до БД(з часом можливо видалю)."""
    #     response = await self.async_client.table("users").select("*").execute()

    async def check_if_user_exists(self, email: str):  # Changed from user: UserInDB
        """Check if a user exists in the database by email"""
        try:
            response = await self.async_client.table("users").select("*").eq("email", email).execute()
            return bool(response.data)
        except Exception as e:
            raise ValueError(e)

    async def add_new_user(self, user: UserInDB) -> dict:
        """Функція для додавання нового користувача у БД, з данних потрібно тільки email і password."""
        try:
            info = {
                "email": user.email,
                "password": user.password
            }
            response = await self.async_client.table("users").insert(info).execute()
            return response.data[0]
        except Exception as e:
            raise ValueError(e)

    async def get_hashed_password_by_email(self, email: str) -> dict:
        """Функція планується для перевірки дійсності паролю
         шляхом витягування захешованого пароля з БД і порівняння з введеним щойно користувачем,
         return -> {"password": hashed_password, "email": email"""
        try:
            response = await self.async_client.table("users").select("password").eq("email", email).execute()
            return {"password": response.data[0]["password"], "email": response.data[0]["email"]}
        except Exception as e:
            raise ValueError("Invalid email")

    # async def delete_user_by_email(self, email: str):
    #     """Функція для видалення користувача по ел. пошті."""
    #     response = await self.async_client.table("users").delete().eq("email", email).execute()


a_client = asyncio.run(get_async_client())
handlers_manager = DatabaseHandlers(a_client)
