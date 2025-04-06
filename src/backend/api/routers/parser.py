from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from src.backend.service import get_current_user
from src.backend.utils import run, get_info, get_links
import plotly
import json

parser_route = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@parser_route.get("/parse")
async def parse(request: Request, user: str = Depends(get_current_user)):
    # job_links = await run()
    # skill_counts = await get_info(job_links)

    return templates.TemplateResponse(
        "parser.html",
        {"request": request, "skill_counts": json.dumps('hello world!'),
                                               'is_login': True if request.cookies.get("access_token") else False}
    )
