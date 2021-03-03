from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator


def teste_vendas(requisicao):
    return render(requisicao, 'teste_vendas.html')


def vendas(requisicao):
    pesquisa = requisicao.GET.get('pesquisa', '')
    id_venda = requisicao.GET.get('venda', '')
    nomeModal = ''
    modal_venda = ''
    modal_lista_produtos = ''
    if pesquisa:
        produtos_banco = Produto.objects.filter(nome__contains=pesquisa)
        nomeModal = 'modalJ'
        modal_venda = 'true'
    else:
        produtos_banco = Produto.objects.all()

    if id_venda:
        venda_modal = Venda.objects.get(id=id_venda)
        modal_lista_produtos = 'true'
        venda_modal.produto_vendas = []
        for produto_venda in ProdutoVenda.objects.filter(venda=venda_modal):
            venda_modal.produto_vendas.append(produto_venda)
    else:
        venda_modal = None

    if requisicao.method == 'POST':
        venda = Venda()
        if requisicao.POST.get('fiado'):
            venda.situacao = True
        else:
            venda.situacao = False
        venda.save()
        venda.lucro_total = 0
        for produto in produtos_banco:
            if requisicao.POST.get('produto_' + str(produto.id), None):
                produto_venda = ProdutoVenda()
                if requisicao.POST['quantidade_' + str(produto.id)]:
                    produto_venda.quantidade = requisicao.POST['quantidade_' + str(produto.id)]
                produto_venda.venda = venda
                produto_venda.produto = Produto.objects.get(id=produto.id)
                produto_venda.lucro = float(produto_venda.quantidade) * produto_venda.produto.valor
                venda.lucro_total = produto_venda.lucro + venda.lucro_total
                produto_venda.save()
        venda.save()
        return redirect('venda:vendas')

    vendas_banco = Venda.objects.all()
    for venda in vendas_banco:
        venda.produto_vendas = []
        for produto_venda in ProdutoVenda.objects.filter(venda=venda):
            venda.produto_vendas.append(produto_venda)
    page = requisicao.GET.get('page', 1)
    paginator = Paginator(vendas_banco, 8)
    vendas_banco = paginator.page(page)
    contexto = {
        'produtos': produtos_banco,
        'vendas': vendas_banco,
        'numero_paginas': vendas_banco.paginator.num_pages - 1,
        'nomeModal': nomeModal,
        'modalAbrir': 'true',
        'modal_venda': modal_venda,
        'pesquisa': pesquisa,
        'venda_modal': venda_modal,
        'modal_lista_produtos': modal_lista_produtos
    }
    print('Chamou vendas')
    return render(requisicao, 'vendas.html', contexto)


def cadastraProduto(requisicao):
    if requisicao.method == 'POST':
        produto = Produto()
        if requisicao.POST['nome']:
            produto.nome = requisicao.POST['nome']
        if requisicao.POST['valor']:
            produto.valor = requisicao.POST['valor'].replace(',', '.')
        produto.save()
    return redirect('venda:vendas')


def deletaProdutoVenda(requisicao, id, page):
    if requisicao.method == 'POST':
        venda = Venda.objects.get(id=id)
        produtos_vendas = ProdutoVenda.objects.filter(venda=venda)
        for produto_venda in produtos_vendas:
            produto_venda.delete()
        venda.delete()
        response = redirect('venda:vendas')
        # response['Location'] += '?' + 'page=' + str(page)
    return response
