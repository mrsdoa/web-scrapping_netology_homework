import requests
from bs4 import BeautifulSoup

# в описании вакансии "Django" и "Flask"
def search(key1, key2):
    url = f'https://spb.hh.ru/search/vacancy?text={key1}%2C+{key2}&salary=&area=1&area=2&ored_clusters=true'
    # f'https://spb.hh.ru/search/vacancy?text=django%2C+flask&salary=&area=1&area=2&ored_clusters=true'
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    vacancies = soup.findAll('div', class_='serp-item')
    # print(len(vacancies))
    data = []

    for vacancy in vacancies:
        link = vacancy.find('a', class_='serp-item__title').get('href')
        position = vacancy.find('a', class_='serp-item__title').text
        try:
            salary = vacancy.find('span', class_='bloko-header-section-3').text.replace("\u202f", " ").replace("\xa0", " ")
        except:
            salary = 'нет информации по зп вилке'
        company_name = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace("\xa0", " ")
        location = vacancy.findAll('div', class_='bloko-text')[1].text.replace("\xa0", " ")

        data.append([link, position, salary, company_name, location])

    print(data)

if __name__=="__main__":
    search(key1='django', key2='flask')
