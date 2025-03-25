import asyncio
from database import async_client
from src.schemas import User
import logging


logging.basicConfig(level=logging.DEBUG)


async def get_all():
    response = await async_client.table("users").select("*").execute()
    print(response.data)


async def add_new_user(user: User):
    info = {
        "email": user.email,
        "password": user.password
    }
    response = await async_client.table("users").insert(info).execute()

user = User(_id=1, email='emaildfs@gmail.com', password='03gub12f80')
asyncio.run(add_new_user(user))
