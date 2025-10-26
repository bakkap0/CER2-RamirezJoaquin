
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Evento 
from django.utils import timezone

def home(request):
    evento_destacado = None 

    if request.user.is_authenticated:
        evento_destacado = Evento.objects.filter(
            fecha__gte=timezone.now(),  
            asistentes=request.user     
        ).order_by('fecha').first()     

    if not evento_destacado:
        evento_destacado = Evento.objects.filter(
            fecha__gte=timezone.now()  
        ).order_by('fecha').first()   

    context = {'evento_destacado': evento_destacado}
    return render(request, 'core/index.html', context)


def eventos(request):
    lista_eventos = Evento.objects.all().order_by('fecha') 
    return render(request, 'core/eventos.html', {'eventos': lista_eventos})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.') 
            return redirect('login')
        else:
            pass
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.') 
        else:
             messages.error(request, 'Nombre de usuario o contraseña incorrectos.') 
    else: 
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@require_POST 
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.') 
    return redirect('index')



@login_required 
def inscribir_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    usuario = request.user

    if request.method == 'POST':
        if usuario in evento.asistentes.all():
            messages.warning(request, f'Ya estás inscrito en "{evento.titulo}".')
        elif evento.cantidad <= 0:
            messages.error(request, f'Lo sentimos, no quedan cupos para "{evento.titulo}".')
        else:
            evento.asistentes.add(usuario)
            evento.cantidad -= 1
            evento.save()
            messages.success(request, f'¡Te has inscrito exitosamente en "{evento.titulo}"!')

    return redirect('eventos')


@login_required 
def mis_eventos(request):
    eventos_inscritos = request.user.eventos_inscritos.all().order_by('fecha')
    context = {
        'eventos': eventos_inscritos
    }
    return render(request, 'core/mis_eventos.html', context)

@login_required 
@require_POST   
def anular_inscripcion(request, evento_id):

    evento = get_object_or_404(Evento, id=evento_id)
    usuario = request.user

    if usuario in evento.asistentes.all():
        evento.asistentes.remove(usuario)
        evento.cantidad += 1
        evento.save()
        messages.success(request, f'Has anulado tu inscripción para "{evento.titulo}" correctamente.')
    else:
        messages.warning(request, f'No estabas inscrito en "{evento.titulo}".')
    return redirect('mis_eventos')