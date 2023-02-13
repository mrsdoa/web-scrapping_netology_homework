import html

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

HOST = 'https://habr.com/ru/all/'
headers = Headers(browse='firefox', os='win').generate()
# определяем список ключевых слов
KEYWORDS = ['Microsoft', 'Яндекс', 'интеграция', 'python']

# Ваш код - <дата> - <заголовок> - <ссылка>.

# html = requests.get(HOST).text
# soup = BeautifulSoup(html, features="lxml")
# text_ = soup.find(class_="tm-article-snippet__title tm-article-snippet__title_h2")
# span_ = text_.find('span')
# text_word1 = span_.text
# print(text_word1)

habr_main_html = requests.get(HOST).text
soup = BeautifulSoup(habr_main_html)
article_list_tag = soup.find(class_="tm-articles-list")
articles_tags = article_list_tag.find_all('article') #ищем теги артикл=списки статей
for article in articles_tags:
    article_time = article.find('time')
    link_tag = article.find('a', class_='tm-article-snippet__title-link') # заголовок ищем

