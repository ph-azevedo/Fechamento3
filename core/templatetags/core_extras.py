from django import template
from core.models import Cliforn, Orc, Livros, Ctrped, Estoque
register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return f'{{{str(arg1)}{str(arg2)} }}'

@register.filter
def fornecedor(arg1):
    nome = Cliforn.objects.filter(codigo=arg1).using('vlbooks')[0].nome
    return nome

@register.filter
def roundcash(arg1):
    valor = round(arg1, 2)
    return valor

@register.filter
def calcula_final(arg1, arg2):
    final = round(arg1 - arg2, 2)
    return final

@register.filter
def get_cgc(arg1):
    cgc = Cliforn.objects.filter(codigo=arg1).using('vlbooks')[0].cgc
    return str(cgc)

@register.filter
def get_nbook(arg1):
    query = Orc.objects.filter(nped=arg1).using('vlbooks')[0].nbook
    return query

@register.filter
def get_qtd(arg1):
    query = Orc.objects.filter(nped=arg1).using('vlbooks')[0]
    return query.qtde

@register.filter
def get_titulo(arg1):
    query = Livros.objects.filter(nbook=arg1).using('vlbooks').first().title
    return query

@register.filter
def get_isbn(arg1):
    query = Livros.objects.filter(nbook=arg1).using('vlbooks').first().isbn1
    return query

@register.filter
def get_pedmktplace(arg1):
    query = Orc.objects.filter(nped=arg1).using('vlbooks')[0]
    return query.it_mktplace


@register.filter
def checar_estoque(arg1):
    query = Estoque.objects.filter(nbook=arg1).using('vlbooks').first().disp
    return query
@register.filter
def checar_catavento(arg1):
    query = Estoque.objects.filter(nbook=arg1).using('vlbooks').first().disp
    return query

@register.filter
def plataforma(arg1):
    query = Ctrped.objects.filter(nped=arg1).using('vlbooks').first().vendedor
    if query == "MELI":
        return "Mercado Livre"
    elif query == "SITE_TRAY":
        return 'Site'
    else:
        return query