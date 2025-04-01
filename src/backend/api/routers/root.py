from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

root_router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@root_router.get('/')
async def home(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@root_router.get('/about')
async def about(request: Request):
    return templates.TemplateResponse('about.html', {"request": request})


@root_router.get('/features')
async def features(request: Request):
    return templates.TemplateResponse('features.html', {"request": request})


@root_router.get('/privacy')
async def privacy(request: Request):
    return templates.TemplateResponse('privacy.html', {"request": request})

@root_router.get('/terms')
async def privacy(request: Request):
    return templates.TemplateResponse('terms.html', {"request": request})

@root_router.get('/cookie')
async def privacy(request: Request):
    return templates.TemplateResponse('cookie.html', {"request": request})
