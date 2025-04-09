import asyncio
import datetime
import re
import time
import random
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WorkUaScraper:
    def __init__(self):
        self.driver = None

    def _start_driver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # Якщо хочеш без вікна — залиш
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # User-Agent
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    async def get_links(self, search="python", location="Вся Україна"):
        return await asyncio.to_thread(self._get_links_sync, search, location)

    def _get_links_sync(self, search, location):
        self.driver = self._start_driver()
        wait = WebDriverWait(self.driver, 10)

        self.driver.get("https://www.work.ua/")
        time.sleep(random.uniform(1, 2))  # затримка

        search_input = wait.until(EC.presence_of_element_located((By.ID, "search")))
        search_input.clear()
        search_input.send_keys(search)
        time.sleep(random.uniform(0.5, 1.5))

        location_input = self.driver.find_element(By.CLASS_NAME, "js-main-region")
        location_input.clear()
        location_input.send_keys(location)
        time.sleep(random.uniform(1, 2))

        self.driver.find_element(By.ID, "sm-but").click()

        wait.until(EC.presence_of_element_located((By.ID, "pjax-job-list")))
        time.sleep(random.uniform(1, 2))

        try:
            vacancies_text = self.driver.find_element(By.CSS_SELECTOR,
                                                      ".col-md-8 #pjax-job-list .mb-lg .mt-8 span").text
            total_vacancies = int(re.search(r"\d+", vacancies_text).group())
        except Exception:
            self.driver.quit()
            return []

        job_links = []
        visited_links = set()
        max_pages = 100
        current_page = 0

        while len(job_links) < total_vacancies and current_page < max_pages:
            current_page += 1
            time.sleep(random.uniform(1, 2))  # пауза

            job_anchors = self.driver.find_elements(By.CSS_SELECTOR, "#pjax-job-list .job-link div h2 a")
            for a in job_anchors:
                href = a.get_attribute("href")
                if href and href not in visited_links:
                    job_links.append(href)
                    visited_links.add(href)

            try:
                # Симуляція прокрутки сторінки
                self.driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(random.uniform(0.5, 1.5))

                next_button = self.driver.find_element(By.CSS_SELECTOR,
                                                       "nav ul .add-left-default .link-icon .glyphicon-chevron-right")
                if not next_button.is_enabled():
                    break
                self.driver.execute_script("arguments[0].click();", next_button)
                wait.until(EC.presence_of_element_located((By.ID, "pjax-job-list")))
            except Exception as e:
                print(f"Pagination ended or error: {e}")
                break

        self.driver.quit()
        return job_links

    async def get_skills_from_links(self, links):
        return await asyncio.to_thread(self._get_skills_sync, links)

    def _get_skills_sync(self, links):
        self.driver = self._start_driver()
        wait = WebDriverWait(self.driver, 5)
        all_skills = []

        for link in links:
            try:
                self.driver.get(link)
                time.sleep(random.uniform(1, 2))  # пауза
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mt-2xl .js-toggle-block li span")))
                skill_elements = self.driver.find_elements(By.CSS_SELECTOR, ".mt-2xl .js-toggle-block li span")
                if not skill_elements:
                    print('no skills')

                all_skills.extend([el.text for el in skill_elements if el.text])
            except Exception as e:
                print(f"error on link: {link}")
                continue

        self.driver.quit()
        return dict(Counter(all_skills))


async def main():
    scraper = WorkUaScraper()
    links = await scraper.get_links("Python", "Київ")
    print(f"Found {len(links)} links")

    if links:
        skills = await scraper.get_skills_from_links(links)
        print("Top Skills:", skills)


asyncio.run(main())
