from django.urls import path
from . import views

app_name = 'Praias'

urlpatterns = [
    path('ListaPraias/', views.listaPraias_view, name='praias'),
    path('praia/<int:praia_id>/', views.Praia_view, name='praia_detail'),


]