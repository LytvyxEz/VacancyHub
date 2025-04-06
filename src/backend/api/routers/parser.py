from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from src.backend.service import get_current_user
from typing import Optional
import json
import plotly

parser_router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")



@parser_router.get("/parse/search", response_class=HTMLResponse)
async def parse_jobs(
        request: Request,
        position: Optional[str] = Query(None),
        location: Optional[str] = Query(None),
        experience: Optional[str] = Query(None),
        salary_min: Optional[int] = Query(None),
        user: str = Depends(get_current_user)
):
    skill_counts = {}
    vacancies_count = 0
    avg_salary = 0

    if position:
        try:
            # skill_counts = await job_parser.analyze_job_market(position, location)

            vacancies_count = len(skill_counts) * 3
            avg_salary = 45000

            if experience:
                pass

            if salary_min:
                pass

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return templates.TemplateResponse(
        "parser_.html",
        {
            "request": request,
            "skill_counts": json.dumps(skill_counts),
            "vacancies_count": vacancies_count,
            "avg_salary": f"{avg_salary:,}",
            "search_query": position or "",
            "location": location or ""
        }
    )


@parser_router.get("/parse/results")
async def get_job_stats(
        request: Request,
        # position: str,
        location: Optional[str] = None,
        experience: Optional[str] = None,
        salary_min: Optional[int] = None,
        user: str = Depends(get_current_user)
):
    try:
        # skill_counts = await job_parser.analyze_job_market(position, location)
        return templates.TemplateResponse('results.html', {'request': request})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
