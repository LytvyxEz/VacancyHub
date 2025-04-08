import asyncio
import re
from collections import Counter
from playwright.async_api import async_playwright
import fastapi
import uvicorn
import sys


class WorkUaScraper:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    async def start_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

    async def stop_browser(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def get_links(self, search="python", location="Київ", max_links=10):
        await self.start_browser()

        await self.page.goto("https://www.work.ua/", wait_until="networkidle")
        await self.page.locator("#search").fill(search)
        await self.page.locator(".js-main-region").fill(location)
        await self.page.locator("#sm-but").click()
        await self.page.wait_for_load_state("networkidle")

        vacancies_text = await self.page.locator(".col-md-8 #pjax-job-list .mb-lg .mt-8 span").text_content()
        match = re.search(r"\d+", vacancies_text or "")
        if not match:
            print("Не вдалося отримати кількість вакансій.")
            await self.stop_browser()
            return []

        total_vacancies = int(match.group())
        print(f"Знайдено вакансій: {total_vacancies}")

        jobs = []
        while len(jobs) < min(total_vacancies, max_links):
            page_jobs = await self.page.locator("#pjax-job-list .job-link div h2 a").evaluate_all(
                "elements => elements.map(e => e.href)"
            )
            jobs.extend(page_jobs)

            next_button = self.page.locator("nav ul .add-left-default .link-icon .glyphicon-chevron-right")
            if await next_button.is_visible():
                await next_button.click()
                await self.page.wait_for_load_state("networkidle")
                await asyncio.sleep(1)
            else:
                break

        await self.stop_browser()
        return jobs[:max_links]

    async def get_skills_from_links(self, links):
        await self.start_browser()
        all_skills = []

        for link in links:
            try:
                await self.page.goto(link, wait_until="networkidle")
                skills = await self.page.locator(".mt-2xl .js-toggle-block li span").all_text_contents()
                all_skills.extend(skills)
            except Exception as e:
                print(f"Помилка на {link}: {e}")
                continue

        await self.stop_browser()
        return dict(Counter(all_skills))


scraper = WorkUaScraper()
app = fastapi.FastAPI()


@app.get("/scrape")
async def scrape_jobs():
    links = await scraper.get_links()
    skills = await scraper.get_skills_from_links(links)
    return {"links": links, "skills": skills}


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    uvicorn.run("your_module_name:app", host="0.0.0.0", port=8002, reload=False)
