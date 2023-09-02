import time
from selenium import webdriver
from selenium.webdriver.common.by import By


with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/selenium/1/1.html')

    input_form = browser.find_element(By.NAME, 'first_name').send_keys('Mansur')
    input_form2 = browser.find_element(By.NAME, 'last_name').send_keys('Kamaldinov')
    input_form3 = browser.find_element(By.NAME, 'patronymic').send_keys('Fanilevich')
    input_form4 = browser.find_element(By.NAME, 'age').send_keys('16')
    input_form5 = browser.find_element(By.NAME, 'city').send_keys('Kazan')
    input_form6 = browser.find_element(By.NAME, 'email').send_keys('Mansur-7')
    button = browser.find_element(By.ID,"btn").click()

    time.sleep(5)