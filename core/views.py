from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from core.models import Movfin, Nfiscal, Ctrped, Cliforn, Orc, Listas, AuxListas, Livros, Estoque
from django.contrib import messages
import datetime
from openpyxl import Workbook


def index(request):
    context = {}
    if request.user.is_authenticated == True:
        auth = True
    username = request.user.get_username()
    if username:
        context = {
            'username': User.objects.get(username=username).first_name,
            'auth': auth
        }

    return render(request, 'index.html', context)

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(username=username, password=password)
        if usuario:
            auth_login(request, usuario)
            return redirect('index')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'login.html', {'form_login': form_login})


@login_required
def fechamento(request):
    context = {}
    if 'POST' == request.method:
        if request.POST.get('circulo'):
            empresa = '01'
        elif request.POST.get('athenas'):
            empresa = '02'
        data = request.POST.get('date').split('-')
        ano = data[0]
        mes = data[1]
        query_notas = Nfiscal.objects.filter(dtemissao__month=mes, dtemissao__year=ano, filial=empresa, nossanf=1).using('vlbooks')
        for nf in query_notas:
            forn = Cliforn.objects.filter(codigo=nf.cliforn).using('vlbooks')[0].nome
        context['query'] = query_notas


        return render(request, 'fechamento.html', context)

    else:
            return render(request, 'fechamento.html')

@login_required()
def logout(request):
    auth_logout(request)
    return redirect('/conta/login')

@login_required()
def pedidos(request):
    context = {}
    peds = Ctrped.objects.filter(env='P', stsite=2).using('vlbooks').exclude(nped=9098).exclude(nped=11700).exclude(nped=13004).exclude(nped=12918)
    context['peds'] = peds

    return render(request, 'pedidos.html', context)

@login_required()
def itens_pendentes(request):
    context = {}
    pedidos_pendentes = Ctrped.objects.filter(env='P', stsite=2).using('vlbooks').exclude(nped=9098).exclude(nped=11700).exclude(nped=13004).exclude(nped=12918)
    context['peds'] = pedidos_pendentes
    return render(request, 'pendentes.html', context)

@login_required()
def gera_lista(request):
    context = {}
    last = Listas.objects.last()

    if request.method == 'GET':
        context['lastdate'] = last.data
        if last.data.day == datetime.datetime.now().day:
            context['listahoje'] = True
        else:
            context['listahoje'] = False
        return render(request, 'gera_listas.html', context)

    elif request.method == "POST":
        lista = Listas()
        lista.save()
        lista_atual = Listas.objects.last()
        pedidos_pendentes = Ctrped.objects.filter(env='P', stsite=2).using('vlbooks').exclude(nped=9098).exclude(nped=11700).exclude(nped=13004).exclude(nped=12918)
        dict_itens = {}
        for pedido in pedidos_pendentes:
            item = Orc.objects.filter(nped=pedido.nped).using('vlbooks')
            for i in item:
                query = Livros.objects.filter(nbook=i.nbook).using('vlbooks').first()
                query2 = Ctrped.objects.filter(nped=pedido.nped).using('vlbooks').first().vendedor
                estoque = Estoque.objects.filter(nbook=i.nbook).using('vlbooks').first().disp
                estoque_cat = Estoque.objects.filter(nbook=i.nbook).using('vlbooks').first().disp_ff
                valor = Ctrped.objects.filter(nped=pedido.nped).using('vlbooks').first().vlped
                context['valor'] = valor

                itemped = AuxListas(isbn=query.isbn1, qtde=i.qtde, pedido=i.it_mktplace, lista_id=lista_atual.pk, local=query2)

                # else:
                #     estoque_cat = Estoque.objects.filter(nbook=i.nbook).using('vlbooks').first().disp_ff
                #     if estoque_cat >= i.qtde:
                #         itemped = AuxListas(isbn=query.isbn1, qtde=i.qtde, pedido=i.it_mktplace,
                #                             lista_id=lista_atual.pk, local=query2, fornecedor='Catavento')
                #     else:
                #         itemped = AuxListas(isbn=query.isbn1, qtde=i.qtde, pedido=i.it_mktplace, lista_id=lista_atual.pk, local=query2)
                itemped.save()
            query = AuxListas.objects.filter(lista_id=lista_atual.pk).using('default')
            dict_itens = {}
            for item in query:
                if item.isbn in dict_itens:
                    dict_itens[item.isbn] = dict_itens[item.isbn] + item.qtde
                else:
                    dict_itens[item.isbn] = item.qtde
        query_forn = AuxListas.objects.filter(lista_id=lista_atual.pk).using('default')
        for i in query_forn:
            nbook = Livros.objects.filter(isbn1=i.isbn).using('vlbooks').first().nbook
            estoque_cat = Estoque.objects.filter(nbook=nbook).using('vlbooks').first().disp_ff
            estoque = Estoque.objects.filter(nbook=nbook).using('vlbooks').first().disp
            estoque_tt = estoque_cat + estoque
            if int(dict_itens[i.isbn]) <= estoque:
                i.fornecedor = 'Circulo'
                i.save()

            elif int(dict_itens[i.isbn]) > estoque:
                if int(dict_itens[i.isbn]) <= estoque_cat:
                    i.fornecedor = 'Catavento'
                    i.save()

                elif int(dict_itens[i.isbn]) > estoque_cat and int(dict_itens[i.isbn]) <= estoque_tt:
                    i.fornecedor = 'Circulo e Catavento'
                    i.save()
            i.save()
        query = AuxListas.objects.filter(lista_id=lista_atual.pk).using('default')
        context['lista'] = lista_atual
        context['produtos'] = query

        return render(request, 'gera_listas.html', context)