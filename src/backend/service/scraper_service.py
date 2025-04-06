import asyncio
from playwright.async_api import async_playwright
from collections import Counter
import re


class ScraperService:
    @staticmethod
    async def get_links(page, query: str):
        try:
            await page.goto("https://www.work.ua/", wait_until="networkidle")
            await page.locator("#search").fill(query)
            await page.locator("#sm-but").click()
            await page.wait_for_load_state("networkidle")

            # Отримуємо загальну кількість вакансій
            vacancies_text = await page.locator(".col-md-8 #pjax-job-list .mb-lg .mt-8 span").text_content()
            match = re.search(r"\d+", vacancies_text or "")
            total_vacancies = int(match.group()) if match else 0
            print(f"Знайдено вакансій: {total_vacancies}")

            # Збираємо всі посилання
            jobs = []
            while True:
                page_jobs = await page.locator("#pjax-job-list .job-link div h2 a").evaluate_all(
                    "elements => elements.map(e => e.href)"
                )
                jobs.extend(page_jobs)

                next_button = page.locator("nav ul .add-left-default .link-icon .glyphicon-chevron-right")
                if await next_button.is_visible():
                    await next_button.click()
                    await page.wait_for_load_state("networkidle")
                    await asyncio.sleep(1)
                else:
                    break

            return jobs[:total_vacancies]  # Повертаємо всі знайдені посилання

        except Exception as e:
            print(f"Помилка при отриманні посилань: {str(e)}")
            return []

    @staticmethod
    async def analyze_skills(links: list[str]):
        if not links:
            return {}

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            skills_counter = Counter()

            for link in links:
                try:
                    await page.goto(link, wait_until="networkidle", timeout=15000)
                    skills = await page.query_selector_all(
                        ".label-skill, .skill-tag, [class*='skill'] span, .job-description"
                    )

                    # Додаємо явні навички
                    skills_texts = [await skill.inner_text() for skill in skills]
                    skills_counter.update(
                        s.strip().lower() for s in skills_texts
                        if s.strip() and len(s.strip()) < 50  # Фільтр для виключення довгого тексту
                    )

                    # Аналіз опису вакансії на наявність ключових слів
                    description = await page.query_selector(".job-description")
                    if description:
                        description_text = (await description.inner_text()).lower()
                        common_skills = ["python", "django", "flask", "sql", "docker", "aws"]
                        for skill in common_skills:
                            if skill in description_text:
                                skills_counter[skill] += 1

                except Exception as e:
                    print(f"Помилка при парсингу {link}: {str(e)}")
                    continue

            await browser.close()
            return dict(skills_counter)