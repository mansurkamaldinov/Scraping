import requests
from bs4 import BeautifulSoup
import lxml
s = []
s1 = []
s2 = []
s3 = []
s4 = []
s5 = []
s6 = []
s7 = []
s8 = []
s9 = []
s10 = []
s11 = []
s12 = []
s13 = []
s14 = []
s15 = []
url = "https://parsinger.ru/table/5/index.html"
response = requests.get(url=url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text,"lxml")
div = soup.find_all("th")
div1 = soup.select("td:nth-child(1)")
div2 = soup.select("td:nth-child(2)")
div3 = soup.select("td:nth-child(3)")
div4 = soup.select("td:nth-child(4)")
div5 = soup.select("td:nth-child(5)")
div6 = soup.select("td:nth-child(6)")
div7 = soup.select("td:nth-child(7)")
div8 = soup.select("td:nth-child(8)")
div9 = soup.select("td:nth-child(9)")
div10 = soup.select("td:nth-child(10)")
div11= soup.select("td:nth-child(11)")
div12= soup.select("td:nth-child(12)")
div13 = soup.select("td:nth-child(13)")
div14 = soup.select("td:nth-child(14)")
div15 = soup.select("td:nth-child(15)")
for txt in div:
    txt = txt.text
    s.append(txt)
for txt1 in div1:
    txt1 = txt1.text
    s1.append(txt1)
for txt2 in div2:
    txt2 = txt2.text
    s2.append(txt2)
for txt3 in div3:
    txt3 = txt3.text
    s3.append(txt3)
for txt4 in div4:
    txt4 = txt4.text
    s4.append(txt4)
for txt5 in div5:
    txt5 = txt5.text
    s5.append(txt5)
for txt6 in div6:
    txt6 = txt6.text
    s6.append(txt6)
for txt7 in div7:
    txt7 = txt7.text
    s7.append(txt7)
for txt8 in div8:
    txt8 = txt8.text
    s8.append(txt8)
for txt9 in div9:
    txt9 = txt9.text
    s9.append(txt9)
for txt10 in div10:
    txt10 = txt10.text
    s10.append(txt10)
for txt11 in div11:
    txt11 = txt11.text
    s11.append(txt11)
for txt12 in div12:
    txt12 = txt12.text
    s12.append(txt12)
for txt13 in div13:
    txt13 = txt13.text
    s13.append(txt13)
for txt14 in div14:
    txt14 = txt14.text
    s14.append(txt14)
for txt15 in div15:
    txt15 = txt15.text
    s15.append(txt15)
num1 = sum(list(map(float,s1)))
num2 = sum(list(map(float,s2)))
num3 = sum(list(map(float,s3)))
num4 = sum(list(map(float,s4)))
s.append(num1,num2)
print(s)





























