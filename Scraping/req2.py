from bs4 import BeautifulSoup
import requests
import lxml
url = "https://parsinger.ru/html/index1_page_1.html"
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text,"lxml")
div = soup.find_all("p","price")
s = []
for txt in div:
    txt = txt.text
    txt = txt.replace(" руб","")

    s.append(txt)

num = list(map(int,s))
print(sum(num))


















