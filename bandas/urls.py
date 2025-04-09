from django.urls import path
from . import views

app_name = 'bandas'

urlpatterns = [
    path('index/', views.listaBandas_view, name='index'),
    path('bandas/<int:banda_id>/', views.banda_view, name='banda_detail'),

    path('albums/<int:album_id>/', views.album_view, name='album_detail'),
    path('musicas/<int:musica_id>/', views.musica_view, name='musica_detail'),

    path('banda/novo', views.novo_banda_view,name="nova_banda"),
    path('banda/<int:banda_id>/edita', views.edita_banda_view,name="edita_banda"),
    path('banda/<int:banda_id>/apaga', views.apaga_banda_view,name="apagar_banda"),
    path('album/<banda_id>/novo-album/', views.novo_album_view,name="novo_album"),
    path('album/<int:album_id>/edita-album/', views.edita_album_view,name="edita_album"),
    path('album/<int:album_id>/apaga-album/', views.apaga_album_view,name="apagar_album"),
    path('musica/<int:album_id>/novo-musica/', views.novo_musica_view,name="nova_musica"),
    path('musica/<int:musica_id>/edita-musica/', views.edita_musica_view,name="edita_musica"),
    path('musica/<int:musica_id>/apaga-musica/', views.apaga_musica_view,name="apagar_musica"),


]