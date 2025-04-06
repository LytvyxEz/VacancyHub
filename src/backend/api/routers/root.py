from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from src.backend.service import get_current_user

root_router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@root_router.get('/')
async def home(request: Request):
    return templates.TemplateResponse('index.html', {"request": request,
                                                     'is_authenticated': True if request.cookies.get(
                                                         "access_token") else False})


@root_router.get('/about')
async def about(request: Request):
    return templates.TemplateResponse('about.html', {"request": request,
                                                     'is_authenticated': True if request.cookies.get(
                                                         "access_token") else False})


@root_router.get('/features')
async def features(request: Request):
    return templates.TemplateResponse('features.html', {"request": request,
                                                        'is_authenticated': True if request.cookies.get(
                                                            "access_token") else False})


@root_router.get('/privacy')
async def privacy(request: Request):
    return templates.TemplateResponse('privacy.html', {"request": request,
                                                       'is_authenticated': True if request.cookies.get(
                                                           "access_token") else False})


@root_router.get('/terms')
async def privacy(request: Request):
    return templates.TemplateResponse('terms.html', {"request": request,
                                                     'is_authenticated': True if request.cookies.get(
                                                         "access_token") else False})


@root_router.get('/cookie')
async def privacy(request: Request):
    return templates.TemplateResponse('cookie.html', {"request": request,
                                                      'is_authenticated': True if request.cookies.get(
                                                          "access_token") else False})
