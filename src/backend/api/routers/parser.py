from fastapi import APIRouter, Request, Depends, HTTPException, Form, Query
from typing import Optional, Annotated
from starlette.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from concurrent.futures import ThreadPoolExecutor
import asyncio
from playwright.async_api import async_playwright

from src.backend.schemas import ParserRequest, parser_request
from src.backend.service import parse_vacancies, analyze_skills, get_current_user
from src.backend.utils import variable_generator

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


    parser_query = parser_request(request, query, experience, location, salary)


    return templates.TemplateResponse("parser__.html", {
        "request": request,
        'url_query': parser_query['url_query'],
        'query': parser_query['query'],
        'experience': parser_query['experience'],
        'location': parser_query['location'],
        'salary': parser_query['salary'],
        'is_authenticated': True if request.cookies.get("access_token") else False
    })


@parser_route.post("/parse")
async def parse_page(
            request: Request,
            user: str = Depends(get_current_user),
            query: Optional[str] = Form(None),
            experience: Optional[str] = Form(None),
            location: Optional[str] = Form(None),
            salary: Optional[int] = Form(None)
        ):

    filters = variable_generator(request=request)
    parser_query = parser_request(request, query, filters['experience'], filters['location'], filters['salary'])


    return RedirectResponse(url=f"/parse/results?query={parser_query['query']}&{parser_query['url_query']}")


@parser_route.api_route('/parse/results', methods=['GET', 'POST'])
async def results(
    request: Request,
    user: str = Depends(get_current_user),
    query: Optional[str] = Query(None)
):
    try:
        filters = variable_generator(request=request)

        experience = filters.get("experience")
        location = filters.get("location")
        salary = filters.get("salary")

        vacancies = await parse_vacancies(query, filters)
        skills_data = await analyze_skills(vacancies, filters)

        return templates.TemplateResponse(
            "results_.html",
            {
                "request": request,
                "jobs": vacancies,
                "skills": skills_data,
                'query': query,
                'experience': experience,
                'location': location,
                'salary': salary,
                'is_authenticated': True if request.cookies.get("access_token") else False
            }
        )
    except Exception as e:
        print(e)

