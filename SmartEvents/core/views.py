from django.shortcuts import render, redirect
from .models import Evento
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout   
from django.views.decorators.http import require_POST   


def home(request):
    return render(request, 'core/index.html')

def eventos(request):
    lista_eventos = Evento.objects.all()
    return render(request, 'core/eventos.html', {'eventos': lista_eventos})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  # pasa request
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@require_POST
def logout_view(request):
    auth_logout(request)
    return redirect('index')
