import csv
import requests
from bs4 import BeautifulSoup

with open('res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        'Наименование', 'Бренд', 'Форм-фактор', 'Ёмкость', 'Объём буф. памяти', 'Цена'])

url = 'https://parsinger.ru/html/index4_page_1.html'
response = requests.get(url=url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')
pagen = soup.find('div', class_='pagen').find_all('a')
list_link = []
shema = 'http://parsinger.ru/html/'
for link in pagen:
    list_link.append(f"{shema}{link['href']}")
res_list=[]

for i in range(len(list_link)):
    url = list_link[i]
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    name = [x.text.strip() for x in soup.find_all('a', class_='name_item')]
    description = [x.text.split('\n') for x in soup.find_all('div', class_='description')]
    description = [x[1:-1] for x in description]
    price = [x.text for x in soup.find_all('p', class_='price')]

    for i in range(len(description)):
        for j in range(len(description[i])):
            description[i][j]=description[i][j].split(":")[-1].strip()

    for item, price, descr in zip(name, price, description):
        res_list.append([item, *descr, price])

with open('res.csv', 'a', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    for i in range(len(res_list)):
        writer.writerow(res_list[i])