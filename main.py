from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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


service = Service(ChromeDriverManager().install())
driver: WebDriver = webdriver.Chrome(service = service)
driver.get("https://quotes.toscrape.com/js/")

ua = UserAgent()
headers = {'User-Agent': ua.random }
qout_list = []


next_btn = driver.find_element(By.CLASS_NAME, 'next').find_element(By.TAG_NAME, 'a').get_attribute('href')
#использовал только для личного удобства
pbar = tqdm()

while next_btn:
    pbar.update(1)
    qouts = driver.find_elements(By.CLASS_NAME, 'quote')
    for qout in qouts:
        #парсиг данных
        try:
            qoute_text = qout.find_element(By.CLASS_NAME, 'text').text
        except Exception:
            qoute_text = 'None'
        try:
            qoute_author = qout.find_element(By.CLASS_NAME, 'author').text
        except Exception:
            qoute_author = 'None'
        try:
            qoute_tags = qout.find_element(By.CLASS_NAME, 'tags').find_elements(By.CSS_SELECTOR, 'a')
            tags_text = [tag.text for tag in qoute_tags]
        except Exception:
            qoute_text = 'None'

        qout_list.append({
            'qoute_text': qoute_text,
            'qoute_author': qoute_author,
            'tags': tags_text
        })
    time.sleep(0.5)
    try:
        #не клик, потому что ширина высота кнопки равняется 0, кнопка не может быть нажата методом click()
        next_btn = driver.find_element(By.CLASS_NAME, 'next').find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.get(next_btn)
    except Exception:
        break

#запись сразу в два удобных формата
with open('all_qouts.json', 'w', encoding='utf-8') as file:
    json.dump(qout_list, file, indent=4, ensure_ascii=False)

with open('all_qouts.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['Text', 'Author', 'Теги'])
    for q in qout_list:
        tags_str = ', '.join(q['tags'])
        writer.writerow([q['qoute_text'], q['qoute_author'], tags_str])

#ожидание ввода, что бы драйвер браузера не закрывался сразу
input()