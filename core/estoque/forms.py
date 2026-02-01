from django import forms
from .models import Produto, Fornecedor

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
    observacao = forms.CharField(
        required=False,
        label="Observação"
    )
