from django.urls import path
from . import views


app_name = 'caudais'
urlpatterns = [
    path('upload_medicoes/', views.upload_medicoes, name='upload_medicoes'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
