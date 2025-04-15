from fastapi import Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse


def get_current_user(request: Request):
    if not hasattr(request.state, "user"):
        return RedirectResponse(url='/error?msg=Not+Authorized')
    return request.state.user
