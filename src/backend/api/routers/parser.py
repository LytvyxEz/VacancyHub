from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates
from collections import Counter
import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.test.test1 import run, get_info

parser_route = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


def run_sync():
    """Синхронна обгортка для асинхронного коду"""
    return asyncio.run(run())


def get_info_sync(links):
    """Синхронна обгортка для асинхронного коду"""
    return asyncio.run(get_info(links))


@parser_route.get('/skills')
async def skills(request: Request):
    try:
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            # Отримуємо посилання
            links = await loop.run_in_executor(executor, run_sync)

            # Отримуємо навички
            skills_data = await loop.run_in_executor(
                executor,
                get_info_sync,
                links
            )

            return templates.TemplateResponse(
                'parser.html',
                {
                    "request": request,
                    "jobs": links[:10],  # Перші 10 вакансій
                    "skills": skills_data,
                    "chart_data": {
                        "labels": list(skills_data.keys()),
                        "values": list(skills_data.values())
                    }
                }
            )
    except Exception as e:
        return templates.TemplateResponse(
            'error.html',
            {"request": request, "error": str(e)}
        )