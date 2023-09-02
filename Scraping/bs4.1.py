import requests
from bs4 import BeautifulSoup
import lxml
s = []

for i in range(4):

    url = "https://parsinger.ru/html/mouse/3/3_"+str(i)+".html"
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text,"lxml")
    div = soup.find_all("p","article")
    for txt in div:
        s.append(txt.text)

print(s)


