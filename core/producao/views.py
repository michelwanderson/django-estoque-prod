from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from estoque.models import Produto, MovimentacaoEstoque
from .forms import SaidaProducaoForm


@login_required
def producao(request):
    if request.method == 'POST':
        form = SaidaProducaoForm(request.POST)

        if form.is_valid():
            produto = form.cleaned_data['produto']
            quantidade = form.cleaned_data['quantidade']

            # Validação baseada no estoque atual
            if quantidade > produto.quantidade:
                messages.error(
                    request,
                    f"Estoque insuficiente! Disponível: {produto.quantidade}"
                )
            else:
                # 🔹 Cria o histórico
                MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo=MovimentacaoEstoque.SAIDA,
                    quantidade=quantidade,
                    observacao="Saída para produção"
                )

                # 🔹 Atualiza o saldo (cache)
                produto.quantidade -= quantidade
                produto.save()

                messages.success(
                    request,
                    "Saída registrada com sucesso!"
                )
    else:
        form = SaidaProducaoForm()

    produtos = Produto.objects.all().order_by('categoria', 'nome')

    return render(request, 'producao/producao.html', {
        'form': form,
        'produtos': produtos
    })
