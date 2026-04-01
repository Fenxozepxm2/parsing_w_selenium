from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import json
from fake_useragent import UserAgent


# задачи
# с каждой цитаты собрать:
# 1. Текст цитаты
# 2. Автор
# 3. Теги
# 4. сохранение в csv 
# 5. обработку ошибок


def parsing_qoutes(driver: WebDriver):
    qout_list = []
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
             qoute_tags = 'None'

        qout_list.append({
                'qoute_text': qoute_text,
                'qoute_author': qoute_author,
                'tags': tags_text
            })
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'quote')))
    return qout_list


def go_next_page(driver: WebDriver):
    try:
        next_btn = driver.find_element(By.CLASS_NAME, 'next')
        link = next_btn.find_element(By.TAG_NAME, 'a')

        driver.execute_script('arguments[0].click();', link)

        return True
    except:
        return False


#запись сразу в два удобных формата
def saving_data(qout_list):
    with open('all_qouts.json', 'w', encoding='utf-8') as file:
        json.dump(qout_list, file, indent=4, ensure_ascii=False)

    with open('all_qouts.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Text', 'Author', 'Теги'])
        for q in qout_list:
            tags_str = ', '.join(q['tags'])
            writer.writerow([q['qoute_text'], q['qoute_author'], tags_str])

#ожидание ввода, что бы драйвер браузера не закрывался сразу
def main():
    service = Service(ChromeDriverManager().install())
    driver: WebDriver = webdriver.Chrome(service = service)
    driver.get("https://quotes.toscrape.com/js/")
    all_qoutes = []
    ua = UserAgent()
    headers = {'User-Agent': ua.random }

    while True:
        qout_list = parsing_qoutes(driver)
        all_qoutes.extend(qout_list)

        if not go_next_page(driver):
            break
    saving_data(all_qoutes)



if __name__ == '__main__':
    main()