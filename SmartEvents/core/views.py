from django.shortcuts import render, HttpResponse
from .models import Evento

# Create your views here.

def home(request):
    titulo = "SmartEvents"
    return render(request,'core/index.html') 

def comunidad(request):
    titulo = "Comunidad"
    return render(request,'core/comunidad.html')

def eventos(request):
    lista_eventos = Evento.objects.all()
    tipo = {'eventos': lista_eventos}
    return render(request,'core/eventos.html', tipo )