from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from autenticacao.decorators import group_required
from .forms import BandaForm, AlbumForm, MusicaForm
# Create your views here.

def listaBandas_view(request):
    bandas=Banda.objects.all()
    bandaOrdenada=Banda.objects.order_by('ano_criacao')

    contexto={'bandas':bandaOrdenada}
    return render(request,"bandas/listaBandas.html",contexto)


    contexto={'bandas':bandaOrdenada}
    return render(request,"bandas/listaBandas.html",contexto)
def banda_view(request,banda_id):
    banda=Banda.objects.get(id=banda_id)
    albums=Album.objects.filter(banda__id=banda_id)
    nrAlbums=albums.all().count()
    nrMusicas=0
    for album in albums:
       nrMusicas=album.musicas.count()

    contexto={'banda':banda,'albums':albums,'nrMusicas':nrMusicas,'nrAlbums':nrAlbums}
    return render(request,"bandas/banda_details.html",contexto)

def album_view(request,album_id):
    album=Album.objects.get(id=album_id)
    musicas=Musica.objects.filter(album__id=album_id)
    contexto={'album':album,'musicas':musicas}
    return render(request,"bandas/album_details.html",contexto)

def musica_view(request,musica_id):
    musica=Musica.objects.get(id=musica_id)
    contexto={'musica':musica}
    return render(request,"bandas/musica_details.html",contexto)


@login_required(login_url='/autenticacao/loginB/')
@group_required('EditorBandas', login_url='/autenticacao/loginB/')
def novo_banda_view(request):
    if request.method == 'POST':
        form = BandaForm(request.POST or None,request.FILES)
        if form.is_valid():
            # Assign the current authenticated user to the autor field
            banda= form.save(commit=False)

            banda.save()
            return redirect('bandas:index')
    else:
        form = BandaForm()

    context = {'form': form}
    return render(request, 'bandas/nova_banda.html', context)


@login_required(login_url='/autenticacao/loginB/')
@group_required('EditorBandas', login_url='/autenticacao/loginA/')
def edita_banda_view(request, banda_id):
    banda = Banda.objects.get(id=banda_id)

    if request.POST:
        form = BandaForm(request.POST or None,request.FILES, instance=banda)
        if form.is_valid():
            form.save()
            return redirect('bandas:index')

    else:
        form = BandaForm(instance=banda)

    context = {'form': form, 'banda':banda}
    return render(request, 'bandas/edita_banda.html', context)


@login_required(login_url='/autenticacao/loginB/')
@group_required('EditorBandas', login_url='/autenticacao/loginB/')
def apaga_banda_view(request, banda_id):
    banda= Banda.objects.get(id=banda_id)
    banda.delete()

    return redirect('bandas:index')


@login_required(login_url='/autenticacao/loginB/')
@group_required('EditorBandas', login_url='/autenticacao/loginB/')
def novo_album_view(request, banda_id):
    banda = Banda.objects.get(id=banda_id)  # Retrieve the Autor object using autor_id
    form = AlbumForm(request.POST or None,request.FILES)

    if form.is_valid():

        album = form.save(commit=False)  # Create a Livro instance without saving to the database yet
        album.banda = banda # Set the autor attribute of the Livro instance
        album.save()  # Save the Livro instance to the database
        return redirect('bandas:banda_detail',banda_id=album.banda.id)

    context = {'form': form,'banda_id':banda_id}
    return render(request, 'bandas/novo_album.html', context)

@login_required(login_url='/autenticacao/loginB/')
@group_required('EditorBandas', login_url='/autenticacao/loginB/')
def edita_album_view(request, album_id):
    album=Album.objects.get(id=album_id)

    if request.POST:
        form = AlbumForm(request.POST or None,request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('bandas:banda_detail',banda_id=album.banda.id)

    else:
        form = AlbumForm(instance=album)

    context = {'form': form, 'album':album}
    return render(request, 'bandas/edita_album.html', context)

@login_required(login_url='/autenticacao/loginB/')
@group_required('EditorBandas', login_url='/autenticacao/loginB/')
def apaga_album_view(request, album_id):
    album= Album.objects.get(id=album_id)
    album.delete()

    return redirect('bandas:banda_detail',banda_id=album.banda.id)

@login_required(login_url='/autenticacao/loginB/')
@group_required('EditorBandas', login_url='/autenticacao/loginB/')
def novo_musica_view(request, album_id):
    album = Album.objects.get(id=album_id)  # Retrieve the Autor object using autor_id
    form = MusicaForm(request.POST or None,request.FILES)

    if form.is_valid():

        musica= form.save(commit=False)  # Create a Livro instance without saving to the database yet
        musica.album = album # Set the autor attribute of the Livro instance

        musica.save()  # Save the Livro instance to the database
        return redirect('bandas:album_detail',album_id=musica.album.id)

    context = {'form': form,'album_id':album_id}
    return render(request, 'bandas/nova_musica.html', context)

@login_required(login_url='/autenticacao/loginB/')
@group_required('EditorBandas', login_url='/autenticacao/loginB/')
def edita_musica_view(request, musica_id):
    musica = Musica.objects.get(id=musica_id)

    if request.POST:

            form = MusicaForm(request.POST or None,request.FILES, instance=musica)
            if form.is_valid():
                form.save()
                return redirect('bandas:album_detail',album_id=musica.album.id)

    else:
        form = MusicaForm(instance=musica)

    context = {'form': form, 'musica':musica}
    return render(request, 'bandas/edita_musica.html', context)

@login_required(login_url='/autenticacao/loginB/')
@group_required('EditorBandas', login_url='/autenticacao/loginB/')
def apaga_musica_view(request, musica_id):
    musica = Musica.objects.get(id=musica_id)

    musica.delete()

    return redirect('bandas:album_detail',album_id=musica.album.id)




