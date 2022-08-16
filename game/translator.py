from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pathlib import Path
# from platform import system


class Translator:
    def __init__(self, engine='DeepL'):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--headless')

        # because of docker
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')  # bad for performance ((( https://github.com/elgalu/docker-selenium/issues/20

        self.browser = webdriver.Chrome(service=Service(str(Path(Path().parent, 'selenium_drivers', 'chromedriver'))), options=chrome_options)
        # if system() == 'Windows':
        #     browser = webdriver.Chrome(service=Service(str(Path(Path().parent, 'selenium_drivers', 'chromedriver.exe'))), options=chrome_options)
        # elif system() == 'Linux':
        #     browser = webdriver.Chrome(service=Service(str(Path(Path().parent, 'selenium_drivers', 'chromedriver'))), options=chrome_options)
        # else:
        #     print('Use Windows or Linux!')
        #     exit()

        if engine == 'DeepL':
            self.browser.get('https://www.deepl.com/translator#en/ru/')
            self.input_field = self.browser.find_element(By.XPATH, '/html/body/div/main/div/div/section/div/div/textarea')

    def translate(self, text):
        self.input_field.clear()
        self.input_field.send_keys(text)
        sleep(2)
        while True:
            soup = BeautifulSoup(self.browser.page_source, 'lxml')
            translation = soup.find('div', id='target-dummydiv').text.strip()
            if len(translation) > 3 and '[...]' not in translation:
                break
            sleep(1)
        return translation
