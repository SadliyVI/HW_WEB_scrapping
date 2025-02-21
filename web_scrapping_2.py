import requests
from bs4 import BeautifulSoup
import time
from pprint import pprint
import bs4
from fake_headers import Headers
import json
from tqdm import tqdm

KEY_WORDS = ['дизайн', 'фото', 'web', 'python']

# def check_word_in_list(word, word_list):
#     return any(word.lower() in item.lower() for item in word_list)
#
# def find_matching_words(source_list, target_list):
#     return any(check_word_in_list(word, target_list) for word in source_list)

# Заменить на одну функцию использующую set()
def find_matching_words(source_list, target_list):
    return any(word.lower() in target_list for word in source_list)

def write_result_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii = False, indent = 4)
        print(f'Данные успешно записаны в файл {filename}')
    except IOError as e:
        print(f'Ошибка при записи в файл: {e}')
    except Exception as e:
        print(f'Произошла неожиданная ошибка: {e}')


def fetch_with_retry(url, headers, timeout=10, max_retries=3, retry_delay=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout, headers=headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            print(f"Попытка {attempt + 1} не удалась: {e}")
            if attempt < max_retries - 1:
                print(f'Повторная попытка через {retry_delay} секунд...')
                time.sleep(retry_delay)
            else:
                print(
                    'Достигнуто максимальное количество попыток. Запрос не удался.')
                return None

def get_article_text(article_link, headers):
    soup = fetch_with_retry (article_link, headers)
    try:
        article_preview = soup.select_one('div.article-formatted-body')
        text =''
        if article_preview:
            articles_text = article_preview.get_text().strip('')
            articles_text = articles_text.replace('\xa0', '')
    except Exception as e:
        print(f'Ошибка при загрузке превью статей: {e}\nПовторите запрос!')
    return articles_text

headers = Headers(browser='chrome', os='win').generate()
url = 'https://habr.com/ru/articles'
soup = fetch_with_retry(url, headers)
if soup is None: # Добавлено по замечаниям преподавателя
    print('Ошибка: Не удалось загрузить главную страницу!')
    exit()
else:
    articles_tag = soup.find_all('article')
    parsed_data = []
    for article in tqdm(articles_tag, desc='Обработка статей', unit='статью'):
        time.sleep(2)
        word_set = []
        article_title_word = article.h2.text.split()
        article_hubs = article.find_all('span', class_ =
                                        'tm-publication-hub__link-container')
        hubs_word = []
        for hub in article_hubs:
            hubs_word.extend(hub.text.strip('*').split())
        artical_body_words = []

        # Изменено по замечаниям# преподавателя
        article_link_element = article.select_one('a.tm-title__link')
        article_link = 'https://habr.com' + article_link_element[
            'href'] if article_link_element else 'Нет ссылки'
        # article_link = 'https://habr.com' + article.select_one(
        #                'a.tm-article-datetime-published.tm-article-datetime'
        #                '-published_link')['href']

        # Изменено по замечаниям# преподавателя
        article_text = get_article_text(article_link, headers)
        article_text = article_text.replace('\xa0', '')
        artical_body_words = article_text.split()

        # word_set.extend(article_title_word)
        # word_set.extend(hubs_word)
        # word_set.extend(artical_body_words)
        # word_set = set(word_set)
        word_set = set(article_title_word + hubs_word + artical_body_words)
        word_set = list(word_set)

        result = find_matching_words(KEY_WORDS, word_set)
        if result:
            parsed_data.append({
                'time': article.select_one('time')['datetime'],
                'title': article.h2.text,
                'link': article_link})

write_result_to_json(parsed_data,'parsed_data_2.json')
pprint(parsed_data)

