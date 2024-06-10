from django.urls import path
from . import views

app_name = 'pwsite'

urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('sobre/', views.sobre_view, name='sobre'),





]
