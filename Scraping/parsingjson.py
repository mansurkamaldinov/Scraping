import requests

url = "https://parsinger.ru/downloads/get_json/res.json"
response =requests.get(url=url).json()
for item in 