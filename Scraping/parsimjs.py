import requests
import json

response = requests.get(url="https://parsinger.ru/downloads/get_json/res.json").json()
for x in response:
    lenn = x["categories"]
    print(len(lenn))


