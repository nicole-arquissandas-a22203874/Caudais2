from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [

    path('', views.landing_page, name='index'),
    path('mebyme/', views.mebyme, name='mebyme'),
    path('sobre/', views.sobre, name='sobre'),



]