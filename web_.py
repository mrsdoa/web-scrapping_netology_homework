import requests
from bs4 import BeautifulSoup
from fake_headers import Headers # импортировать
import pprint from pprint 
URL = 'https://habr.com/ru/all/'

# функция получения на каждый запрос новый заголовок
def get_headers():
    Headers(browser='firefox', os='win').generate()

# headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'}
# page = requests.get(URL, headers=headers)
# soup = BeautifulSoup(page.content, 'html.parser')
#
# # print(soup)
# 
# title_ = soup.find(class_='tm-articles-list').get_text()
# # product_price = soup.find(class_='ux-textspans ux-textspans--SECONDARY ux-textspans--BOLD').get_text()
# print(title_)


habr_main_html = requests.get(URL).text
soup = BeautifulSoup(habr_main_html, features='lxml')

article_list_tag = soup.find(class_='tm-articles-list') #нашли тег в которых лежат все статьи
article_tags = article_list_tag.find_all('article') # все статьи

# делаем список, в который будем складывать данные
articles = []

# делаем цикл с помощью которого будем ходить по статьям
for article in article_tags:
    article_time = article.find('time')['title']
    link_tag = article.find('a', class_='tm-article-snippet__title-link')
    link_relative = link_tag['href'] # ссылка тут относительная
    link = f'https://habr.com{link_relative}'
    span_tag = link_tag.find('span')
    title = span_tag.text # тут заголовок
    article_html = requests.get(link, headers=get_headers()).text # вытащи линк с этим заголовком
    article_body = BeautifulSoup(article_html, features='lxml').find(id='post-content-body').text # вытащи данные по ссылке, и найди айдишник
    articles.append({
        'time': article_time,
        'title': title,
        'body': article_body,
        'link': link
    })
print(article_list_tag)
