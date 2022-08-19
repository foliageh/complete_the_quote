from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import util


def index(request):
    return render(request, 'game/index.html', {})


@csrf_exempt
def get_random_quote(request):
    try:
        quote = util.get_random_quote()
    except:
        util.fill_db()
        quote = util.get_random_quote()

    if request.method == 'GET':
        return JsonResponse(quote)
    else:
        return JsonResponse({'error': 'GET request required.'}, status=400)
