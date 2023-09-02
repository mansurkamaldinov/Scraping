import requests
from bs4 import BeautifulSoup
import json
import lxml
index={1:"watch/1/1_",2:"mobile/2/2_",3:"mouse/3/3_",4:"hdd/4/4_",5:"headphones/5/5_"}
resultjs = []
for j in range(0,5):
    for i in range(1,33):
        url = "https://parsinger.ru/html/"+str(index[j+1])+str(i)+".html"

        response = requests.get(url)

        response.encoding="utf-8"

        soup = BeautifulSoup(response.text,"lxml")

        name = [txt.text for txt in soup.find_all("p",id="p_header")]
        artic = [txt.text.split(": ")[1] for txt in soup.find_all("p",class_="article")]
        descr = [txt.text.split(": ")[1] for txt in soup.find("ul",id="description").find_all("li")]
        stock = [txt.text.split(": ")[1] for txt in soup.find_all("span",id="in_stock")]
        price = [txt.text for txt in soup.find("div",class_="sale").find_all("span",id="price")]
        olprice = [txt.text for txt in soup.find("div",class_="sale").find_all("span",id="old_price")]
        descrip = [li["id"] for li in soup.find("ul",id ="description").find_all("li")]


        resultjs.append({
        "name":[x for x in name][0],
        "article":[x for x in artic][0],
        "description":{
            descrip[0]:[x for x in descr][0],
            descrip[1]:[x for x in descr][1],
            descrip[2]:[x for x in descr][2],
            descrip[3]: [x for x in descr][3],
            descrip[4]: [x for x in descr][4],
            descrip[5]: [x for x in descr][5],
            descrip[6]: [x for x in descr][6],
            descrip[7]: [x for x in descr][7]},
        "count":[x for x in stock][0],
        "price": [x for x in price][0],
        "old_price":[x for x in olprice][0],
        "link":"https://parsinger.ru/html/"+str(index[j+1])+str(i)+".html"
    })


    with open("res.json","w",encoding="utf-8") as file:
        json.dump(resultjs,file,indent=4,ensure_ascii=False)








