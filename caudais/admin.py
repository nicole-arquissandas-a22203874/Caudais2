from django.contrib import admin
from .models import Regiao, PontoMedida, Serie, Medicao




class MedicaoAdmin(admin.ModelAdmin):
    list_display = ('serie','valor', 'timestamp')
    ordering = ['timestamp']
admin.site.register(Regiao)
admin.site.register(PontoMedida)
admin.site.register(Serie)
admin.site.register(Medicao,MedicaoAdmin)
