import requests
from bs4 import BeautifulSoup
import time
from pprint import pprint
from webbrowser import Chrome

from selenium.common import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions



import re
import bs4
from fake_headers import Headers
import json



KEY_WORDS = ['дизайн', 'фото', 'web', 'python']




# Selenium
# pip install selenium
# pip install webdriver-manager

def wait_element(browser, delay = 3, by=By.TAG_NAME, value = None):
    try:
        return WebDriverWait(browser, delay).until(
            expected_conditions.presence_of_element_located((by, value)))
    except TimeoutException:
        print(f'Element not found after {delay} seconds')
        return None



# chrome_path = ChromeDriverManager().install()
# service = Service(executible_path=chrome_path)
# browser = Chrome(service=service)
# options = ChromeOptions()
# options.add_argument('--headless')
# # browser = Chrome(service=service, options=options)
# # time.sleep(5)
# browser.get('https://dtf.ru/games')
# time.sleep(1)

# Поиск элементов
# раньше в БС было так articles_list = soup.select('div.content--short')

# articles_list = browser.find_elements(by=By.CSS_SELECTOR, value='div.content--short')
# print(len(articles_list))
#
# links = []
# for article in articles_list:
#     link = wait_element(browser=article, by=By.CSS_SELECTOR,
#                         value='a.content__link').get_attribute('href')
#     # print(link)
#     links.append(link)
#
# parsed_data = []
# for link in links:
#     # print(link)
#     # response = requests.get(link)
#     browser.get(link)
#     # soup = bs4.BeautifulSoup(response.text, features='lxml')
#     # title = soup.select_one('h1').text.strip()
#     # print(title)
#     article_title = wait_element(browser=browser, by=By.TAG_NAME,
#                                  value='h1').text.strip()
#
#     # time = soup.select_one('time')['datetime']
#     # print(time)
#     article_time = wait_element(browser=browser, by=By.TAG_NAME,
#                                 value='time').get_attribute('datetime')
#
#     # articles_text = soup.select_one(
#     #     'article.content__blocks').text.strip()
#     article_text = wait_element(browser=browser, by=By.CSS_SELECTOR,
#                                 value='article.content__blocks').text
#
#     # print(articles_text)
#     parsed_data.append({
#         'link': link,
#         'time': article_time,
#         'title': article_title,
#         'text': article_text})
#     # pprint(parsed_data)
#     print(article_title)
#     with open('article_2.json', 'w', encoding='utf-8') as f:
#         f.write(json.dumps(parsed_data, ensure_ascii=False, indent=4))
#
# search = wait_element(browser=browser, by=By.CSS_SELECTOR,
#                       value='button.search__button')
# search.click()
# time.sleep(3)
#
# search_field = wait_element(browser=browser, by=By.CSS_SELECTOR,
#                             value='input.text-input')
# search_field.send_keys('fallout')
# search_field.send_keys(Keys.ENTER)
# time.sleep(10)
def get_article_text(article_link):
    response = requests.get(article_link)
    pprint(response.text)
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    articles_text = soup.select_one(
        'article.tm-article-presenter_content').text
    return articles_text

# response = requests.get('https://habr.com/ru/articles')
# # print(response.text)
#
# soup = bs4.BeautifulSoup(response.text, features='lxml')
# articles_list = soup.select('h2.tm-title')
# # print(len(articles_list))
# # pprint(articles_list)
# parsed_data = []
# for article in articles_list:
#     article_title = article.select_one('span').text
#     # print(article_title)
#     if any(word.lower() in article_title for word in KEY_WORDS):
#         article_time = soup.select_one('time')['datetime']
#         # print(time)
#
#
#         article_link = 'https://habr.com' + article.select_one(
#                        'a.tm-title__link')['href']
#         text = get_article_text('https://habr.com/ru/companies/kts/articles/882078/')
#         print(text)
#         parsed_data.append({'time':article_time,'title':article_title, 'link': article_link})
#         # article_text =  articles_text = soup.select_one(
#         # 'article.content__blocks').text.strip()
# pprint(parsed_data)


    # articles_text = articles_soup.select_one('p')
#
#     # print(articles_text)
#     parsed_data.append({
#         'link': link,
#         'time': time,
#         'title': title,
#         'articles_text': articles_text})
#     pprint(parsed_data)
#     with open('article.json', 'w', encoding='utf-8') as f:
#         f.write(json.dumps(parsed_data, ensure_ascii=False, indent=4))

text = get_article_text('https://habr.com/ru/companies/kts/articles/882078/')
print(text)
#post-content-body > div > div > div > p:nth-child(3)