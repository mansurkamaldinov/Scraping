import requests
from bs4 import BeautifulSoup
import lxml


s = []
s1 = []
index_labels = {1: "watch", 2: "mobile", 3: "mouse", 4: "hdd", 5: "headphones"}
for i in range(5):
    for j in range(32):
        url = f"https://parsinger.ru/html/{index_labels[i+1]}/{i+1}/{i+1}_{j+1}.html"
        response = requests.get(url=url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text,"lxml")
        div = soup.find_all("span",id="price")
        div2 = soup.find_all("span",id="in_stock")
        for txt in div:
            txt = txt.text
            txt = txt.replace(" руб","")
            s.append(txt)
        for txt2 in div2:
            txt2 = txt2.text
            txt2 = txt2.replace("В наличии:","")
            s1.append(txt2)
num = list(map(int,s))
num1 = list(map(int,s1))

ab = []
for k in range(0,len(num)):
     ab.append(num[k]*num1[k])
print(sum(ab))


