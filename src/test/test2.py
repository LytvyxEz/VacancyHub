import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin
import re


async def fetch_html(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'uk-UA,uk;q=0.9'
    }
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.text()
            print(f"Помилка: статус {response.status} для {url}")
            return None
    except Exception as e:
        print(f"Помилка отримання {url}: {e}")
        return None


async def parse_vacancies(session, base_url):
    search_url = f"{base_url}/jobs-python/?search=python&city=Київ"
    html = await fetch_html(session, search_url)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    jobs = []

    for job in soup.select("#pjax-job-list .job-link"):
        link = job.select_one("h2 a")
        if link and link.has_attr('href'):
            jobs.append(urljoin(base_url, link['href']))

    print(f"Знайдено {len(jobs)} вакансій на першій сторінці")
    return jobs


async def parse_skills(session, url):
    html = await fetch_html(session, url)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    skills = []

    # 1. Спроба знайти навички в описі вакансії
    description = soup.select_one(".card.wordwrap")
    if description:
        text = description.get_text(" ", strip=True)
        # Шукаємо ключові слова, пов'язані з Python
        python_skills = re.findall(
            r'(Django|Flask|FastAPI|SQL|PostgreSQL|MySQL|Git|Docker|Linux|AWS|OOP|REST|API|JavaScript|React)',
            text, re.IGNORECASE
        )
        skills.extend(skill.lower() for skill in python_skills)

    # 2. Спроба знайти блок "Вимоги" або "Навички"
    requirements = soup.select_one(".card-indent:-soup-contains('Вимоги')")
    if not requirements:
        requirements = soup.select_one(".card-indent:-soup-contains('Навички')")

    if requirements:
        items = requirements.find_next("ul")
        if items:
            for li in items.select("li"):
                skills.append(li.get_text(strip=True))

    # 3. Додаткові місця для пошуку навичок
    tags = soup.select(".tag")
    for tag in tags:
        skills.append(tag.get_text(strip=True))

    return list(set(skills))  # Видаляємо дублікати


async def run():
    base_url = "https://www.work.ua"

    async with ClientSession() as session:
        jobs = await parse_vacancies(session, base_url)
        jobs = jobs[:10]  # Обмежуємо кількість для тесту

        all_skills = []
        for job_url in jobs:
            print(f"Аналіз {job_url}")
            skills = await parse_skills(session, job_url)
            if skills:
                print(f"Знайдені навички: {skills}")
                all_skills.extend(skills)
            else:
                print(f"Навички не знайдені для {job_url}")

        if all_skills:
            return dict(Counter(all_skills))
        return {"Помилка": "Не вдалося знайти навички. Можливо, структура сайту змінилася."}


if __name__ == "__main__":
    result = asyncio.run(run())
    print("Результат:", result)