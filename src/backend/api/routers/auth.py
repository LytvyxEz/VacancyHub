from fastapi import APIRouter, Request, Form, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.responses import JSONResponse, Response, RedirectResponse
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

from src.backend.data import handlers_manager
from src.backend.service import get_current_user
from src.backend.schemas import User, UserInDB
from src.backend.models import JWT

auth_router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_router.get('/auth/')
async def auth(request: Request):
    return templates.TemplateResponse('auth.html',
                                      request=request,
                                      context={'request': request})


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


@auth_router.get('/auth/logout/confirm')
async def logout_confirm(request: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse('logout.html', {'request': request})


@auth_router.get('/auth/logout')
async def logout(request: Request, user: str = Depends(get_current_user)):

    response = RedirectResponse(url="/", status_code=303)

    if request.cookies.get('access_token'):
        response.delete_cookie(key="access_token")

    if await handlers_manager.check_refresh_token(email=user):
        await handlers_manager.remove_refresh_token(email=user)

    return response


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

        access_token, refresh_token = JWT.create_tokens(email=email)

        await handlers_manager.write_token(token=refresh_token, email=email)

        response.set_cookie(
            key="access_token",
            value=access_token,
            expires=(datetime.utcnow() + timedelta(minutes=60 * 24)).strftime("%a, %d %b %Y %H:%M:%S GMT"),
            httponly=True,
            secure=True,
            samesite="lax",
            path="/"
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


@auth_router.get("/auth/refresh")
async def refresh(request: Request, user: str = Depends(get_current_user)):
    try:
        if handlers_manager.check_refresh_token(user):

            new_access_token, new_refresh_token = JWT.create_tokens(user)
            response = RedirectResponse(
                url=request.cookies.get("next_url"),
                status_code=status.HTTP_200_OK
            )

            handlers_manager.update_refresh_token(email=user,
                                                  token=new_refresh_token)

            response.set_cookie(
                key="access_token",
                value=new_access_token,
                expires=(datetime.utcnow() + timedelta(days=1)).strftime("%a, %d %b %Y %H:%M:%S GMT"),
                httponly=True,
                secure=True,
                samesite="lax",
                path="/"
            )

            response.delete_cookie(
                key="next_url"
            )

            return response

        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    except jwt.ExpiredSignatureError:
        response = RedirectResponse(
            "/auth/login",
            status_code=status.HTTP_303_SEE_OTHER
        )
        response.delete_cookie("access_token")
        response.delete_cookie(
            key="next_url"
        )
        return response
