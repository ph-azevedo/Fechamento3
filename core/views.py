from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from core.models import Movfin, Nfiscal, Ctrped, Cliforn, Orc
from django.contrib import messages

# Create your views here.

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