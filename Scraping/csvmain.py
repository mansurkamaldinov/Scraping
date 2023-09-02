import requests
from bs4 import BeautifulSoup
import csv

header = ["Name", "Article", "Brand", "Model", "Availability", "Price", "Old Price", "Product Link"]


def pagination_index():
    host = "https://parsinger.ru/html/index1_page_1.html#1_1"
    response = requests.get(host)
    soup = BeautifulSoup(response.text, "lxml")
    pages = [x.text for x in soup.find("div", class_="nav_menu").find_all("a")]
    return len(pages)


def main(index):
    for i in range(0, index):
        for j in range(1, 33):
            sub = {1:"watch/1/1_",2:"mobile/2/2_",3:"mouse/3/3_",4:"hdd/4/4_",5:"headphones/5/5_"}
            url = "https://parsinger.ru/html/"+str(sub[i+1])+str(j)+".html"
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "lxml")

            name = [txt.text for txt in soup.find_all("p", id="p_header")]
            article = [txt.text.split(": ")[1] for txt in soup.find_all("p", class_="article")]
            brand = [txt.text.split(": ")[1] for txt in soup.find_all("li", id="brand")]
            model = [txt.text.split(": ")[1] for txt in soup.find_all("li", id="model")]
            availability = [txt.text.split(": ")[1] for txt in soup.find_all("span", id="in_stock")]
            price = [txt.text for txt in soup.find_all("span", id="price")]
            old_price = [txt.text for txt in soup.find_all("span", id="old_price")]
            product_link = [url for _ in range(len(name))]

            with open("res.csv", "a", encoding="utf-8-sig", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow([*name, *article, *brand, *model, *availability, *price, *old_price, *product_link])


with open("res.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(header)
index = pagination_index()
main(index)


