from platform import system
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pathlib import Path


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--headless')

# because of docker
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')  # bad for performance ((( https://github.com/elgalu/docker-selenium/issues/20

browser = webdriver.Chrome(service=Service(str(Path(Path().parent, 'selenium_drivers', 'chromedriver'))), options=chrome_options)
# if system() == 'Windows':
#     browser = webdriver.Chrome(service=Service(str(Path(Path().parent, 'selenium_drivers', 'chromedriver.exe'))), options=chrome_options)
# elif system() == 'Linux':
#     browser = webdriver.Chrome(service=Service(str(Path(Path().parent, 'selenium_drivers', 'chromedriver'))), options=chrome_options)
# else:
#     browser = ''
#     print('Use Windows or Linux!')
#     exit()

browser.get('https://www.deepl.com/translator#en/ru/')
field = browser.find_element(By.XPATH, '/html/body/div/main/div/div/section/div/div/textarea')


def translate(text):
    field.clear()
    field.send_keys(text)
    while True:
        sleep(3)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        translation = soup.find('div', id='target-dummydiv').text
        if translation.strip():
            break
    return translation
