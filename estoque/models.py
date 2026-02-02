from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=150)
    categoria = models.CharField(max_length=20, blank=True, null=True) 
    cod_barras = models.CharField(max_length=50, blank=True, null=True, unique=True)
    unidade_medida = models.CharField(
        max_length=10,
        choices=[
            ('UN', 'Unidade'),
            ('KG', 'Quilo'),
            ('LT', 'Litro'),
            ('M', 'Metro'),
            ('CX', 'Caixa'),
            ('PC', 'Pacote'),
            ('ML', 'Mililitro'),
            ('M2', 'Metro Quadrado'),
            ('M3', 'Metro Cúbico'),
            ('G', 'Grama'),
        ]
    )
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nome

    

class Fornecedor(models.Model):
    nome = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome

    


class NotaFiscal(models.Model):
    numero = models.CharField(max_length=50)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    data_emissao = models.DateField(auto_now_add=True)
    confirmada = models.BooleanField(default=False)

    def __str__(self):
        return f"NF {self.numero} - {self.fornecedor}"


class ItemNotaFiscal(models.Model):
    nota = models.ForeignKey(NotaFiscal, related_name='itens', on_delete=models.CASCADE)

    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.produto} - {self.quantidade}"



class MovimentacaoEstoque(models.Model):
    ENTRADA = 'E'
    SAIDA = 'S'

    TIPO_CHOICES = [
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saída'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True, verbose_name='Data da Movimentação')
    observacao = models.TextField(blank=True, null=True)

    nota = models.ForeignKey(
        NotaFiscal,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.produto} {self.tipo} {self.quantidade}"
