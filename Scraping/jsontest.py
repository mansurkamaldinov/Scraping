import json
import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url)
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "lxml")


url = "https://parsinger.ru/html/index3_page_1.html"
schema = "https://parsinger.ru/html/"
soup = get_soup(url)
categories = [f'{schema}{a["href"]}' for a
              in soup.find(class_="nav_menu").find_all("a")]

pages = []
for category in categories:
    soup = get_soup(url=category)
    pages.extend(
        [f'{schema}{a["href"]}' for a
         in soup.find(class_="pagen").find_all("a")])

cards = []
for page in pages:
    soup = get_soup(url=page)
    cards.extend(
        [f'{schema}{a["href"]}' for a in soup.find_all(class_="name_item")])

result_json = []
for card in cards:
    soup = get_soup(url=card)
    data = {
        "categories": card.split("/")[-3],
        "name": soup.find("p", id="p_header").text,
        "article": soup.find("p", class_="article").text.split(":")[-1].strip(),
        "description": {li["id"]: "".join(li.text.split(":")[1:]).strip() for li
                        in soup.find("ul", id="description").find_all("li")},
        "count": soup.find("span", id="in_stock").text.split(":")[-1].strip(),
        "price": soup.find("span", id="price").text,
        "old_price": soup.find("span", id="old_price").text,
        "link": card

    }
    result_json.append(data)

with open('4_9_4.json', 'w', encoding='utf-8') as file:
    json.dump(result_json, file, indent=4, ensure_ascii=False)







