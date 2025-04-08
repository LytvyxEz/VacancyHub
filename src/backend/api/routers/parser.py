from fastapi import APIRouter, Request, Depends, HTTPException
from starlette.templating import Jinja2Templates
from concurrent.futures import ThreadPoolExecutor
import asyncio
from playwright.async_api import async_playwright


from src.backend.service import get_current_user
from src.backend.service import parse_vacancies, analyze_skills

parser_route = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@parser_route.get("/parse")
async def parse_page(request: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse("parser__.html", {
        "request": request,
        "user": user,
        "is_authenticated": user is not None
    })


@parser_route.get('/parse/results')
async def results(
    request: Request,
    user: str = Depends(get_current_user),
    query: str = "python"
):
    try:
        vacancies = await parse_vacancies(query)
        skills_data = await analyze_skills(vacancies)

        # sorted_skills = sorted(skills_data.items(), key=lambda x: x[1], reverse=True)
        # chart_labels = [skill[0] for skill in sorted_skills]
        # chart_values = [skill[1] for skill in sorted_skills]
        print(vacancies, skills_data)


        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "jobs": vacancies,
                "skills": skills_data,

                # "chart_data": {
                #     "labels": chart_labels,
                #     "values": chart_values
                # }
            }
        )
    except Exception as e:
        pass




