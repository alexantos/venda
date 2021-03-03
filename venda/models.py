from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=16)
    valor = models.FloatField()


class Venda(models.Model):
    data = models.DateTimeField(auto_now=True)
    lucro_total = models.FloatField(null=True)#false
    situacao = models.BooleanField(null=True)#false

    produto_vendas = []


class ProdutoVenda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    venda = models.ForeignKey(Venda, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    lucro = models.FloatField()
