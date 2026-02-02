from django import forms
from .models import Produto, Fornecedor, NotaFiscal, ItemNotaFiscal

class EntradaEstoqueForm(forms.Form):
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedor.objects.all(),
        label="Fornecedor"
    )
    numero_nota = forms.CharField(label="Número da Nota Fiscal")
    data_emissao = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data de Emissão"
    )
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        label="Produto"
    )
    quantidade = forms.IntegerField(
        min_value=1,
        label="Quantidade"
    )
    cod_barras = forms.CharField(
        required=False,
        label="Código de Barras"
    )
    observacao = forms.CharField(
        required=False,
        label="Observação"
    )


class NotaFiscalForm(forms.ModelForm):
    class Meta:
        model = NotaFiscal
        fields = ['numero', 'fornecedor']
        labels = {'numero': 'Número da Nota', 'fornecedor': 'Fornecedor'}

class ItemNotaFiscalForm(forms.ModelForm):
    cod_barras = forms.CharField(
        required=False,
        label="Código de Barras",
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    class Meta:
        model = ItemNotaFiscal
        fields = ['produto', 'quantidade', 'observacao']