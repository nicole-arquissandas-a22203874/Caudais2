from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index_view),
    path('funcao2/',views.funcao2),
    path('funcao3/',views.funcao3),
    path('funcao4/',views.funcao4)
]