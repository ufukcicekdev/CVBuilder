# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name ="accounts"

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('chage_password/', views.change_password, name='changepass'),

]
