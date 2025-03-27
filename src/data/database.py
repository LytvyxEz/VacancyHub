from supabase import create_async_client, AsyncClient
from config import DB_KEY, DB_URL


async def get_async_client():
    """Отримання зв'язку з базою данних."""
    async_client: AsyncClient = await create_async_client(supabase_url=DB_URL, supabase_key=DB_KEY)
    return async_client
