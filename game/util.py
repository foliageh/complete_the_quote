from random import randint, sample
from . import translator
from . models import Quote


def _add_quotes_from_csv():
    # data in quotes.csv was given in the following format:
    #   row1: quote,author,category
    #   row2: blablabla,D.Trump,"freedom, something"
    #   row3: I'm a Lizard King,Jim Morrison,"power, something, cute-animals"
    #   ...

    import csv
    from pathlib import Path

    dataset_path = Path(Path().parent, 'sentences_datasets', 'quotes.csv')
    dataset = open(dataset_path, newline='', encoding='utf-8')
    reader = csv.reader(dataset)
    next(reader)  # skip title line

    # cleared_dataset = open(Path(Path().parent, 'sentences_datasets', 'quotes_cleared.csv'), 'w', newline='', encoding='utf-8')
    # writer = csv.writer(cleared_dataset, delimiter=',')

    rows_added = 0
    while True:
        try:
            quote, author, tags = next(reader)
            while len(quote) > 600 or len(quote) < 4 or len(author) < 4 or len(author) > 150 or len(tags) > 500 or \
                    any(not ('A' <= i <= 'z') and i not in '\'\u00a0"()-&—#–№−:;,.?!0123456789 ' for i in quote) or \
                    any(not ('A' <= i <= 'z') and i not in '\'\u00a0"()-&—#–№−:;,.?!0123456789 ' for i in author) or \
                    any(not ('A' <= i <= 'z') and i not in '\'\u00a0"()-&—#–№−:;,.?!0123456789 ' for i in tags):
                quote, author, tags = next(reader)
        except StopIteration:
            break

        quote = quote.replace('\u00a0', ' ').replace('  ', ' ').replace(' ,', ',').replace(' .', '.')  # \u00a0 - nbsp
        quote = quote.replace(' ?', '?').replace(' !', '!').replace(' ;', ';').replace(' )', ')').strip()
        author = author.replace('\u00a0', ' ').replace('  ', ' ').replace(' ,', ',').replace(' .', '.')
        author = author.replace(' ?', '?').replace(' !', '!').replace(' ;', ';').replace(' )', ')').strip()
        tags = tags.replace('\u00a0', ' ').replace('  ', ' ').replace(', ', ',').strip().lower()
        tags = [tag for tag in tags.split(',') if tag != 'attributed-no-source' and all('A' <= i <= 'z' or i in '-—–−' or '0' <= i <= '9' for i in tag)]
        tags = ','.join(tags)

        Quote(source=author, text=quote, tags=tags).save()
        rows_added += 1
        # writer.writerow([author, quote, tags])

    print(f'Yeah! {rows_added} rows was added.')


def mask(text):
    split_symbols = '"()-&—#–№−:;,.?!0123456789 '

    sentence = []
    words = []
    word_start_pos = -1
    for i in range(len(text)):
        if text[i] in split_symbols:
            if word_start_pos != -1:
                word = text[word_start_pos:i]
                if word.lower() not in ('i', "i'm", 'you', 'he', 'she', 'we', 'my', 'his', 'her', 'our', 'and'):
                    words.append((word, len(sentence)))
                sentence.append(word)
                word_start_pos = -1
            sentence.append(text[i])
        elif word_start_pos == -1:
            word_start_pos = i

    replacements_number = randint(len(words) // 7, len(words) // 3)
    replacements_number = replacements_number if replacements_number else 1
    replacement_words_indexes = sample(range(len(words)), replacements_number)

    hided_words = []
    for i in sorted(replacement_words_indexes):
        hided_words.append(sentence[words[i][1]])
        sentence[words[i][1]] = '___'

    return sentence, hided_words


def get_random_quote():
    quote = Quote.objects.order_by('?').first()
    quote = {'quote': quote.text,
             'author': quote.source,
             'tags': quote.tags}
    quote['masked_quote'], quote['hided_words'] = mask(quote['quote'])
    quote['translation'] = translator.translate(quote['quote'])
    return quote


translator = translator.Translator()
