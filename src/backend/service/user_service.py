from fastapi import Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse


def get_current_user(request: Request):
    if not hasattr(request.state, "user"):
        response = RedirectResponse(url='/error?msg=Not+Authorized')
        response.status_code = 401
        return response
    return request.state.user
