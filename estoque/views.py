
# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, MovimentacaoEstoque, ItemNotaFiscal, NotaFiscal, Fornecedor
from .forms import EntradaEstoqueForm, NotaFiscalForm, ItemNotaFiscalForm
import json


@login_required
def lista_produtos(request):
    categoria_filtro = request.GET.get('categoria')
    
    produtos = Produto.objects.all().order_by('categoria', 'nome')
    
    # Obtém categorias únicas para o dropdown
    categorias = Produto.objects.exclude(categoria__isnull=True).exclude(categoria__exact='').values_list('categoria', flat=True).distinct().order_by('categoria')

    if categoria_filtro:
        produtos = produtos.filter(categoria=categoria_filtro)

    return render(request, 'estoque/estoque.html', {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_filtro': categoria_filtro
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
            cod_barras = form.cleaned_data['cod_barras']
            observacao = form.cleaned_data['observacao']
            unidade = produto.unidade_medida  


            if cod_barras:
                produto.cod_barras = cod_barras

            nota, created = NotaFiscal.objects.get_or_create(
                numero=numero_nota,
                fornecedor=fornecedor,
                defaults={'data_emissao': data_emissao}
            )

            MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo=MovimentacaoEstoque.ENTRADA,
                quantidade=quantidade,
                nota=nota,
                observacao=observacao,
                usuario=request.user
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
    if request.method == 'POST':
        form = NotaFiscalForm(request.POST)
        if form.is_valid():
            nota = form.save()
            return redirect('entrada_nota', nota_id=nota.id)
    else:
        form = NotaFiscalForm()

    return render(request, 'estoque/criar_nota.html', {
        'form': form
    })


@login_required
def entrada_nota(request, nota_id):
    nota = get_object_or_404(NotaFiscal, id=nota_id, confirmada=False)

    if request.method == 'POST':
        form = ItemNotaFiscalForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            
            cod_barras = form.cleaned_data.get('cod_barras')
            if cod_barras:
                item.produto.cod_barras = cod_barras
                item.produto.save()
            
            item.nota = nota
            item.save()
            messages.success(request, 'Item adicionado com sucesso')
            return redirect('entrada_nota', nota_id=nota.id)
    else:
        form = ItemNotaFiscalForm()

    produtos_map = {p.id: p.cod_barras for p in Produto.objects.all() if p.cod_barras}

    return render(request, 'estoque/entrada.html', {
        'nota': nota,
        'form': form,
        'itens': nota.itens.all(),
        'produtos_map': json.dumps(produtos_map)
    })


@login_required
def excluir_item_nota(request, item_id):
    item = get_object_or_404(ItemNotaFiscal, id=item_id, nota__confirmada=False)
    nota_id = item.nota.id
    nome_produto = item.produto.nome
    item.delete()
    messages.success(request, f"Item '{nome_produto}' removido da nota.")
    return redirect('entrada_nota', nota_id=nota_id)




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
                observacao=item.observacao,
                usuario=request.user
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
            quantidade=quantidade,
            usuario=request.user
        )

        messages.success(request, 'Saída registrada')
        return redirect('saida_producao')




@login_required
def historico(request):
    movimentacoes = MovimentacaoEstoque.objects.select_related('produto', 'nota').all().order_by('-data')

    return render(request, 'estoque/historico.html', {
        'movimentacoes': movimentacoes
    })
