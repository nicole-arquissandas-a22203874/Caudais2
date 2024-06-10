from bandas.models import*
import json
from datetime import timedelta

Banda.objects.all().delete()
Album.objects.all().delete()



with open('bandas/jsons/bandas.json')as f:
    bandas=json.load(f)

    for banda in bandas:
        Banda.objects.create(
            nome_banda=banda['titulo'],
            nacionalidade=banda['nacionalidade'],
            ano_criacao=banda['ano_criacao']

            )


with open('bandas/jsons/discos.json')as f:
    albums=json.load(f)

    for album in albums:
        Album.objects.create(
            titulo_Album=album['titulo'],
            banda=Banda.objects.get(nome_banda=album['banda']),
            ano_lancamento=album['ano_lancamento']

            )
        for musica in album['musicas']:
            duration_parts = musica['duracao'].split(':')
            duracao_timedelta = timedelta(minutes=int(duration_parts[0]), seconds=int(duration_parts[1]))
            Musica.objects.create(
                nome_musica=musica['titulo'],
                duracao=duracao_timedelta,
                album=Album.objects.get(titulo_Album=album['titulo'])

            )


