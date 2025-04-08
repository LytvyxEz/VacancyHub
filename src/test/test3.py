import asyncio
import re
from collections import Counter
from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from fastapi import FastAPI


app = FastAPI()


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


async def get_links(driver) -> List[str]:
    job_elements = driver.find_elements(By.CSS_SELECTOR, "#pjax-job-list .job-link div h2 a")
    return [job.get_attribute("href") for job in job_elements]


async def scrape_vacancies() -> List[str]:
    driver = await get_driver()

    try:
        driver.get("https://www.work.ua/")

        search = driver.find_element(By.ID, "search")
        search.send_keys("python")

        region = driver.find_element(By.CSS_SELECTOR, ".js-main-region")
        region.clear()
        region.send_keys("")

        submit = driver.find_element(By.ID, "sm-but")
        submit.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#pjax-job-list"))
        )

        vacancies_text = driver.find_element(
            By.CSS_SELECTOR, ".col-md-8 #pjax-job-list .mb-lg .mt-8 span"
        ).text
        match = re.search(r"\d+", vacancies_text)
        total_vacancies = int(match.group()) if match else 0
        print(f"Found vacancies: {total_vacancies}")

        jobs = []
        while len(jobs) < total_vacancies:
            page_jobs = await get_links(driver)
            jobs.extend(page_jobs)

            try:
                next_button = driver.find_element(
                    By.CSS_SELECTOR,
                    "nav ul .add-left-default .link-icon .glyphicon-chevron-right"
                )
                next_button.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#pjax-job-list"))
                )
                await asyncio.sleep(1)
            except:
                break

        return jobs  # Return max 10 jobs

    finally:
        driver.quit()


async def scrape_skills(links: List[str]) -> Dict[str, int]:
    driver = await get_driver()
    all_skills = []

    try:
        for link in links:
            try:
                driver.get(link)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".mt-2xl .js-toggle-block"))
                )

                skill_elements = driver.find_elements(
                    By.CSS_SELECTOR, ".mt-2xl .js-toggle-block li span"
                )
                skills = [skill.text for skill in skill_elements]
                all_skills.extend(skills)
            except Exception as e:
                continue

        return dict(Counter(all_skills))

    finally:
        driver.quit()




async def get_skills():
    links = await scrape_vacancies()
    skills = await scrape_skills(links)
    for a, b in skills.items():
        print(a, b)
    return skills



if __name__ == '__main__':
    asyncio.run(get_skills())
