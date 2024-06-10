
from django.shortcuts import render, redirect
from .models import *

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from autenticacao.decorators import group_required
from .forms import CursoForm, DisciplinaForm, ProjetoForm,AreaForm
# Create your views here.
def CursoLista_view(request):
    cursos=Curso.objects.all()
    contexto={'cursos':cursos}
    return render(request,"curso/listaCurso.html",contexto)


def Curso_view(request,curso_id):
    curso=Curso.objects.get(id=curso_id)
    areasCientificas=curso.areasCientificas.all()
    disciplinas=curso.disciplinas.all()

    contexto={'curso':curso,'areas':areasCientificas,'disciplinas':disciplinas}
    return render(request,"curso/curso.html",contexto)

def disciplina_details_view(request,disciplina_id):
    disciplina=Disciplina.objects.get(id=disciplina_id)
    projetos=Projeto.objects.filter(disciplina__id=disciplina_id)
    linguagens=disciplina.linguagens.all()
    contexto={'disciplina':disciplina,'projetos':projetos,'linguagens':linguagens}
    return render(request,"curso/disciplina.html",contexto)

def projeto_view(request,projeto_id):
    projeto=Projeto.objects.get(id=projeto_id)
    contexto={'projeto':projeto}
    return render(request,"curso/projeto.html",contexto)




@login_required(login_url='/autenticacao/loginC/')
@group_required('EditorCurso', login_url='/autenticacao/loginC/')
def edita_curso_view(request, curso_id):
    curso = Curso.objects.get(id=curso_id)

    if request.POST:
        form = CursoForm(request.POST or None,request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('curso:cursoDetail',curso_id=curso_id)

    else:
        form = CursoForm(instance=curso)

    context = {'form': form, 'curso':curso}
    return render(request, 'curso/edita_curso.html', context)

@login_required(login_url='/autenticacao/loginC/')
@group_required('EditorCurso', login_url='/autenticacao/loginC/')
def novo_areaCientifica_view(request, curso_id):
    curso= Curso.objects.get(id=curso_id)  # Retrieve the Autor object using autor_id
    form = AreaForm(request.POST or None,request.FILES)
    if form.is_valid():
        area = form.save(commit=False)  # Create a Livro instance without saving to the database yet
        area.curso = curso # Set the autor attribute of the Livro instance
        area.save()  # Save the Livro instance to the database
        return redirect('curso:cursoDetail',curso_id=area.curso.id)
    context = {'form': form,'curso_id':curso_id}
    return render(request, 'curso/nova_areaCientifica.html', context)


@login_required(login_url='/autenticacao/loginC/')
@group_required('EditorCurso', login_url='/autenticacao/loginC/')
def edita_areaCientifica_view(request, areacientifica_id):
    area = AreaCientifica.objects.get(id=areacientifica_id)
    if request.POST:
        form = AreaForm(request.POST or None,request.FILES, instance=area)
        if form.is_valid():
            form.save()
            return redirect('curso:cursoDetail',curso_id=area.curso.id)


    else:
        form = AreaForm(instance=area)

    context = {'form': form, 'curso_id':area.curso.id,'area':area}
    return render(request, 'curso/edita_areaCientifica.html', context)


@login_required(login_url='/autenticacao/loginC/')
@group_required('EditorCurso', login_url='/autenticacao/loginC/')
def apaga_areaCientifica_view(request, areacientifica_id):
    area= AreaCientifica.objects.get(id=areacientifica_id)
    cursoId=area.curso.id
    area.delete()

    return redirect('curso:cursoDetail',curso_id=cursoId)


@login_required(login_url='/autenticacao/loginC/')
@group_required('EditorCurso', login_url='/autenticacao/loginC/')
def novo_disciplina(request, areacientifica_id):
    area = AreaCientifica.objects.get(id=areacientifica_id)  # Retrieve the Autor object using autor_id
    form = DisciplinaForm(request.POST or None,request.FILES)

    if form.is_valid():

        disciplina = form.save(commit=False)  # Create a Livro instance without saving to the database yet
        disciplina.areaCientifica = area # Set the autor attribute of the Livro instance
        disciplina.save()  # Save the Livro instance to the database
        return redirect('curso:cursoDetail',curso_id=area.curso.id)

    context = {'form': form,'curso_id':area.curso.id,'area_id':areacientifica_id}
    return render(request, 'curso/novo_disciplina.html', context)

@login_required(login_url='/autenticacao/loginC/')
@group_required('EditorCurso', login_url='/autenticacao/loginC/')
def edita_disciplina_view(request, disciplina_id):
     disciplina = Disciplina.objects.get(id=disciplina_id)
     initial_linguagens = set(disciplina.linguagens.all())
     if request.method == 'POST':
         form = DisciplinaForm(request.POST, instance=disciplina)
         if form.is_valid():
             disciplina = form.save(commit=False)
             form.save_m2m()  # This saves the many-to-many relationships

            # Get the updated list of linguagens from the form
             updated_linguagens = set(form.cleaned_data['linguagens'])

            # Determine which linguagens to remove
             linguagens_to_remove = initial_linguagens - updated_linguagens

            # Remove the linguagens that were not selected
             for linguagem in linguagens_to_remove:
                 disciplina.linguagens.remove(linguagem)

             disciplina.save()
             return redirect('curso:disciplina', disciplina_id=disciplina.id)
     else:
         form = DisciplinaForm(instance=disciplina)

     context = {'form': form, 'disciplina': disciplina}
     return render(request, 'curso/edita_disciplina.html', context)


@login_required(login_url='/autenticacao/loginC/')
@group_required('EditorCurso', login_url='/autenticacao/loginC/')
def apaga_disciplina_view(request, disciplina_id):
    disciplina= Disciplina.objects.get(id=disciplina_id)
    cursoId=disciplina.areaCientifica.curso.id
    disciplina.delete()

    return redirect('curso:cursoDetail',curso_id=cursoId)

@login_required(login_url='/autenticacao/loginC/')
@group_required('EditorCurso', login_url='/autenticacao/loginC/')
def novo_projeto_view(request, disciplina_id):
    disciplina = Disciplina.objects.get(id=disciplina_id)  # Retrieve the Autor object using autor_id
    form = ProjetoForm(request.POST or None,request.FILES)

    if form.is_valid():

        projeto= form.save(commit=False)  # Create a Livro instance without saving to the database yet
        projeto.disciplina = disciplina # Set the autor attribute of the Livro instance

        projeto.save()  # Save the Livro instance to the database
        return redirect('curso:disciplina',disciplina_id=disciplina_id)

    context = {'form': form,'disciplina_id':disciplina_id}
    return render(request, 'curso/novo_projeto.html', context)

@login_required(login_url='/autenticacao/loginC/')
@group_required('EditorCurso', login_url='/autenticacao/loginC/')
def edita_projeto_view(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    disciplina_id = projeto.disciplina.id

    # Store the initial list of linguagens
    initial_linguagens = set(projeto.linguagensProgramacao.all())

    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            projeto = form.save(commit=False)
            form.save_m2m()  # This saves the many-to-many relationships

            # Get the updated list of linguagens from the form
            updated_linguagens = set(form.cleaned_data['linguagensProgramacao'])

            # Determine which linguagens to remove
            linguagens_to_remove = initial_linguagens - updated_linguagens

            # Remove the linguagens that were not selected
            for linguagem in linguagens_to_remove:
                projeto.linguagensProgramacao.remove(linguagem)

            projeto.save()
            return redirect('curso:projeto', projeto_id=projeto.id)
    else:
        form = ProjetoForm(instance=projeto)

    context = {'form': form, 'projeto': projeto}
    return render(request, 'curso/edita_projeto.html', context)

@login_required(login_url='/autenticacao/loginC/')
@group_required('EditorCurso', login_url='/autenticacao/loginC/')
def apaga_projeto_view(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    disciplina_id = projeto.disciplina.id
    projeto.delete()
    return redirect('curso:disciplina', disciplina_id=disciplina_id)






