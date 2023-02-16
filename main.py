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