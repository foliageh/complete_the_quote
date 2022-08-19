# Complete The Quote
A simple game written with Django for learning English by inserting missing words in random quotes. Each quotation is accompanied by Russian translation (future expansion into other languages is planned).

**RU:** Простая игра на Django для изучения англиского путем вставления пропущенных слов в случайные цитаты. К каждой цитате дается перевод на русском языке (в будущем планируется расширение и на другие языки).

## Installation
You need Docker on your computer to run the app.
```sh
git clone https://github.com/foliageh/complete_the_quote.git
cd complete_the_quote
docker-compose run django python manage.py migrate
```

## Launch & Closing
Enter the following command while in the project folder to launch the app:
```sh
docker-compose up
```
Then open http://localhost:8000 in browser.

To close the app, enter the following command:
```sh
docker-compose down
```

## Screenshots
![1](https://user-images.githubusercontent.com/46216950/185354842-dd1ec6d3-2bb7-4257-9daa-d0a9bbfc3eb2.jpg)
![2](https://user-images.githubusercontent.com/46216950/185354830-78a08165-be2a-4897-b07e-5f3207df2f31.jpg)

## Sources
Quotes: https://github.com/ShivaliGoel/Quotes-500K  
Translations: https://www.deepl.com