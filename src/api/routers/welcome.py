from fastapi import APIRouter


welcome_router = APIRouter()


@welcome_router.get('/')
async def welcome():
    ...
