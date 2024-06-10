from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def index_view(request):
    return HttpResponse("Olá n00b, esta é a página web mais básica do mundo!")


def funcao2(request):
    return HttpResponse("esta  e segunda funcao")



def funcao3(request):
    return HttpResponse("esta  e terceira funcao")


def funcao4(request):
    return HttpResponse("esta  e quarta funcao")

