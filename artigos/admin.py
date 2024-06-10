from django.contrib import admin
from .models import Autor, Artigo, Comentario, Rating
# Register your models here.

admin.site.register(Autor)
admin.site.register(Artigo)
admin.site.register(Comentario)
admin.site.register(Rating)



