from src.backend.service.user_service import get_current_user
from src.backend.service.scraper_service import WorkUaScraper
import asyncio

async def parse_vacancies(query: str, filters: dict):
    scraper = WorkUaScraper()
    return await scraper.get_links(search=query, filters=filters)


async def analyze_skills(vacancy_links: list[str], filters: dict):
    scraper = WorkUaScraper()
    return await scraper.get_skills_from_links(vacancy_links, filters)


