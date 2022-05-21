import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
from os import path
import os.path
import lxml
import time

start_time = time.time()
session = HTMLSession()
finish = []


def start_selenium(url):
    # Settings of webdriver
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    try:
        driver.title
    except:
        print("The incorrect link")
        exit(0)
    driver.get(url
               )
    return driver


def take_information_from_page(page):
    try:
        soup = BeautifulSoup(page, "lxml")
        # All vacancy_cards cards
        vacancy_cards = soup.find_all('span', class_="g-user-content")
        links = []
        for vacancy in vacancy_cards:
            # Taking a link for a vacancy
            link = vacancy.find('a', class_="bloko-link").get("href")
            links.append(link)

        for link in links:
            request = session.get(link)
            soup = BeautifulSoup(request.content, "lxml")
            experience = soup.find('div', class_="vacancy-description").find_all('span')[0].text
            time_work = soup.find('div', class_="vacancy-description").find_all('span')[1].text
            name = soup.find('h1', class_="bloko-header-1").text
            finish.append({'name': name,
                           'experience': experience,
                           'time_work': time_work,
                           'link': link,
                           })
    except:
        return


def parsed_all_pages(driver):
    page = 0
    while True:
        print(f'Current parsed page : {page}')
        page_sources = driver.page_source
        take_information_from_page(page_sources)
        page += 1
        try:
            buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "pager"))
            )
            # Press the button "the next page"
            buttons.find_element(By.LINK_TEXT, "дальше").click()
        except:
            return


print("Enter the url: \n")
url = input()
driver = start_selenium(url)
parsed_all_pages(driver)
if path.exists('Parsed_Data.csv'):
    if path.exists('Previous_Parsed_Data.csv'):
        os.remove('Previous_Parsed_Data.csv')
    os.rename('Parsed_Data.csv', 'Previous_Parsed_Data.csv')
q = pd.DataFrame(finish)
q.to_csv('Parsed_Data.csv', index=False)
print(f'time = {time.time() - start_time}')
driver.close()
driver.quit()
