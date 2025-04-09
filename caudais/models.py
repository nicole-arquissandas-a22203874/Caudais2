from django.db import models

class Regiao(models.Model):
    nome = models.CharField(max_length=100)
    localidade = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome} - {self.localidade}'
class PontoMedida(models.Model):
    regiao = models.ForeignKey(Regiao, on_delete=models.CASCADE,related_name='pontoMedida')
    tipoMedidor=models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    def __str__(self):
        return f'Ponto de Medida {self.id} - {self.regiao}'

class Serie(models.Model):
    ponto_medida = models.ForeignKey(PontoMedida, on_delete=models.CASCADE,related_name='serie')

    def __str__(self):
        return f'Série {self.id} - {self.ponto_medida}'

class Medicao(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE,related_name='medicao')
    valor = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True, db_index=True)   # Indexado para melhorar pesquisa

    def __str__(self):
        return f'Caudal: {self.valor} - Data: {self.timestamp}'
