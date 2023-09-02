from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'http://parsinger.ru/selenium/3/3.html'
with webdriver.Chrome() as browser:
    browser.get(url)
    print(sum(int(el.text) for el in browser.find_elements(By.XPATH, "//div[@class='text']/p[2]")))