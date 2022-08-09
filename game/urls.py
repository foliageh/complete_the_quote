from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/get_quote', views.get_random_quote, name='get_quote')
]
