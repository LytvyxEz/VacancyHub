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
        salary: Optional[int] = Form(None),
        max_pages: Optional[int] = Form(20)
):
    parser_query = parser_request(request, query, experience, location, salary, max_pages)

    return templates.TemplateResponse("parser__.html", {
        "request": request,
        'url_query': parser_query['url_query'],
        'query': parser_query['query'],
        'experience': parser_query['experience'],
        'location': parser_query['location'],
        'salary': parser_query['salary'],
        'max_pages': parser_query['max_pages'],
        'is_authenticated': True if request.cookies.get("access_token") else False
    })


@parser_route.post("/parse")
async def parse_page(
        request: Request,
        user: str = Depends(get_current_user),
        query: Optional[str] = Form(None),
        experience: Optional[str] = Form(None),
        location: Optional[str] = Form(None),
        salary: Optional[int] = Form(0),
        max_pages: int = Form(default=20)
):
    filters = variable_generator(request=request)

    if filters:
        experience = filters.get('experience') if experience else experience
        location = filters.get('location') if location else location
        salary = filters.get('salary') if salary else salary
        max_pages = filters.get('max_pages', max_pages)
    else:
        experience = experience
        location = location
        salary = salary
        max_pages = max_pages

    parser_query = parser_request(request, query, experience, location, salary, max_pages)

    return RedirectResponse(
        url=f"/parse/results?query={parser_query['query']}"
            f"&experience={parser_query['experience']}"
            f"&location={parser_query['location']}"
            f"&salary={parser_query['salary']}"
            f"&max_pages={parser_query['max_pages']}"
    )


@parser_route.api_route('/parse/results', methods=['GET', 'POST'])
async def results(
        request: Request,
        user: str = Depends(get_current_user),
        query: Optional[str] = Query(None)
):
    try:
        filters = variable_generator(request=request)

        if filters:
            if "salary" in filters:
                filters["salary"] = int(filters["salary"]) if filters["salary"] else 0
            if "max_pages" in filters:
                filters["max_pages"] = int(filters["max_pages"]) if filters["max_pages"] else 20

            experience = filters.get("experience")
            location = filters.get("location")
            salary = filters.get("salary", 0)
            max_pages = filters.get("max_pages", 20)
        else:
            experience = None
            location = None
            salary = 0
            max_pages = 20

        # vacancies = await parse_vacancies(query, filters)
        # skills_data = await analyze_skills(vacancies, filters)

        return templates.TemplateResponse(
            "results_.html",
            {
                "request": request,
                # "jobs": vacancies,
                # "skills": skills_data,
                'query': query,
                'experience': experience,
                'location': location,
                'salary': salary,
                'max_pages': max_pages,
                'is_authenticated': True if request.cookies.get("access_token") else False
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameter type: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
