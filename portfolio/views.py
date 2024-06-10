
from django.shortcuts import render

def landing_page(request):
    return render(request, 'portfolio/landing_page.html')

def mebyme(request):
    return render(request, 'portfolio/mebyme.html')

def sobre(request):
    return render(request, 'portfolio/sobre.html')


