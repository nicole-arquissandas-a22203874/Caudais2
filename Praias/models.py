from django.db import models

# Create your models here.

class Regiao(models.Model):
    nome = models.CharField(max_length=200)
    def __str__(self):
        return self.nome

class Servico(models.Model):
    titulo = models.CharField(max_length=200)
    def __str__(self):
        return self.titulo

class Praia(models.Model):
    nome=models.CharField(max_length=200)
    regiao= models.ForeignKey(Regiao, on_delete=models.CASCADE,related_name='praias')
    imagem=models.ImageField(upload_to='Praias/fotos', null=True, blank=True)
    servicos=models.ManyToManyField(Servico, related_name='praias', blank=True)
    def __str__(self):
        return self.nome




