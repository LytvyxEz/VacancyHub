import asyncio
import sys
from playwright.async_api import async_playwright
import re
from collections import Counter


async def get_links(page):
    jobs = await page.locator("#pjax-job-list .job-link div h2 a").evaluate_all("elements => elements.map(e => e.href)")
    return jobs


async def run():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.work.ua/", wait_until="networkidle")
        await page.locator("#search").fill("python")
        await page.locator(".js-main-region").fill("Київ")
        await page.locator("#sm-but").click()
        await page.wait_for_load_state("networkidle")

        vacancies_text = await page.locator(".col-md-8 #pjax-job-list .mb-lg .mt-8 span").text_content()
        match = re.search(r"\d+", vacancies_text or "")
        if not match:
            print("Не вдалося отримати кількість вакансій.")
            return []

        total_vacancies = int(match.group())
        print(f"Знайдено вакансій: {total_vacancies}")

        jobs = []
        while len(jobs) < min(total_vacancies, 10):
            page_jobs = await get_links(page)
            jobs.extend(page_jobs)

            next_button = page.locator("nav ul .add-left-default .link-icon .glyphicon-chevron-right")
            if await next_button.is_visible():
                await next_button.click()
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(1)
            else:
                break

        await browser.close()
        return jobs


async def get_info(list_links):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        all_skills = []

        for link in list_links[:10]:  # Обмежуємо кількість для тесту
            try:
                await page.goto(link, wait_until="networkidle")
                skills = await page.locator(".mt-2xl .js-toggle-block li span").all_text_contents()
                all_skills.extend(skills)
            except Exception as e:
                print(f"Помилка на {link}: {e}")
                continue

        await browser.close()
        return dict(Counter(all_skills))


if __name__ == "__main__":
    # Для тестування окремо
    links = asyncio.run(run())
    skills_data = asyncio.run(get_info(links))
    print(skills_data)