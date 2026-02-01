from django import forms
from estoque.models import Produto

class SaidaProducaoForm(forms.Form):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        label="Produto"
    )
    quantidade = forms.IntegerField(
        min_value=1,
        label="Quantidade a retirar"
    )
    data_retirada = forms.DateField(
        widget=forms.SelectDateWidget,
        label="Data de Retirada"
    )