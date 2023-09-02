from bs4 import BeautifulSoup
import requests

result_list = []
for i in range(1, 5):
    url = f'http://parsinger.ru/html/index3_page_{i}.html'
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    result_list.append([txt.text for txt in soup.find_all('a', class_='name_item')])

print(result_list)











