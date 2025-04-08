import asyncio
import re
from collections import Counter
from playwright.async_api import async_playwright
import sys



class WorkUaScraper:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

        if sys.platform.startswith("win") and sys.version_info >= (3, 8):
            import asyncio

            try:
                from asyncio import (
                    WindowsProactorEventLoopPolicy,
                    WindowsSelectorEventLoopPolicy,
                )
            except ImportError:
                pass
                # not affected
            else:
                if type(asyncio.get_event_loop_policy()) is WindowsProactorEventLoopPolicy:
                    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
                    print(f'do not change to Selector Event Loop')

    # async def start_browser(self):
    #     self.playwright = await async_playwright().start()
    #     self.browser = await self.playwright.chromium.launch(headless=True)
    #     self.page = await self.browser.new_page()
    #
    # async def stop_browser(self):
    #     if self.browser:
    #         await self.browser.close()
    #     if self.playwright:
    #         await self.playwright.stop()

    async def get_links(self, search="python", location="Вся Україна"):

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()



            await browser.page.goto("https://www.work.ua/", wait_until="networkidle")
            await browser.page.locator("#search").fill(search)
            await browser.page.locator(".js-main-region").fill(location)
            await browser.page.locator("#sm-but").click()
            await browser.page.wait_for_load_state("networkidle")

            vacancies_text = await browser.page.locator(".col-md-8 #pjax-job-list .mb-lg .mt-8 span").text_content()
            match = re.search(r"\d+", vacancies_text or "")
            if not match:
                await self.stop_browser()
                return []

            total_vacancies = int(match.group())
            jobs = []

            while len(jobs) < total_vacancies:
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

                await context.close()
                return jobs

    async def get_skills_from_links(self, links):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            all_skills = []

            for link in links:
                try:
                    await self.page.goto(link, wait_until="networkidle")
                    skills = await self.page.locator(".mt-2xl .js-toggle-block li span").all_text_contents()
                    all_skills.extend(skills)
                except Exception as e:
                    print(f"Error parsing {link}: {e}")
                    continue

            await context.close()

            return dict(Counter(all_skills))