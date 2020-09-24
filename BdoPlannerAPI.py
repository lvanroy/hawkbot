from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.firefox import GeckoDriverManager

from bs4 import BeautifulSoup

import re


def get_stats_from_planner(url):
    character_stats = dict()
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    wait = WebDriverWait(driver, 10)
    driver.get(url)

    wait.until(EC.url_changes(url))

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.close()

    values = soup.find_all("div", {"class": "stat-value"})
    labels = soup.find_all("div", {"class": "stat-label"})
    for i in range(len(values)):
        value = re.sub("[^0-9]", "", values[i].string)
        label = re.sub("[^A-Z]", "", labels[i].string)
        character_stats[label] = value

    values = soup.find_all("span", {"class": "value"})
    labels = soup.find_all("span", {"class": "label"})

    for i in range(len(values)):
        value = re.sub("[^0-9]", "", values[i].string)
        label = re.sub("[^A-Z]", "", labels[i].string)
        if label not in character_stats:
            character_stats[label] = value

    print(character_stats)

    return character_stats
