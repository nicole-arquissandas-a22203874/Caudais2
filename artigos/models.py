
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#1-N author-comentario
#1-N artigo-comentario
#1-n artigo-ratings
#1-n author-followers







class Autor(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    idade = models.PositiveIntegerField(null=True, blank=True)
    followers= models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username

class Artigo(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE,related_name='artigos')
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    user_comentario = models.ForeignKey(User, on_delete=models.CASCADE)
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE,related_name='comentarios')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_comentario.username}:{self.texto}"



class Rating(models.Model):
    user_rating = models.ForeignKey(User, on_delete=models.CASCADE)
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE,related_name='ratings')
    nota = models.IntegerField(verbose_name='rating(1-10)')

    def __str__(self):
        return f"{self.user_rating.username}: {self.nota}"







