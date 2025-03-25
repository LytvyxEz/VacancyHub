from config import DB_KEY, DB_URL
from supabase import AsyncClient, create_async_client


async_client: AsyncClient = create_async_client(DB_URL, DB_KEY)
