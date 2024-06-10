from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from autenticacao.decorators import group_required
from .forms import ArtigoForm, ComentarioForm, RatingForm

# Create your views here.

def listaArtigos_view(request):
    artigos=Artigo.objects.all()
    contexto={'artigos':artigos}
    return render(request,"artigos/listaArtigos.html",contexto)

def artigo_details_view(request,artigo_id):
    artigo=Artigo.objects.get(id=artigo_id)
    autor=Artigo.objects.get(id=artigo_id).autor
    contexto={'artigo':artigo,'autor':autor}
    return render(request,"artigos/artigoDetails.html",contexto)



def user_view(request, usernamestr):
    usert = get_object_or_404(User, username=usernamestr)
    contexto = {
        'usuario': usert,
        'is_autor': False,
        'bio': '',
        'autor_id': -1,
    }

    try:
        autor = Autor.objects.get(user=usert)
        contexto['is_autor'] = True
        contexto['bio'] = autor.bio
        contexto['autor_id'] = autor.id
        contexto['autor']=autor
        contexto['has_followers'] = autor.followers.exists()
    except Autor.DoesNotExist:
        is_autor=False
        bio='.'
        autorId=-1


    return render(request, "artigos/userDetails.html", contexto)



def followers_view(request,autor_id):
    followers=Autor.objects.get(id=autor_id).followers.all()
    contexto={'followers':followers}
    return render(request,"artigos/followers.html",contexto)

def comentarios_view(request,artigo_id):
    comentarios=Artigo.objects.get(id=artigo_id).comentarios.all()
    artigoId=artigo_id
    contexto={'comentarios':comentarios,'artigo_id':artigoId}
    return render(request,"artigos/comentarios.html",contexto)

def ratings_view(request,artigo_id):
    ratings=Artigo.objects.get(id=artigo_id).ratings.all()
    artigoId=artigo_id
    contexto={'ratings':ratings,'artigo_id':artigoId}
    return render(request,"artigos/ratings.html",contexto)

def NoFollowers_view(request):
    return HttpResponse("Não tem followers")

def comentarioDetail_view(request,comentario_id):
    comentario=Comentario.objects.get(id=comentario_id)
    comentarioId=comentario_id
    contexto={'comentario':comentario,'comentario_id':comentarioId}
    return render(request,"artigos/comentarioDetail.html",contexto)
def ratingDetail_view(request,rating_id):
    rating=Rating.objects.get(id=rating_id)
    ratingId=rating_id
    contexto={'rating':rating,'rating_id':ratingId}
    return render(request,"artigos/ratingDetail.html",contexto)


@login_required(login_url='/autenticacao/loginA/')
@group_required('EditorArtigos', login_url='/autenticacao/loginA/')
def novo_artigo_view(request):
    if request.method == 'POST':
        form = ArtigoForm(request.POST or None)
        if form.is_valid():
            # Assign the current authenticated user to the autor field
            artigo = form.save(commit=False)
            artigo.autor = request.user  # Assuming 'autor' is the ForeignKey to the User model
            artigo.save()
            return redirect('artigos:index')
    else:
        form = ArtigoForm()

    context = {'form': form}
    return render(request, 'artigos/novo_artigo.html', context)


@login_required(login_url='/autenticacao/loginA/')
@group_required('EditorArtigos', login_url='/autenticacao/loginA/')
def edita_artigo_view(request, artigo_id):
    artigo = Artigo.objects.get(id=artigo_id)

    if request.POST:
        if request.user == artigo.autor:
            form = ArtigoForm(request.POST or None, instance=artigo)
            if form.is_valid():
                form.save()
                return redirect('artigos:index')
        else:
            return render(request,'artigos/error.html')
    else:
        form = ArtigoForm(instance=artigo)

    context = {'form': form, 'artigo':artigo}
    return render(request, 'artigos/edita_artigo.html', context)


@login_required(login_url='/autenticacao/loginA/')
@group_required('EditorArtigos', login_url='/autenticacao/loginA/')
def apaga_artigo_view(request, artigo_id):
    artigo = Artigo.objects.get(id=artigo_id)
    if request.user == artigo.autor:
        artigo.delete()
    else:
        return render(request,'artigos/error.html')
    return redirect('artigos:index')


@login_required(login_url='/autenticacao/loginA/')
@group_required('EditorArtigos', login_url='/autenticacao/loginA/')
def novo_comentario_view(request, artigo_id):
    artigo = Artigo.objects.get(id=artigo_id)  # Retrieve the Autor object using autor_id
    form = ComentarioForm(request.POST or None)

    if form.is_valid():

        comentario = form.save(commit=False)  # Create a Livro instance without saving to the database yet
        comentario.artigo = artigo  # Set the autor attribute of the Livro instance
        comentario.user_comentario=request.user
        comentario.save()  # Save the Livro instance to the database
        return redirect('artigos:comentarios',artigo_id=comentario.artigo.id)

    context = {'form': form}
    return render(request, 'artigos/novo_comentario.html', context)

@login_required(login_url='/autenticacao/loginA/')
@group_required('EditorArtigos', login_url='/autenticacao/loginA/')
def edita_comentario_view(request, comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)

    if request.POST:
        if request.user == comentario.user_comentario:
            form = ComentarioForm(request.POST or None, instance=comentario)
            if form.is_valid():
                form.save()
                return redirect('artigos:comentarios',artigo_id=comentario.artigo.id)
        else:
            return render(request,'artigos/error.html')
    else:
        form = ComentarioForm(instance=comentario)

    context = {'form': form, 'comentario':comentario,'artigo_id':comentario.artigo.id}
    return render(request, 'artigos/edita_comentario.html', context)

@login_required(login_url='/autenticacao/loginA/')
@group_required('EditorArtigos', login_url='/autenticacao/loginA/')
def apaga_comentario_view(request, comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)
    artigoId=comentario.artigo.id
    if request.user == comentario.user_comentario:
        comentario.delete()
    else:
        return render(request,'artigos/error.html')
    return redirect('artigos:comentarios',artigo_id=artigoId)

@login_required(login_url='/autenticacao/loginA/')
@group_required('EditorArtigos', login_url='/autenticacao/loginA/')
def novo_rating_view(request, artigo_id):
    artigo = Artigo.objects.get(id=artigo_id)  # Retrieve the Autor object using autor_id
    form = RatingForm(request.POST or None)

    if form.is_valid():

        rating= form.save(commit=False)  # Create a Livro instance without saving to the database yet
        rating.artigo = artigo  # Set the autor attribute of the Livro instance
        rating.user_rating=request.user
        rating.save()  # Save the Livro instance to the database
        return redirect('artigos:ratings',artigo_id=rating.artigo.id)

    context = {'form': form}
    return render(request, 'artigos/novo_rating.html', context)

@login_required(login_url='/autenticacao/loginA/')
@group_required('EditorArtigos', login_url='/autenticacao/loginA/')
def edita_rating_view(request, rating_id):
    rating = Rating.objects.get(id=rating_id)

    if request.POST:
        if request.user == rating.user_rating:
            form = RatingForm(request.POST or None, instance=rating)
            if form.is_valid():
                form.save()
                return redirect('artigos:ratings',artigo_id=rating.artigo.id)
        else:
            return render(request,'artigos/error.html')
    else:
        form = RatingForm(instance=rating)

    context = {'form': form, 'rating':rating}
    return render(request, 'artigos/edita_rating.html', context)

@login_required(login_url='/autenticacao/loginA/')
@group_required('EditorArtigos', login_url='/autenticacao/loginA/')
def apaga_rating_view(request, rating_id):
    rating = Rating.objects.get(id=rating_id)
    artigoID=rating.artigo.id
    if request.user == rating.user_rating:
        rating.delete()
    else:
        return render(request,'artigos/error.html')
    return redirect('artigos:ratings',artigo_id=rating.artigo.id)


#tenho que criar os templates editar e criar para ratings artigos e comentarios e tenho que criar urls par aos comentarios e ratings



