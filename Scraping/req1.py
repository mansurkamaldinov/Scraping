import requests
from bs4 import BeautifulSoup
import lxml
url = "https://parsinger.ru/html/hdd/4/4_1.html"
response = requests.get(url)
response.encoding = "utf=8"
soup = BeautifulSoup(response.text,"lxml")
div = soup.find("span",id="price")
div2 = soup.find("span",id="old_price")
for txt in div:
    txt = txt.text
for txt1 in div2:
    txt1 = txt1.text
rep = txt.replace(" руб","")
rep2 = txt1.replace(" руб","")
num = int(rep)
num1 = int(rep2)
res = (num1-num)*100/num1
print(res)






