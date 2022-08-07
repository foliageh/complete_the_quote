import csv
from random import randint, sample

from platform import system
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--headless')

# because of docker
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--disable-gpu')

if system() == 'Windows':
    browser = webdriver.Chrome(service=Service('selenium_drivers/chromedriver.exe'), options=chrome_options)
elif system() == 'Linux':
    browser = webdriver.Chrome(service=Service('selenium_drivers/chromedriver'), options=chrome_options)
else:
    browser = ''
    print('Use Windows or Linux!')
    exit()

browser.get('https://www.deepl.com/translator#en/ru/')
field = browser.find_element(By.XPATH, '/html/body/div/main/div/div/section/div/div/textarea')


def hide_words(quote):
    split_symbols = ' ;,.?!'

    sentence = []
    words_number = 0
    word_start_pos = -1
    for i in range(len(quote)):
        if quote[i] in split_symbols:
            if word_start_pos != -1:
                sentence.append(quote[word_start_pos:i])
                words_number += 1
                word_start_pos = -1
            sentence.append(quote[i])
        elif word_start_pos == -1:
            word_start_pos = i

    replacements_number = randint(words_number//7, words_number//3)
    replacements_number = replacements_number if replacements_number else 1
    replacement_words_indexes = sample(range(1, words_number+1), replacements_number)

    hided_words = []
    word_index = 0
    for i in range(len(sentence)):
        if sentence[i] in split_symbols:
            continue
        word_index += 1
        if word_index in replacement_words_indexes:
            hided_words.append(sentence[i])
            sentence[i] = '___'

    return ''.join(sentence), hided_words


def translate(text):
    field.send_keys(text)
    while True:
        soup = BeautifulSoup(browser.page_source, 'lxml')
        translation = soup.find('div', id='target-dummydiv').text
        if translation.strip():
            break
        sleep(3)
    return translation


with open('sentences_datasets/quotes.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # skip title line
    for _ in range(randint(0, 1000)):
        next(reader)
    for _ in range(1):
        quote, author, tags = next(reader)
        quote = quote.replace('\u00a0', ' ').replace('  ', ' ').strip()  # replace nbsp and double spaces
        tags = [tag for tag in tags.split(', ') if tag != 'attributed-no-source']

        unfilled_sentence, hided_words = hide_words(quote)
        print(unfilled_sentence)
        print(author, tags, '\n')
        print(translate(quote))
        words = input().replace('  ', ' ').strip().split(' ')
        for word, right_word in zip(words, hided_words):
            if word == right_word:
                print(f'{word}: correct')
            else:
                print(f'{word}: wrong! (right word is `{right_word}`)')
        # sleep(20)
        print(quote)

'''
class Database:
    def __init__(self):
        pass

    def get_random_quote(self, tags=None):
        pass

    def add_quote(self, quote, translation, tags, source):
        pass
'''