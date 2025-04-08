from fastapi import Request, HTTPException, status
from src.backend.models import JWT


async def auth_middleware(request: Request, call_next):
    if request.url.path not in ("/parse", '/parse/search', '/parse/results', '/auth/logout/confirm', '/auth/logout'):
        return await call_next(request)

    token = request.cookies.get("access_token")

    try:
        if token:
            email = JWT.verify_token(token)
            request.state.user = email

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return await call_next(request)
