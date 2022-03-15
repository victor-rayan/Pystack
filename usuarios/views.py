from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario
import hashlib


# Create your views here.

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})


def login(request):
    return render(request, 'login.html')

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    valida_user = Usuario.objects.filter(email=email)
    if len(senha) < 4 or len(senha)> 20:
        return redirect('/auth/cadastro?status=1')

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro?status=2')

    if len(valida_user)>0:
        return redirect('/auth/cadastro?status=3')  

    try:
        senha = hashlib.sha256(senha.encode()).hexdigest() 
        usuario = Usuario(nome = nome,
                       senha = senha, 
                       email = email)
        usuario.save()
        return redirect('/auth/cadastro?status=4')
    except:
        return HttpResponse ('erro tente novamente mais tarde') 
