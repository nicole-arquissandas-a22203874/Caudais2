from django import forms
from .models import *

class BandaForm(forms.ModelForm):
  class Meta:
    model = Banda
    fields ='__all__'

    widgets = {
      'nome_banda': forms.TextInput(attrs={
          'placeholder':'Insira nome da banda',
      }),
       'foto': forms.ClearableFileInput(attrs={
          'placeholder':'Insira imagem ',

      }),

      'nacionalidade': forms.TextInput(attrs={
          'placeholder':'Insira a nacionalidade da banda ',

      }),
      'ano_criacao': forms.NumberInput(attrs={
          'placeholder':'Insira o ano de criacao ',

      }),

      'biografia': forms.Textarea(),

    }
    labels={'nome_banda':"Nome",
            "conteudo":"Conteudo",
            'foto':"Imagem",
            'nacionalidade':'Nacionalidade',
            'ano_criacao':'Ano de criação',
            'biografia':'Biografia'
        }

    help_texts={
        'biografia':'Insira uma breve biografia de 4-5 linhas.',
        }


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['titulo_Album','capa','ano_lancamento']
        widgets = {
            'titulo_Album': forms.TextInput(attrs={
            'placeholder':'Insira o titulo',
            }),

             'capa': forms.ClearableFileInput(attrs={
            'placeholder':'Insira imagem para capa',
            }),

            'ano_lancamento': forms.NumberInput(attrs={
            'placeholder':'Insira ano de lançamento',
            }),

            }
        labels={'titulo_Album':"Título",
        'capa':'Capa',
        'ano_lancamento':'Ano de lançamento',

        }
class MusicaForm(forms.ModelForm):
    class Meta:
        model = Musica
        fields = ['nome_musica','duracao','link']
        widgets = {

          'nome_musica': forms.TextInput(attrs={
          'placeholder':'Insira o nome'
          }),

          'duracao': forms.TextInput(attrs={
          'placeholder':'HH:MM:SS'
          }),

          'link': forms.URLInput(attrs={
          'placeholder':'Insira o link de spotify'
          }),

           'letra': forms.Textarea(attrs={
          'placeholder':'Insira a letra da musica'
          }),


          }
        labels={'link':"Spotify Link",'duracacao':'Duração','nome_musica':'Nome',
        'letra':'Letra'
        }


