from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from src.backend.models import JWT
import jwt


async def auth_middleware(request: Request, call_next):
    if request.url.path not in ("/parse", '/parse/results',
                                '/auth/logout/confirm', '/auth/logout'):
        return await call_next(request)

    access_token = request.cookies.get("access_token")
    response = RedirectResponse(url='/error?msg=Not+Authorized')
    response.set_cookie(key="next_url",
                        value=request.url.path,
                        )
    try:
        if access_token:
            payload = JWT.decode_jwt(access_token)
            if payload.get('typ') != "access":
                return response
            request.state.user = payload["sub"]

    except jwt.ExpiredSignatureError:
        return response

    except Exception as e:
        return RedirectResponse(url=f'/error?msg={e}')

    return await call_next(request)
