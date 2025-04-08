from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates
from collections import Counter
import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.test.test1 import run, get_info

parser_route = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/parse", response_class=HTMLResponse)
async def parse_page(request: Request):
    return templates.TemplateResponse("parser.html", {"request": request})


@router.get("/parse/search")
async def search_vacancies(request: Request, query: str = "python", limit: int = 10):
    try:
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            vacancies = await loop.run_in_executor(
                executor,
                lambda: asyncio.run(parse_vacancies(query, limit)))

            # Analyze skills
            skills_data = await loop.run_in_executor(
                executor,
                lambda: asyncio.run(analyze_skills(vacancies)))

            # Prepare chart data
            sorted_skills = sorted(skills_data.items(), key=lambda x: x[1], reverse=True)
            chart_labels = [skill[0] for skill in sorted_skills]
            chart_values = [skill[1] for skill in sorted_skills]

            return templates.TemplateResponse(
                "results.html",
                {
                    "request": request,
                    "jobs": vacancies,
                    "skills": skills_data,
                    "chart_data": {
                        "labels": chart_labels,
                        "values": chart_values
                    }
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))