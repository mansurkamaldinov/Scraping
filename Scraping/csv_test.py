import requests
from bs4 import BeautifulSoup
import csv

import lxml

with open('res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["Наименование", "Артикул", "Бренд", "Модель", "Тип", "Технология экрана", "Материал корпуса",
                     "Материал браслета", "Размер", "Сайт производителя",
                     "Наличие", "Цена", "Старая цена", "Ссылка на карточку с товаром"])
for i in range(1,33):
    url = "https://parsinger.ru/html/watch/1/1_"+str(i)+".html"

    response = requests.get(url=url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text,"lxml")
    name = [txt.text for txt in soup.find("p",id="p_header")]
    artic = [txt.text.split()[1] for txt in soup.find("p",class_="article")]
    descr = [txt.text.split(": ")[1] for txt in soup.find("ul",id="description").find_all("li")]
    nalich = [txt.text for txt in soup.find("span",id="in_stock")]
    price = [txt.text for txt in soup.find("span",id="price")]
    olprice = [txt.text for txt in soup.find("span",id = "old_price")]
    ssylka = "https://parsinger.ru/html/watch/1/1_"+str(i)+".html"
    print(name)
    with open('res.csv', 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        writer.writerow([*name,*artic,*descr,*nalich,*price,*olprice,ssylka])




