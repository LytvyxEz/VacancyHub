from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

welcome_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@welcome_router.get('/')
async def welcome(request: Request):

    return templates.TemplateResponse('index.html', request=request, context={'request': request})
