from django.shortcuts import render, HttpResponse,redirect
from .models import Evento
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,authenticate,logout


def home(request):
    titulo = "SmartEvents"
    return render(request,'core/index.html') 

#def comunidad(request):
   # titulo = "Comunidad"
    #return render(request,'core/comunidad.html')

def eventos(request):
    lista_eventos = Evento.objects.all()
    tipo = {'eventos': lista_eventos}
    return render(request,'core/eventos.html', tipo )

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    data = {'form': form}
    return render(request, 'core/registro.html', data)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('')  
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})
