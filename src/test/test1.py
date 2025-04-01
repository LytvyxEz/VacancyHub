import plotly.express as px
import pandas as pd
from playwright.async_api import async_playwright
import asyncio
import re
import time
from collections import Counter


async def get_link(page):
    jobs = await page.locator("#pjax-job-list .job-link div h2 a").evaluate_all("elements => elements.map(e => e.href)")
    return jobs


async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.work.ua/")

        await page.locator("#search").fill("python")
        await page.locator(".js-main-region").fill(" ")

        await page.locator("#sm-but").click()
        await page.wait_for_load_state("networkidle")

        vacancies_text = await page.locator(".col-md-8 #pjax-job-list .mb-lg .mt-8 span").text_content()

        match = re.search(r"\d+", vacancies_text or "")
        if not match:
            print("Не вдалося отримати кількість вакансій.")
            return

        total_vacancies = int(match.group())
        print(f"Знайдено вакансій: {total_vacancies}")

        jobs = []
        while len(jobs) < total_vacancies:
            page_jobs = await get_link(page)
            jobs.extend(page_jobs)
            next_button = page.locator("nav ul .add-left-default .link-icon .glyphicon-chevron-right")

            print(await next_button.is_visible())
            if await next_button.is_visible():
                await next_button.click()
                await page.wait_for_load_state("networkidle")
                time.sleep(0.1)
            else:
                break


        print(jobs)
        return jobs


async def get_info(list_links):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        all_skill_list = []

        for link in list_links:
            await page.goto(link)
            skills = page.locator("div ul .label-skill span")
            if await skills.element_handles():
                skills_list = await skills.all_text_contents()
                all_skill_list.extend(skills_list)

        skill_counts = dict(Counter(all_skill_list))
        return skill_counts





