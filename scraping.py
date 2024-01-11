import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random


DOWNLOAD_PATH = "E:\Arxiv papers"
SITE = "arxiv.org"

def setup_chrome_driver(download_path):
    # Set up Chrome options
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize the Chrome driver with the options
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def find_my_site_link(article_name):
    query = f"{article_name} site:arxiv.org"
    google_url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(google_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if 'arxiv.org' in href:
            return href

    return None


def find_my_site_link_bing(article_name, site):
    query = f"{article_name} site:{site}"
    bing_url = f"https://www.bing.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(bing_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if site in href:
            return href

    return None

def find_my_site_link_duckduckgo(article_name, site):
    query = f"{article_name} site:{site}"
    duckduckgo_url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(duckduckgo_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a', class_='result__a'):
        href = link.get('href')
        if site in href:
            return href

    return None

def download_article_source(article_name, download_path=DOWNLOAD_PATH, site=SITE):
    article_url = find_my_site_link_duckduckgo(article_name, site)

    if not article_url:
        print("Article not found on the site.")
        return

    driver = setup_chrome_driver(download_path)
    driver.get(article_url)

    # Click on "Other formats"
    other_formats_button = driver.find_element(By.LINK_TEXT, "Other Formats")
    other_formats_button.click()

    # Wait for the page to load
    time.sleep(random.randint(3, 5))

    # Click on "Download source"
    download_button = driver.find_element(By.LINK_TEXT, "Download source")
    download_button.click()

    # Close the browser
    time.sleep(random.randint(5, 10))
    driver.quit()


# Example usage
article_name = "Towards Reasoning in Large Language Models: A Survey"
download_article_source(article_name, DOWNLOAD_PATH, SITE)
