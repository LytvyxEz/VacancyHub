from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from src.test import run, get_info, get_link
import plotly
import json

parser_route = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")



@parser_route.get("/get-skills")
async def get_skills(request: Request):
    job_links = await run()
    skill_counts = await get_info(job_links)

    return templates.TemplateResponse(
        "parser.html",
        {"request": request, "skill_counts": json.dumps(skill_counts)}
    )
