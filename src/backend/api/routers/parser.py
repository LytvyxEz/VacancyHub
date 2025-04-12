from fastapi import APIRouter, Request, Depends, HTTPException, Form, Query
from typing import Optional, Annotated
from starlette.templating import Jinja2Templates
from concurrent.futures import ThreadPoolExecutor
import asyncio
from playwright.async_api import async_playwright

from src.backend.schemas import ParserRequest, query_validator
from src.backend.service import get_current_user
from src.backend.service import parse_vacancies, analyze_skills

parser_route = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@parser_route.get("/parse")
async def parse_page(
            request: Request,
            user: str = Depends(get_current_user),
            query: Optional[str] = Form(None),
            experience: Optional[str] = Form(None),
            location: Optional[str] = Form(None),
            salary: Optional[int] = Form(None)
        ):


    parser_request = ParserRequest(
        query=query,
        experience=experience,
        location=location,
        salary=salary
    )

    query = parser_request.query
    experience = parser_request.experience
    location = parser_request.location
    salary = parser_request.salary

    return templates.TemplateResponse("parser__.html", {
        "request": request,
        'query': query,
        'experience': experience,
        'location': location,
        'salary': salary,
        'is_authenticated': True if request.cookies.get("access_token") else False
    })


@parser_route.post("/parse")
async def parse_page(
            request: Request,
            user: str = Depends(get_current_user),
            query: str = Depends(query_validator),
            experience: Optional[str] = Form(None),
            location: Optional[str] = Form(None),
            salary: Optional[int] = Form(None)
        ):


    ParserRequest(
        query=query,
        experience=experience,
        location=location,
        salary=salary
    )

    query = parser_request.query
    experience = parser_request.experience
    location = parser_request.location
    salary = parser_request.salary

    return templates.TemplateResponse("parser__.html", {
        "request": request,
        'query': query if query else None,
        'experience': experience if experience else None,
        'location': location if location else None,
        'salary': salary if salary else None,
        'is_authenticated': True if request.cookies.get(
            "access_token") else False
    })


@parser_route.get('/parse/results')
async def results(
        request: Request,
        user: str = Depends(get_current_user),
        query: str = Query(),
        experience: Optional[str] = Query(),
        location: Optional[str] = Query(),
        salary: Optional[str] = Query()
):
    try:
        filters = {
            'experience': experience,
            'location': location,
            'salary': salary
        }
        vacancies = await parse_vacancies(query, filters)
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
                'query': query if query else None,
                'experience': experience if experience else None,
                'location': location if location else None,
                'salary': salary if salary else None,
                'is_authenticated': True if request.cookies.get(
                    "access_token") else False

                # "chart_data": {
                #     "labels": chart_labels,
                #     "values": chart_values
                # }
            }
        )
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Something went wrong</h1><p>{str(e)}</p>",
            status_code=500
        )
