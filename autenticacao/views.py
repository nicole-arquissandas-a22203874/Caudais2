

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import models, authenticate, login, logout
from artigos.models import Autor



def registo_viewA(request):
    if request.method == "POST":
        usert= models.User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            first_name=request.POST['nome'],
            last_name=request.POST['apelido'],
            password=request.POST['password']
        )
        Autor.objects.create(user=usert)
        return redirect('autenticacao:loginA')

    return render(request, 'autenticacao/registoA.html')


def registo_viewB(request):
    if request.method == "POST":
        models.User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            first_name=request.POST['nome'],
            last_name=request.POST['apelido'],
            password=request.POST['password']
        )
        return redirect('autenticacao:loginB')

    return render(request, 'autenticacao/registoB.html')

def registo_viewC(request):
    if request.method == "POST":
        models.User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            first_name=request.POST['nome'],
            last_name=request.POST['apelido'],
            password=request.POST['password']
        )
        return redirect('autenticacao:loginC')

    return render(request, 'autenticacao/registoC.html')



def login_viewA(request):
    if request.method == "POST":

        # Verifica as credenciais
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            # Se as credenciais são válidas, faz login e redireciona
            login(request, user)
            return render(request, 'autenticacao/userA.html')
        else:
            # Se inválidas, reenvia para login com mensagem
            render(request, 'autenticacao/loginA.html', {
                'mensagem':'Credenciais inválidas'
            })

    return render(request, 'autenticacao/loginA.html')


def login_viewB(request):
    if request.method == "POST":

        # Verifica as credenciais
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            # Se as credenciais são válidas, faz login e redireciona
            login(request, user)
            return render(request, 'autenticacao/userB.html')
        else:
            # Se inválidas, reenvia para login com mensagem
            render(request, 'autenticacao/loginB.html', {
                'mensagem':'Credenciais inválidas'
            })

    return render(request, 'autenticacao/loginB.html')


def login_viewC(request):
    if request.method == "POST":

        # Verifica as credenciais
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            # Se as credenciais são válidas, faz login e redireciona
            login(request, user)
            return render(request, 'autenticacao/userC.html')
        else:
            # Se inválidas, reenvia para login com mensagem
            render(request, 'autenticacao/loginC.html', {
                'mensagem':'Credenciais inválidas'
            })

    return render(request, 'autenticacao/loginC.html')
def logoutA_view(request):
    logout(request)
    return redirect('artigos:index')

def logoutB_view(request):
    logout(request)
    return redirect('bandas:index')

def logoutC_view(request):
    logout(request)
    return redirect('curso:index')




