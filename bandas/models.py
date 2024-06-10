from django.db import models

# Create your models here.
class Banda(models.Model):
    nome_banda=models.CharField(max_length=50)
    foto=models.ImageField(upload_to='bandas/fotosBandas', null=True, blank=True)
    nacionalidade=models.CharField(max_length=25,blank=True,null=True)
    ano_criacao=models.IntegerField(null=True)
    biografia=models.TextField(default='', null=True, blank=True)
    def __str__(self):
        return self.nome_banda

class Album(models.Model):
    titulo_Album=models.CharField(max_length=50)
    capa=models.ImageField(upload_to='bandas/fotosAlbums', null=True, blank=True)
    banda=models.ForeignKey(Banda,on_delete=models.CASCADE,related_name='albums')
    ano_lancamento=models.IntegerField(null=True)
    def __str__(self):
        return self.titulo_Album

class Musica(models.Model):
    nome_musica=models.CharField(max_length=50)
    link=models.URLField(blank=True,null=True)
    duracao=models.DurationField(null=True)
    album=models.ForeignKey(Album,on_delete=models.CASCADE,related_name='musicas')
    letra = models.TextField(default='', null=True, blank=True)
    def __str__(self):
        return self.nome_musica
