from django.urls import path
from .views import *

app_name = 'venda'

urlpatterns = [
    path('teste_vendas', teste_vendas, name='teste_vendas'),
    path('vendas', vendas, name="vendas"),
    path('cadastraProduto', cadastraProduto, name="cadastraProduto"),
    path('deletaProdutoVenda/<int:id>/<int:page>', deletaProdutoVenda, name="deletaProdutoVenda")
]
