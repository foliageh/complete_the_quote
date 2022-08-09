import csv
from random import randint
from pathlib import Path


dataset_path = Path(Path().parent, 'sentences_datasets', 'quotes.csv')
dataset = open(dataset_path, newline='', encoding='utf-8')
reader = csv.reader(dataset)
next(reader)  # skip title line


def get_random_quote():  # (self, tags=None):
    for _ in range(randint(0, 1000)):  # skip a random number of quotes
        next(reader)
    quote, author, tags = next(reader)
    while len(quote) > 300:
        quote, author, tags = next(reader)
    quote = quote.replace('\u00a0', ' ').replace('  ', ' ').replace(' ,', ',').replace(' .', '.').replace(' ?', '?').replace(' !', '!').replace(' ;', ';').strip()  # replace nbsp and double spaces
    tags = [tag for tag in tags.split(', ') if tag != 'attributed-no-source']
    return {'quote': quote, 'author': author, 'tags': tags}
