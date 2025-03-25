from fastapi import Request, HTTPException


def get_access_token(request: Request):
    token = request.session.get("access_token")

    if not token:
        raise HTTPException(401, "Not authorized: No token found in session")
    return token
