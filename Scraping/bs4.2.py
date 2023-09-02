import requests
from bs4 import BeautifulSoup
import lxml
s = []
for i in range(1,5):
    url = "https://parsinger.ru/html/index4_page_"+str(i)+".html"
    response = requests.get(url)
    response.encoding="utf-8"
    soup = BeautifulSoup(response.text,"lxml")