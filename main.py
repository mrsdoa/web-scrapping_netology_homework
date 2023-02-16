import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json
from pprint import pprint

# URL = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page=1'

# функция получения на каждый запрос новый заголовок
def get_links(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(url=f"https://spb.hh.ru/search/vacancy?text={text}&area=1&area=2&page=1", headers={"user-agent":ua.random})
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:    
        page_count = int(soup.find('div',attrs={"class":"pager"}).find_all("span", recursive=False)[-1].find('a').find("span").text)
    except:
        return
    for page in range(page_count):
        try:
            data = requests.get(url=f"https://spb.hh.ru/search/vacancy?text={text}&area=1&area=2&page={page}", headers={"user-agent":ua.random})
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, 'lxml')
            for a in soup.find_all('a', attrs={'class':'resume-search-item-name'}):
                yield f"https://hh.ru{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f"{e}")
        time.sleep(1)




def get_resume(link):
    ua = fake_useragent.UserAgent()
    data = requests.get(url=link,
    headers={'user-agent':ua.random})
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        name = soup.find(attrs={'class':"resume-block__title-text"}).text
    except: 
        name = ""
    try:
        salary = soup.find(attrs={'class':"resume-block__title-text_salary"}).text.replace("\u2009", "").replace("\xa0", " ")
    except: 
        salary = ""
    resume = {
        "name": name,
        "salary": salary
    }
    return resume



if __name__=="__main__":
    for a in get_links("python"):
        print(get_resume(a))
        time.sleep(1)
        
        
        
        
import requests
from bs4 import BeautifulSoup

# в описании вакансии "Django" и "Flask"

url = 'https://spb.hh.ru/search/vacancy?text=django%2C+flask&salary=&area=1&area=2&ored_clusters=true'

headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify)

article_list_tag = soup.find(class_='vacancy-serp-content') #or vacancy-serp__results
article_tags = article_list_tag.find_all('div', class_='serp-item')

# делаем список, в который будем складывать данные
articles = []

# ссылка, вилка зп, название компании, город
# делаем цикл с помощью которого будем ходить по статьям
for article in article_tags:
    link_tag = article.find('a', class_='bloko-button bloko-button_kind-primary bloko-button_scale-small')
    link_relative = link_tag['href']  # ссылка тут относительная
    link = f'https://spb.hh.ru/{link_relative}'
    salary_tag = article.find('div', class_='bloko-header-3')
    # span_salary = salary_tag.find('span', class_='bloko-header-section-3')
    company_name_tag = article.find('div', class_='vacancy-serp-item__meta-info-company')
    company_name = company_name_tag.find('href')
    # name = company_name.text
    location_tag = article.find('div', class_='bloko-text')
    articles.append({
        'link': link,
        # 'salary': span_salary,
        # 'company': name,
        'location': location_tag
    })
print(articles)
