# accounts/urls.py
from django.urls import path
from .views import *

app_name = 'core'



urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path("forgot-password/",forgot_password, name="forgot_password"),
    path("reset-password/",reset_password,name="reset_password"),
]
