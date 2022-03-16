from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Cursos

# Create your views here.

def home(request):
    if request.session.get('usuario'):
        cursos = Cursos.objects.all()
        request_usuario = request.session.get('usuario')
        return render(request, 'home.html',{'cursos': cursos, 'request_usuario':request_usuario})
    else:
        return redirect('/auth/login?status=2')    

