from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from src.backend.models import JWT
import jwt


async def auth_middleware(request: Request, call_next):
    if request.url.path not in ("/parse", '/parse/results',
                                '/auth/logout/confirm', '/auth/logout'):
        return await call_next(request)

    access_token = request.cookies.get("access_token")

    if not access_token:
        response = RedirectResponse(url='/error?msg=Not+Authorized')
        response.set_cookie(key="next_url", value=request.url.path)
        return response

    try:
        payload = JWT.decode_jwt(access_token)

        if payload.get('typ') != "access":
            response = RedirectResponse(url='/error?msg=Invalid+token')
            response.set_cookie(key="next_url", value=request.url.path)
            return response

        request.state.user = payload["sub"]

    except jwt.ExpiredSignatureError:
        response = RedirectResponse(url='/error?msg=Invalid+token')
        response.set_cookie(key="next_url", value=request.url.path)
        return response

    except Exception as e:
        response = RedirectResponse(url=f'/error?msg={e}')
        response.set_cookie(key="next_url", value=request.url.path)
        return response

    return await call_next(request)
