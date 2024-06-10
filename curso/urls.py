from django.urls import path
from . import views


app_name = 'curso'
urlpatterns = [
    path('index/', views.CursoLista_view, name='index'),
    path('curso/<int:curso_id>/', views.Curso_view, name='cursoDetail'),
    path('disciplina/<int:disciplina_id>/', views.disciplina_details_view, name='disciplina'),
    path('projeto/<int:projeto_id>/', views.projeto_view, name='projeto'),

    path('curso/<int:curso_id>/edita', views.edita_curso_view,name="edita_curso"),
    path('areacientifica/<int:curso_id>/nova-areaCientifica/', views.novo_areaCientifica_view,name="nova_areaCientifica"),
    path('areacientifica/<int:areacientifica_id>/edita-cientifica/', views.edita_areaCientifica_view,name="edita_areaCientifica"),
    path('areacientifica/<int:areacientifica_id>/apaga-areaCientifica/', views.apaga_areaCientifica_view,name="apagar_areaCientifica"),
    path('disciplina/<int:areacientifica_id>/nova-disciplina/', views.novo_disciplina,name="nova_disciplina"),
    path('disciplina/<int:disciplina_id>/edita-disciplina/', views.edita_disciplina_view,name="edita_disciplina"),
    path('disciplina/<int:disciplina_id>/apaga-disicplina/', views.apaga_disciplina_view,name="apagar_disciplina"),
    path('projeto/<int:disciplina_id>/novo-projeto/', views.novo_projeto_view,name="nova_projeto"),
    path('projeto/<int:projeto_id>/edita-projeto/', views.edita_projeto_view,name="edita_projeto"),
    path('projeto/<int:projeto_id>/apaga-projeto/', views.apaga_projeto_view,name="apagar_projeto"),

]