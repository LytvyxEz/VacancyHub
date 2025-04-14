import asyncio
import datetime
import re
import time
import random
from collections import Counter

import selenium
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
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")


        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    async def get_links(self, search: str, filters: dict):
        return await asyncio.to_thread(self._get_links_sync, search, filters)

    def _get_links_sync(self, search: str, filters: dict):
        location = filters['location'] if filters['location'] else 'Вся Україна'

        self.driver = self._start_driver()
        wait = WebDriverWait(self.driver, 5)

        self.driver.get("https://www.work.ua/")
        time.sleep(1)

        search_input = wait.until(EC.presence_of_element_located((By.ID, "search")))
        search_input.clear()
        search_input.send_keys(search)


        location_input = self.driver.find_element(By.CLASS_NAME, "js-main-region")
        location_input.clear()
        location_input.send_keys(location)
        self.driver.execute_script(f"document.querySelector('.js-main-region').value = '{location}';")


        time.sleep(1)

        self.driver.find_element(By.ID, "sm-but").click()

        wait.until(EC.presence_of_element_located((By.ID, "pjax-job-list")))
        time.sleep(1)

        try:
            vacancies_text = self.driver.find_element(By.CSS_SELECTOR,
                                                      ".col-md-8 #pjax-job-list .mb-lg .mt-8 span").text
            total_vacancies = int(re.search(r"\d+", vacancies_text).group())
        except Exception:
            self.driver.quit()
            return []

        job_links = []
        visited_links = set()
        max_pages = filters['max_pages'] if filters['max_pages'] else 20
        current_page = 0

        while len(job_links) < total_vacancies and current_page < max_pages:
            current_page += 1

            anchors = self.driver.find_elements(By.CSS_SELECTOR, "#pjax-job-list .job-link div h2 a")
            links = self.driver.execute_script("return arguments[0].map(el => el.href);", anchors)
            for href in links:
                if href and href not in visited_links:
                    job_links.append(href)
                    visited_links.add(href)

            try:
                self.driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(1)

                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR,
                                                           "nav ul .add-left-default .link-icon .glyphicon-chevron-right")

                except Exception as e:
                    print('button not found')
                    break

                self.driver.execute_script("arguments[0].click();", next_button)
                wait.until(EC.presence_of_element_located((By.ID, "pjax-job-list")))

            except Exception as e:
                print('error')
                break

        self.driver.quit()
        return job_links

    async def get_skills_from_links(self, links, filters):
        return await asyncio.to_thread(self._get_skills_sync, links, filters)

    def _get_skills_sync(self, links, filters):
        salary_filter = filters.get('salary', 0)
        experience_filter = filters.get('experience')

        # Convert experience if it's a digit string
        if experience_filter and experience_filter != "noexperience":
            match = re.search(r'\d+', experience_filter)
            if match:
                experience_filter = int(match.group())
            else:
                experience_filter = None

        print("experience_filter:", experience_filter)
        print("salary_filter:", salary_filter)

        self.driver = self._start_driver()
        wait = WebDriverWait(self.driver, 5)
        all_skills = []
        links_return = []

        for link in links:
            try:
                self.driver.get(link)

                # Wait and extract skills
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mt-2xl .js-toggle-block li span")))
                skill_elements = self.driver.find_elements(By.CSS_SELECTOR, ".mt-2xl .js-toggle-block li span")

                # Extract experience
                experience_elements = self.driver.find_elements(By.CSS_SELECTOR, ".wordwrap .list-unstyled li")
                experience_value = None
                for el in experience_elements:
                    if "Досвід роботи" in el.text:
                        match = re.search(r'\d+', el.text)
                        if match:
                            experience_value = int(match.group())
                            break

                # Extract salary
                salary_elements = self.driver.find_elements(By.CSS_SELECTOR,
                                                            ".wordwrap .list-unstyled .text-indent span")
                salary_value = None
                for el in salary_elements:
                    if "грн" in el.text:
                        cleaned = re.sub(r'[\s\u202f\u2009]', '', el.text)
                        numbers = re.findall(r'\d+', cleaned)
                        if numbers:
                            salary_value = int(numbers[0])
                            break

                # Filtering logic
                pass_salary = salary_value is None or salary_value >= salary_filter
                pass_experience = False

                if experience_filter is None:
                    pass_experience = True
                elif experience_filter == "noexperience" and (experience_value is None or experience_value == 0):
                    pass_experience = True
                elif isinstance(experience_filter, int) and experience_value is not None:
                    pass_experience = experience_value >= experience_filter

                if pass_salary and pass_experience:
                    all_skills.extend([el.text for el in skill_elements if el.text])
                    links_return.append(link)
                    print("Accepted:", link)

            except Exception as e:
                print(f"Error on link: {link} -> {e}")
                continue

        self.driver.quit()
        print("Collected skills:", all_skills)
        return dict(Counter(all_skills)), links_return

