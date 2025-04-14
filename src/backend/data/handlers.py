from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
from .database import get_async_client
from src.backend.schemas import UserInDB


class DatabaseHandlers:
    """Клас для зручної роботи з хендлерами і уникненю пошуку роботи функції."""
    def __init__(self):
        self.async_client = None

    async def init(self):
        if not self.async_client:
            self.async_client = await get_async_client()

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

    async def write_token(self, email: str, token: str) -> None:
        if not self.async_client:
            await self.init()

        try:
            info = {"email": email,
                    "token": token,
                    "expire_time": str(datetime.now(timezone.utc) + timedelta(days=30))}
            response = await self.async_client.table("refresh_tokens").insert(info).execute()

        except Exception as e:
            raise "Token already exists"

    async def remove_refresh_token(self, email: str) -> None:
        if not self.async_client:
            await self.init()

        try:
            response = await self.async_client.table("refresh_tokens").delete().eq("email", email).execute()
            print(response.data)

        except Exception as e:
            raise e

    async def update_refresh_token(self, email: str, token: str) -> None:
        if not self.async_client:
            await self.init()

        try:
            info = {"token": token,
                    "expire_time": str(datetime.now(tz=timezone.utc) + timedelta(days=30))}
            response = self.async_client.table("refresh_token").update(info).eq("email", email).execute()

        except Exception as e:
            raise e

    async def check_refresh_token(self, email: str) -> bool:
        """Перевіряє, чи існує дійсний refresh token для email."""
        if not self.async_client:
            await self.init()

        try:
            response = await self.async_client.table("refresh_tokens").select("*").eq("email", email).execute()

            if not response.data:
                return False

            record = response.data[0]
            token = record.get("token")
            expire_time = record.get("expire_time")

            if not token:
                return False

            if expire_time:
                try:
                    if isinstance(expire_time, str):
                        expire_time = parse(expire_time)

                    if expire_time.tzinfo is None:
                        expire_time = expire_time.replace(tzinfo=timezone.utc)

                    current_time = datetime.now(timezone.utc)
                    is_valid = expire_time > current_time
                    return is_valid
                except Exception as e:
                    print(f"Error parsing expire_time: {e}")
                    return False

            return True

        except Exception as e:
            print(f"Error in check_refresh_token: {e}")
            return False


handlers_manager = DatabaseHandlers()
