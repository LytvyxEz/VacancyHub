from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


parser_route = APIRouter()
templates = Jinja2Templates(directory="src/frontend/templates")



@parser_route.get('/parse')
async def vacancy_analytic(request: Request):
    return templates.TemplateResponse('parser.html', {"request": request})


