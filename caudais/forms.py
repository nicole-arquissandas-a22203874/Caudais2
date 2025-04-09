from django import forms

class RegiaoForm(forms.Form):
    regiao_nome = forms.CharField(
        max_length=100,
        label='Nome',
        widget=forms.TextInput(attrs={'placeholder': 'Insira o nome da região'})
    )
    regiao_localidade = forms.CharField(
        max_length=100,
        label='Localidade',
        widget=forms.TextInput(attrs={'placeholder': 'Insira a localidade da região'})
    )

class PontoMedidaForm(forms.Form):
    tipo_medidor = forms.CharField(
        max_length=100,
        label='Tipo de Medidor',
        widget=forms.TextInput(attrs={'placeholder': 'Insira o tipo de medidor'})
    )
    latitude = forms.FloatField(
        required=False,
        label='Latitude (Opcional)',
        widget=forms.NumberInput(attrs={'placeholder': 'Insira a latitude'})
    )
    longitude = forms.FloatField(
        required=False,
        label='Longitude (Opcional)',
        widget=forms.NumberInput(attrs={'placeholder': 'Insira a longitude '})
    )

class ArquivoExcelForm(forms.Form):
    arquivo_excel = forms.FileField(
        label='Arquivo Excel',
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Selecione um arquivo Excel'})
    )
