import requests
from bs4 import BeautifulSoup

URL = 'https://habr.com/ru/all/'

headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup)
#
product_title = soup.find(class_='tm-articles-list').get_text()
# product_price = soup.find(class_='ux-textspans ux-textspans--SECONDARY ux-textspans--BOLD').get_text()
print(product_title)
# print(product_price)
articles_tags = article_list_tag.find_all('article') #ищем теги артикл=списки статей
for article in articles_tags:
    article_time = article.find('time')['title']
    link_tag = article.find('a', class_='tm-article-snippet__title-link')
    link = link_tag['href']
    span_tag = link_tag.find('span')
    title = span_tag.text
