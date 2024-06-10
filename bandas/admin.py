

# Register your models here.
from django.contrib import admin
from .models import Banda
from .models import Album
from .models import Musica


class AlbumAdmin(admin.ModelAdmin):
    list_display=('titulo_Album','banda','ano_lancamento')
    #ordering=('titulo_Album','nome_banda')
    #search_fields=('nome_banda','titulo_Album','nome_musica')

class MusicaAdmin(admin.ModelAdmin):
    list_display=('nome_musica','album','banda')

    def banda(self, obj):
        return obj.album.banda.nome_banda

class BandaAdmin(admin.ModelAdmin):
    list_display=('Banda','ano_criacao')
    ordering=('ano_criacao',)

    def Banda(self, obj):
        return obj.nome_banda


# Register your models here.
admin.site.register(Banda,BandaAdmin)
admin.site.register(Album,AlbumAdmin)
admin.site.register(Musica,MusicaAdmin)

