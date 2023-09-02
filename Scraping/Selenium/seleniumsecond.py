import time
from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as browser:
    browser.get("https://parsinger.ru/selenium/2/2.html")
    input = browser.find_element(By.LINK_TEXT,'16243162441624').click()

    time.sleep(40)








