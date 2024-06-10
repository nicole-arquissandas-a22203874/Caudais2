from django.db import models

# Create your models here.

class Curso(models.Model):
    nome=models.CharField(max_length=25)
    apresentacao=models.TextField()
    objetivos=models.TextField()
    competencias=models.TextField()

    def __str__(self):
        return self.nome

class AreaCientifica(models.Model):
    nome=models.CharField(max_length=100)
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE,related_name='areasCientificas',null=True,blank=True)
    def __str__(self):
        return self.nome
class LinguagemProgramacao(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome=models.CharField(max_length=100)
    ano=models.IntegerField()
    semestre=models.CharField(max_length=25)
    ects=models.IntegerField()
    curricularIUnitReadableCode=models.CharField(max_length=25)
    areaCientifica=models.ForeignKey(AreaCientifica, on_delete=models.CASCADE,related_name='disciplinas',null=True,blank=True)
    curso=models.ManyToManyField(Curso,related_name='disciplinas',null=True,blank=True)
    linguagens=models.ManyToManyField(LinguagemProgramacao,related_name='disciplinas',null=True,blank=True)
    def __str__(self):
        return self.nome


class Projeto(models.Model):
    nome=models.CharField(max_length=25)
    descricao=models.TextField()
    conceitosAplicados=models.TextField()
    tecnologiasUsadas=models.TextField()
    imagem = models.ImageField(upload_to='curso/fotosProjetos',null=True,blank=True)
    video_demo = models.URLField(null=True,blank=True)
    repositorio_github = models.URLField(null=True,blank=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE,related_name='projetos',null=True,blank=True)
    linguagensProgramacao=models.ManyToManyField(LinguagemProgramacao,related_name='projetos',null=True,blank=True)

    def __str__(self):
        return self.nome


class Docente(models.Model):
    nome = models.CharField(max_length=100)
    disciplinas = models.ManyToManyField(Disciplina,related_name='docentes')

    def __str__(self):
        return self.nome




