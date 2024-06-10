from django.shortcuts import render

# Create your views here.
# pwsite/views.py



def index_view(request):
    return render(request, "pwsite/index.html")

def sobre_view(request):
    return render(request, "pwsite/sobre.html")



