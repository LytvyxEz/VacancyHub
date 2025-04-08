import asyncio
import re
from collections import Counter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome


async def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver


async def parse_vacancies(query: str = "python", limit: int = 10) -> list[str]:
    driver = await get_driver()
    try:
        driver.get("https://www.work.ua/")


        search_input = driver.find_element(By.ID, "search")
        search_input.clear()
        search_input.send_keys(query)

        submit_button = driver.find_element(By.ID, "sm-but")
        submit_button.click()


        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#pjax-job-list"))
        )


        vacancies = []
        while len(vacancies) < limit:
            job_elements = driver.find_elements(By.CSS_SELECTOR, "#pjax-job-list .job-link h2 a")
            vacancies.extend([job.get_attribute("href") for job in job_elements[:limit]])

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, ".pagination .glyphicon-chevron-right")
                next_button.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#pjax-job-list"))
                )
                await asyncio.sleep(1)
            except:
                break

        return vacancies[:limit]
    finally:
        driver.quit()


async def analyze_skills(vacancy_urls: list[str]) -> dict[str, int]:
    driver = await get_driver()
    skills_counter = Counter()

    try:
        for url in vacancy_urls:
            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".card.wordwrap"))
                )


                skill_elements = driver.find_elements(
                    By.CSS_SELECTOR, ".js-toggle-block li span, .card.wordwrap .text-indent"
                )
                skills = [el.text.strip() for el in skill_elements if el.text.strip()]
                skills_counter.update(skills)
            except Exception as e:
                continue

        return dict(skills_counter)
    finally:
        driver.quit()