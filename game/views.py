from django.shortcuts import render


def index(request):
    quote = 1
    return render(request, 'game/index.html', {
        'quote': quote,
    })

