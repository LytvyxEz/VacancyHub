from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.responses import JSONResponse, Response, RedirectResponse
from passlib.context import CryptContext

from src.backend.data import handlers_manager
from src.backend.utils import hash_password
from src.backend.schemas import User, UserInDB
from src.backend.models import JWT

auth_router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_router.get('/auth/')
async def auth(request: Request):
    return templates.TemplateResponse('auth.html', request=request, context={'request': request})


@auth_router.get('/auth/register')
async def register(request: Request):
    return templates.TemplateResponse('register.html', request=request, context={'request': request})


@auth_router.get('/auth/login')
async def login(request: Request):
    return templates.TemplateResponse('login.html', request=request, context={'request': request})


@auth_router.post('/auth/register')
async def register_user(
        request: Request,
        email: Annotated[str, Form()],
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
            status_code=status.HTTP_200_OK,
            content={'message': 'Successfully signed up'}

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


@auth_router.post('/auth/login')
async def login(request: Request,
                response: Response,
                email:  Annotated[str, Form()],
                password: Annotated[str, Form()]):

    try:

        if not await handlers_manager.check_if_user_exists(email):
            raise HTTPException(status_code=400, detail='User does not exists')

        hashed_password = await handlers_manager.get_hashed_password_by_email(email)

        if not pwd_context.verify(password, hashed_password):
            raise HTTPException(status_code=400, detail=f'Incorrect password')

        token = JWT.encode_jwt(email)

        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            path="/",
            max_age=60*60*24,
            httponly=False,
            secure=False,
        )

        response.status_code = 200
        response.body = b'{"message": "Successfully signed up"}'
        return response

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": "Invalid password or email"}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )
