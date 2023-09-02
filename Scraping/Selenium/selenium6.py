from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as browser:
    browser.get("https://parsinger.ru/selenium/7/7.html")
    print(sum(int(el.text) for el in browser.find_elements(By.TAG_NAME, "option")))

