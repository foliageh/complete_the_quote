from random import randint, sample
from . import quote_db, translator


def mask(text):
    split_symbols = ' ;,.?!'

    sentence = []
    words_number = 0
    word_start_pos = -1
    for i in range(len(text)):
        if text[i] in split_symbols:
            if word_start_pos != -1:
                sentence.append(text[word_start_pos:i])
                words_number += 1
                word_start_pos = -1
            sentence.append(text[i])
        elif word_start_pos == -1:
            word_start_pos = i

    replacements_number = randint(words_number // 7, words_number // 3)
    replacements_number = replacements_number if replacements_number else 1
    replacement_words_indexes = sample(range(1, words_number + 1), replacements_number)

    hided_words = []
    word_index = 0
    for i in range(len(sentence)):
        if sentence[i] in split_symbols:
            continue
        word_index += 1
        if word_index in replacement_words_indexes:
            hided_words.append(sentence[i])
            sentence[i] = '___'
    print(text, sentence)
    return sentence, hided_words


def get_random_quote():
    quote = quote_db.get_random_quote()
    quote['masked_quote'], quote['hided_words'] = mask(quote['quote'])
    quote['translation'] = translator.translate(quote['quote'])
    return quote
