from fastapi import APIRouter, Request, Form, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.responses import JSONResponse

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


@auth_router.post('/auth/register')
async def register_user(
        request: Request,
        email:  Annotated[str, Form()],
        password: Annotated[str, Form()],
        confirm_password: Annotated[str, Form()]
):
    try:
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords don't match")

        if await handlers_manager.check_if_user_exists(email):
            raise HTTPException(status_code=400, detail='User already exists')

        user_create = User(
            email=email,
            password=password,
        )

        user_in_db = UserInDB.create_from_user(user_create)
        await handlers_manager.add_new_user(user_in_db)

        return JSONResponse(
            status_code=200,
            content={"message": "Registration successful"}
        )

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )


 
@auth_router.get('/auth/login')
async def login(request: Request):
    return templates.TemplateResponse('login.html', request=request, context={'request': request})


@auth_router.post('/auth/login')
async def login(request: Request, ):
    return templates.TemplateResponse('login.html', request=request, context={'request': request})
