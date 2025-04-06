import sys
from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates
import asyncio
from src.test import run, get_info

parser_route = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@parser_route.get('/skills')
async def skills(request: Request):
    try:
        # Don't set event loop policy here - let Playwright handle it
        links = await run()
        info = await get_info(links)
        print(info)

        chart_data = {
            "labels": list(info.keys()),
            "values": list(info.values())
        }

        return templates.TemplateResponse('parser.html', {
            "request": request,
            "jobs": links,
            "skills": info,
            "chart_data": chart_data
        })
    except Exception as e:
        return templates.TemplateResponse('error.html', {
            "request": request,
            "error": str(e)
        })