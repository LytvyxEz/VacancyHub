from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from src.data import handlers_manager
from src.utils import hash_password
from src.schemas import User


auth_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@auth_router.get('/auth/')
async def auth(request: Request):
    return templates.TemplateResponse('auth.html', request=request, context={'request': request})


@auth_router.get('/auth/register')
async def register(request: Request, user: User):

    handlers_manager.add_new_user(user=user)

    return templates.TemplateResponse('register.html', request=request, context={'user': User})


@auth_router.post('/auth/register')
async def register(request: Request, user: User):

    handlers_manager.add_new_user(user=user)

    return

 
@auth_router.get('/auth/login')
async def login(request: Request):

    return templates.TemplateResponse('login.html', request=request, context={'request': request})
