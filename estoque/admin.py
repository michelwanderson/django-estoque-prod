from django.contrib import admin

# Register your models here.
from .models import Produto, MovimentacaoEstoque, Fornecedor, NotaFiscal

admin.site.register(Produto)
admin.site.register(Fornecedor)
admin.site.register(NotaFiscal)
admin.site.register(MovimentacaoEstoque)
