from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_form, name='home'),
    path('login', views.loginView, name='login'),


    path('librarian', views.librarian, name='librarian'),



    path('publisher', views.publisher, name='publisher'),



    path('dashboard', views.dashboard, name='dashboard'),
]
