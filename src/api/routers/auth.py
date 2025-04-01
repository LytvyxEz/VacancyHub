from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated

from src.data import handlers_manager
from src.utils import hash_password
from src.schemas import User, UserInDB

auth_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@auth_router.get('/auth/')
async def auth(request: Request):
    return templates.TemplateResponse('auth.html', request=request, context={'request': request})


@auth_router.get('/auth/register')
async def register(request: Request):
    return templates.TemplateResponse('register.html', request=request, context={'request': request})


@auth_router.post('/auth/register', response_class=HTMLResponse)
async def register_user(
        request: Request,
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        confirm_password: Annotated[str, Form()]
):
    user_create = UserCreate(
        email=email,
        password=password,
        confirm_password=confirm_password
    )

    user_in_db = UserInDB.create_from_user(user_create)

    handlers_manager.add_new_user(user_in_db)

    return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)


 
@auth_router.get('/auth/login')
async def login(request: Request):
    return templates.TemplateResponse('login.html', request=request, context={'request': request})


@auth_router.post('/auth/login')
async def login(request: Request, ):
    return templates.TemplateResponse('login.html', request=request, context={'request': request})
