from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from src.backend.models import JWT
import jwt


async def auth_middleware(request: Request, call_next):
    if request.url.path not in ("/parse", '/parse/results',
                                '/auth/logout/confirm', '/auth/logout'):
        return await call_next(request)

    access_token = request.cookies.get("access_token")

    try:
        if access_token:
            payload = JWT.decode_jwt(access_token)
            if payload.get('typ') != "access":
                return RedirectResponse(url='/error?msg=Not+Authorized')
            request.state.user = payload["sub"]

    except jwt.ExpiredSignatureError:
        return RedirectResponse(url='/error?msg=Not+Authorized')

    except Exception as e:
        return RedirectResponse(url=f'/error?msg={e}')

    return await call_next(request)
