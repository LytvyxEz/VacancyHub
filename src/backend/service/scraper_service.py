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
        # options.add_argument('--headless')
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
        salary = filters['salary'] if filters['salary'] else None

        experience = filters['experience'] if filters['experience'] else None
        if experience is not None and experience != "noexperience":
            match = re.search(r'\d+', experience)
            if match:
                experience = int(match.group())
            else:
                experience = None

        print("experience:", experience)

        self.driver = self._start_driver()
        wait = WebDriverWait(self.driver, 5)
        all_skills = []

        for link in links:
            try:
                self.driver.get(link)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mt-2xl .js-toggle-block li span")))
                skill_elements = self.driver.find_elements(By.CSS_SELECTOR, ".mt-2xl .js-toggle-block li span")

                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".wordwrap .list-unstyled li")))
                experience_elements = self.driver.find_elements(By.CSS_SELECTOR, ".wordwrap .list-unstyled li")
                for i in experience_elements:
                    if "Досвід роботи" in i.text:
                        print(i.text)
                        match = re.search(r'\d+', i.text)
                        if match:
                            experience_elements_num = int(match.group())
                            print(experience_elements_num)


                # salary_elements = self.driver.find_elements(By.CSS_SELECTOR, ".mt-2xl .js-toggle-block li span")

                if not skill_elements:
                    print('no skills')

                if not experience_elements:
                    print('no experience')

                if experience == None:
                    all_skills.extend([el.text for el in skill_elements if el.text])
                    print("ура: ", link)
                elif experience == "noexperience":
                    if experience == "noexperience":
                        all_skills.extend([el.text for el in skill_elements if el.text])
                        print("ура: ", link)
                elif isinstance(experience, int):
                    if experience_elements_num >= experience:
                        all_skills.extend([el.text for el in skill_elements if el.text])
                        print("ура: ", link)


            except Exception as e:
                print(f"error on link: {link}")
                continue

        self.driver.quit()
        print(all_skills)
        return dict(Counter(all_skills))



# async def main():
#     scraper = WorkUaScraper()
#     links = await scraper.get_links("Python", {'experience': '1-3', 'salary': 10000, 'location': None})
#     print(f"Found {len(links)} links")
#
#     if links:
#         skills = await scraper.get_skills_from_links(links)
#         print("Top Skills:", skills)
#
#
#

# asyncio.run(main())
