from django.urls import path
from .views import *
from . import views


app_name = 'profile'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('add_education/', views.add_education, name='add_education'),
    path('edit_education/<int:education_id>/', views.edit_education, name='edit_education'),
    path('education/<int:education_id>/delete/', views.delete_education, name='delete_education'),

    path('add-experience/', views.add_experience, name='add_experience'),
    path('edit-experience/<int:pk>/', views.edit_experience, name='edit_experience'),
    path('delete-experience/<int:pk>/', views.delete_experience, name='delete_experience'),


    path('add_skill/', views.add_skill, name='add_skill'),
    path('edit_skill/<int:pk>/', views.edit_skill, name='edit_skill'),
    path('delete_skill/<int:pk>/', views.delete_skill, name='delete_skill'),


    path('add_certificate/', views.add_certificate, name='add_certificate'),
    path('edit_certificate/<int:pk>/', views.edit_certificate, name='edit_certificate'),
    path('delete_certificate/<int:pk>/', views.delete_certificate, name='delete_certificate'),

    path('add-cover-letter/', views.add_cover_letter, name='add_cover_letter'),
    path('edit-cover-letter/<int:pk>/', views.edit_cover_letter, name='edit_cover_letter'),
    path('delete-cover-letter/<int:pk>/', views.delete_cover_letter, name='delete_cover_letter'),


    path('add-project/', views.add_project, name='add_project'),
    path('edit-project/<int:pk>/', views.edit_project, name='edit_project'),
    path('delete-project/<int:pk>/', views.delete_project, name='delete_project'),


    path('add-self-introduction/', views.add_self_introduction, name='add_self_introduction'),
    path('edit-self-introduction/<int:pk>/', views.edit_self_introduction, name='edit_self_introduction'),
    path('delete-self-introduction/<int:pk>/', views.delete_self_introduction, name='delete_self_introduction'),



    path('generate-cv/', views.generate_cv, name='generate_user_cv'),

    path('cv/<int:cv_id>/', views.view_cv, name='view_cv'),
    path('delete-cv/<int:pk>/', views.delete_cv, name='delete_cv'),

]

