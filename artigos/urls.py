from django.urls import path
from . import views

app_name = 'artigos'

urlpatterns = [
    path('index/', views.listaArtigos_view, name='index'),
    path('artigo_details/<int:artigo_id>/', views.artigo_details_view, name='artigoDetails'),
    path('user/<str:usernamestr>/', views.user_view, name='user'),
    path('followers/<int:autor_id>/', views.followers_view, name='followers'),
    path('comentarios/<int:artigo_id>/', views.comentarios_view, name='comentarios'),
    path('ratings/<int:artigo_id>/', views.ratings_view, name='ratings'),
    path('comentarioDetail/<int:comentario_id>/', views.comentarioDetail_view, name='comentarioDetail'),
    path('ratingDetail/<int:rating_id>/', views.ratingDetail_view, name='ratingDetail'),
    path('NoFollowers/', views.NoFollowers_view, name='Nofollowers'),

    path('artigo/novo', views.novo_artigo_view,name="novo_artigo"),
    path('artigo/<int:artigo_id>/edita', views.edita_artigo_view,name="edita_artigo"),
    path('artigo/<int:artigo_id>/apaga', views.apaga_artigo_view,name="apagar_artigo"),
    path('comentario/<int:artigo_id>/novo-cometario/', views.novo_comentario_view,name="novo_comentario"),
    path('comentario/<int:comentario_id>/edita-comentario/', views.edita_comentario_view,name="edita_comentario"),
    path('comentario/<int:comentario_id>/apaga-comentario/', views.apaga_comentario_view,name="apagar_comentario"),
    path('rating/<int:artigo_id>/novo-rating/', views.novo_rating_view,name="novo_rating"),
    path('rating/<int:rating_id>/edita-rating/', views.edita_rating_view,name="edita_rating"),
    path('rating/<int:rating_id>/apaga-rating/', views.apaga_rating_view,name="apagar_rating"),




]