import requests
from bs4 import BeautifulSoup
import lxml
s = []
url = "https://parsinger.ru/table/5/index.html"
response = requests.get(url=url)
response.encoding="utf-8"
soup = BeautifulSoup(response.text,"lxml")
div = soup.find_all('td',"green")
for txt in div:
    txt = txt.text
    s.append(txt)
num = list(map(float,s))

print(sum(num))




