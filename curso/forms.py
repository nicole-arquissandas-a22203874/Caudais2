from django import forms
from .models import Curso, Disciplina, Projeto, AreaCientifica,LinguagemProgramacao

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'apresentacao', 'objetivos', 'competencias']

class DisciplinaForm(forms.ModelForm):

    class Meta:
        model = Disciplina
        linguagens = forms.ModelMultipleChoiceField(queryset=LinguagemProgramacao.objects.all(),widget=forms.CheckboxSelectMultiple,required=False)
        fields = ['nome', 'ano', 'semestre', 'ects', 'curricularIUnitReadableCode','linguagens']

class ProjetoForm(forms.ModelForm):

    class Meta:
        model = Projeto

        linguagensProgramacao = forms.ModelMultipleChoiceField(
        queryset=LinguagemProgramacao.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
        fields = ['nome', 'descricao', 'conceitosAplicados', 'tecnologiasUsadas', 'imagem', 'video_demo', 'repositorio_github', 'disciplina', 'linguagensProgramacao']

class AreaForm(forms.ModelForm):
    class Meta:
        model = AreaCientifica
        fields = ['nome']
