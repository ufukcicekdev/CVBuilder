# accounts/urls.py
from django.urls import path
from .views import *

app_name = 'language'



urlpatterns = [
    path('set_language/', set_language, name='set_language'),
]
