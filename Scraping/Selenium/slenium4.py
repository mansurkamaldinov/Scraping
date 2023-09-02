from selenium import webdriver
from selenium.webdriver.common.by import By
import time

with webdriver.Chrome() as browser:
    browser.get("https://parsinger.ru/selenium/4/4.html")

    elements = browser.find_elements(By.CLASS_NAME, "check")
    for element in elements:
        element.click()
    btn = browser.find_element(By.CLASS_NAME,"btn").click()
    res = browser.find_element(By.TAG_NAME,"p")
    print(res.text)

    time.sleep(10)





