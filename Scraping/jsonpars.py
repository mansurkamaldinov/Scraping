import requests
from bs4 import BeautifulSoup
import json

for i in range(1,5):
    url = 'https://parsinger.ru/html/index3_page_'+str(i)+'.html'
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    name = [x.text.strip() for x in soup.find_all('a', class_='name_item')]
    description = [x.text.strip().split('\n') for x in soup.find_all('div', class_='description')]
    price = [x.text for x in soup.find_all('p', class_='price')]


    result_json = []

    for list_item, price_item, name in zip(description, price, name):
        result_json.append({
            'name': name,
            'brand': [x.split(':')[1] for x in list_item][0],
            'type': [x.split(':')[1] for x in list_item][1],
            'connect': [x.split(':')[1] for x in list_item][2],
            'game': [x.split(':')[1] for x in list_item][3],
            'price': price_item

            })
        print(name)

    with open('res.json', 'w', encoding='utf-8') as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)