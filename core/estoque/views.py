
# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, MovimentacaoEstoque, ItemNotaFiscal, NotaFiscal, Fornecedor
from .forms import EntradaEstoqueForm


@login_required
def lista_produtos(request):
    produtos = Produto.objects.all().order_by('categoria', 'nome')
    return render(request, 'estoque/lista_produtos.html', {
        'produtos': produtos
    })


@login_required
def entrada_estoque(request):
    unidade = None

    if request.method == 'POST':
        form = EntradaEstoqueForm(request.POST)

        if form.is_valid():
            fornecedor = form.cleaned_data['fornecedor']
            numero_nota = form.cleaned_data['numero_nota']
            data_emissao = form.cleaned_data['data_emissao']
            produto = form.cleaned_data['produto']
            quantidade = form.cleaned_data['quantidade']
            observacao = form.cleaned_data['observacao']

            unidade = produto.unidade_medida  # 👈 aqui

            nota, created = NotaFiscal.objects.get_or_create(
                numero=numero_nota,
                fornecedor=fornecedor,
                defaults={'data_emissao': data_emissao}
            )

            MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo=MovimentacaoEstoque.ENTRADA,
                quantidade=quantidade,
                nota_fiscal=nota,
                observacao=observacao
            )

            produto.quantidade += quantidade
            produto.save()

            messages.success(
                request,
                f"Entrada registrada: {quantidade} {produto.unidade_medida} de {produto.nome}"
            )
    else:
        form = EntradaEstoqueForm()

    return render(request, 'estoque/entrada.html', {
        'form': form,
        'unidade': unidade
    })


@login_required
def criar_nota(request):
    fornecedores = Fornecedor.objects.all()

    if request.method == 'POST':
        numero = request.POST.get('numero')
        fornecedor_id = request.POST.get('fornecedor')

        if not numero or not fornecedor_id:
            messages.error(request, 'Preencha todos os campos')
            return redirect('criar_nota')

        nota = NotaFiscal.objects.create(
            numero=numero,
            fornecedor_id=fornecedor_id
        )

        return redirect('entrada_nota', nota_id=nota.id)

    return render(request, 'estoque/criar_nota.html', {
        'fornecedores': fornecedores
    })


@login_required
def entrada_nota(request, nota_id):
    nota = get_object_or_404(NotaFiscal, id=nota_id, confirmada=False)
    produtos = Produto.objects.all()

    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        quantidade = request.POST.get('quantidade')
        observacao = request.POST.get('observacao')

        if not produto_id or not quantidade:
            messages.error(request, 'Informe produto e quantidade')
            return redirect('entrada_nota', nota_id=nota.id)

        ItemNotaFiscal.objects.create(
            nota=nota,
            produto_id=produto_id,
            quantidade=quantidade,
            observacao=observacao
        )

        messages.success(request, 'Item adicionado')
        return redirect('entrada_nota', nota_id=nota.id)

    return render(request, 'estoque/entrada.html', {
        'nota': nota,
        'produtos': produtos,
        'itens': nota.itens.all()
    })




@login_required
def confirmar_nota(request, nota_id):
    nota = get_object_or_404(NotaFiscal, id=nota_id, confirmada=False)

    with transaction.atomic():
        for item in nota.itens.all():
            produto = item.produto
            produto.quantidade += item.quantidade
            produto.save()

            # aqui depois você liga com o histórico de movimentação
            MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo=MovimentacaoEstoque.ENTRADA,
                quantidade=item.quantidade,
                nota=nota,
                observacao=item.observacao
            )

        nota.confirmada = True
        nota.save()

    return redirect('lista_produtos')




@login_required
def estoque_atual(produto):
    entradas = MovimentacaoEstoque.objects.filter(
        produto=produto,
        tipo='E'
    ).aggregate(total=Sum('quantidade'))['total'] or 0

    saidas = MovimentacaoEstoque.objects.filter(
        produto=produto,
        tipo='S'
    ).aggregate(total=Sum('quantidade'))['total'] or 0

    return entradas - saidas



@login_required
def saida_producao(request):
    if request.method == 'POST':
        produto_id = request.POST['produto']
        quantidade = Decimal(request.POST['quantidade'])

        produto = Produto.objects.get(id=produto_id)
        estoque = estoque_atual(produto)

        if quantidade > estoque:
            messages.error(request, 'Estoque insuficiente')
            return redirect('saida_producao')

        MovimentacaoEstoque.objects.create(
            produto=produto,
            tipo='S',
            quantidade=quantidade
        )

        messages.success(request, 'Saída registrada')
        return redirect('saida_producao')




@login_required
def historico(request):
    movimentacoes = MovimentacaoEstoque.objects.select_related('produto', 'nota').all().order_by('-data')

    return render(request, 'estoque/historico.html', {
        'movimentacoes': movimentacoes
    })
