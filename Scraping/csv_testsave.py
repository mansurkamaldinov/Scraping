import requests
from bs4 import BeautifulSoup
import csv
import lxml
from fake_useragent import UserAgent


def get_html_text(url: str) -> str:
    ua: UserAgent = UserAgent()
    headers: dict = {'user-agent': ua.random}
    responce: requests = requests.get(url, head'pers=headers)
    responce.encoding: str = 'utf-8'

    return responce.text
#

def get_name_products(get_title: str) -> list:
    soup: BeautifulSoup = BeautifulSoup(get_title, 'lxml')
    names: list = [
        name.text.strip() for name in soup.find_all('a', class_='name_item')
    ]

    return names


def get_description_products(get_title: str) -> list:
    soup: BeautifulSoup = BeautifulSoup(get_title, 'lxml')
    description: list = [
        description.text.split('\n')
        for description in soup.find_all('div', class_='description')
    ]

    return description


def get_price_product(get_title: str) -> list:
    soup: BeautifulSoup = BeautifulSoup(get_title, 'lxml')
    price: list = [x.text for x in soup.find_all('p', class_='price')]

    return price


def main():
    with open('res.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            'Наименование', 'Бренд', 'Форм-фактор', 'Ёмкость',
            'Объём буф. памяти', 'Цена'
        ])

    url = 'https://parsinger.ru/html/index4_page_1.html'
    title = get_html_text(url)
    name = get_name_products(title)
    description = get_description_products(title)
    price = get_price_product(title)

    for item, price, descr in zip(name, price, description):
        flatten = item, price, *[x.split(':')[1].strip() for x in descr if x]

        file = open('res.csv', 'a', encoding='utf-8-sig', newline='')
        writer = csv.writer(file, delimiter=';')
        writer.writerow(flatten)
    file.close()


if __name__ == '__main__':
    main()