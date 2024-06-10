from django.contrib import admin
from .models import Curso, AreaCientifica, Disciplina, Projeto, LinguagemProgramacao, Docente

class DisciplinaAdmin(admin.ModelAdmin):
    list_display=('Disciplina','Ano_Curricular','semestre','Ects')
    ordering=('ano','semestre',)

    def Disciplina(self,obj):
        return obj.nome

    def Ano_Curricular(self,obj):
        return obj.ano

    def Ects(self,obj):
        return obj.ects





# Register your models here.
admin.site.register(Curso)
admin.site.register(AreaCientifica)
admin.site.register(Disciplina,DisciplinaAdmin)
admin.site.register(Projeto)
admin.site.register(LinguagemProgramacao)
admin.site.register(Docente)