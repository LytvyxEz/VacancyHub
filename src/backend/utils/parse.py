import sys
import os
from collections import Counter
from playwright.async_api import async_playwright
import asyncio
import re

# Prevent Python from finding your token.py in the local directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

async def get_links(page):
    jobs = await page.locator("#pjax-job-list .job-link div h2 a").evaluate_all(
        "elements => elements.map(e => e.href)"
    )
    return jobs

async def scrape_workua():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.work.ua/", timeout=15000)
        await page.locator("#search").fill("python")
        await page.locator(".js-main-region").fill(" ")
        await page.locator("#sm-but").click()
        await page.wait_for_load_state("networkidle")

        vacancies_text = await page.locator(
            ".col-md-8 #pjax-job-list .mb-lg .mt-8 span"
        ).text_content()
        match = re.search(r"\d+", vacancies_text or "")
        total_vacancies = int(match.group()) if match else 0
        print(f"Found vacancies: {total_vacancies}")

        jobs = []
        while len(jobs) < min(total_vacancies, 100):  # Limit for testing
            page_jobs = await get_links(page)
            jobs.extend(page_jobs)

            next_button = page.locator(
                "nav ul .add-left-default .link-icon .glyphicon-chevron-right"
            )
            if await next_button.is_visible():
                await next_button.click()
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(0.5)
            else:
                break

        return jobs

async def main():
    jobs = await scrape_workua()
    print(f"Collected {len(jobs)} job links")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())