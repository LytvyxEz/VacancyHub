from fastapi import APIRouter


auth_router = APIRouter()


@auth_router.get('/auth')
async def auth():
    ...

@auth_router.post('/auth/register')
async def register():
    ...


@auth_router.post('/auth/login')
async def login():
    ...
