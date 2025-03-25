from fastapi import APIRouter


root_router = APIRouter()


@root_router.post('/analytic')
async def vacancy_analytic():
    ...


@root_router.post('/search')
async def vacancy_search():
    ...
