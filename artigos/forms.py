from django import forms
from .models import *

class ArtigoForm(forms.ModelForm):
  class Meta:
    model = Artigo
    fields = ['titulo','conteudo']

    widgets = {
      'titulo': forms.TextInput(attrs={
          'placeholder':'Insira título',
      }),
       'conteudo': forms.Textarea(attrs={
          'placeholder':'Insira conteudo',
      }),

    }
    labels={'titulo':"Título",
            "conteudo":"Conteudo"
        }




class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
            'placeholder':'Insira o seu comentario',
            }),
            }
        labels={'texto':"Comentario",

        }
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['nota']
        widgets = {

          'nota': forms.NumberInput(attrs={
          'placeholder':'Insira o seu rating','max':10,'min':0
          }),
          }
        labels={'nota':"Nota",
        }


