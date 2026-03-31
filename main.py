from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv
import requests
import json
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import urljoin
from tqdm import tqdm



# задачи
# с каждой цитаты собрать:
# 1. Текст цитаты
# 2. Автор
# 3. Теги
# 4. сохранение в csv 
# 5. обработку ошибок


driver: WebDriver = webdriver.Chrome()
driver.get("https://quotes.toscrape.com/js/")

ua = UserAgent()
headers = {'User-Agent': ua.random }
qout_list = {}


next_btn = driver.find_element(By.CLASS_NAME, 'next').find_element(By.TAG_NAME, 'a').get_attribute('href')


while next_btn[:1]:

    qouts = driver.find_elements(By.CLASS_NAME, 'quote')
    for qout in qouts:
        try:
            qoute_text = driver.find_element(By.CLASS_NAME, 'text').text
        except Exception:
            qoute_text = 'None'
        
        try:
            qoute_author = driver.find_element(By.CLASS_NAME, 'author').text
        except Exception:
            qoute_text = 'None'

        try:
            qoute_tags = driver.find_element(By.CLASS_NAME, 'text').text
        except Exception:
            qoute_text = 'None'

    time.sleep(0.5)
    next_btn = driver.find_element(By.CLASS_NAME, 'next').find_element(By.TAG_NAME, 'a').get_attribute('href')
    driver.get(next_btn)

input()