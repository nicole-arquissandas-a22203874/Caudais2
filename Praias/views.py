from django.shortcuts import render

# Create your views here.
from .models import *

# Create your views here.

def listaPraias_view(request):
    praias=Praia.objects.all()
    contexto={'praias':praias}
    return render(request,"Praias/listaPraias.html",contexto)

def Praia_view(request,praia_id):
    praia=Praia.objects.get(id=praia_id)
    contexto={'praia':praia}
    return render(request,"Praias/Praia_details.html",contexto)


