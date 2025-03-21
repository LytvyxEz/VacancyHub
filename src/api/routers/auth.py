from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

auth_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@auth_router.get('/auth/')
async def auth(request: Request):

    return templates.TemplateResponse('auth.html', request=request, context={'request': request})

@auth_router.post('/auth/register')
async def register():
    ...


@auth_router.post('/auth/login')
async def login():
    ...
