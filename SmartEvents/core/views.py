from django.shortcuts import render, HttpResponse,redirect
from .models import Evento
from django.contrib.auth.forms import UserCreationForm



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
            username = form.cleaned_data.get('username')
            
            return redirect('login')
    else: 
        form = UserCreationForm()
        data = {'form': form}  
   
    return render(request,'registration/registro.html',data)