# --- Importaciones necesarias ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required # Para proteger vistas
from django.contrib import messages # Para mostrar mensajes
from .models import Evento # Tu modelo Evento

# --- Tus vistas existentes ---
def home(request):
    # Podrías querer pasar algún evento destacado a la plantilla index.html
    # evento_destacado = Evento.objects.filter(fecha__gte=timezone.now()).order_by('fecha').first() # Necesitarías importar timezone
    # context = {'evento_destacado': evento_destacado}
    # return render(request, 'core/index.html', context)
    return render(request, 'core/index.html') # Versión simple

def eventos(request):
    lista_eventos = Evento.objects.all().order_by('fecha') # Ordenar por fecha
    return render(request, 'core/eventos.html', {'eventos': lista_eventos})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.') # Mensaje de éxito
            return redirect('login')
        else:
            # Los errores se mostrarán automáticamente por {{ form.as_p }} en la plantilla
            pass
    else: # GET
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
                # Intenta redirigir a la página a la que querían ir, o al index
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.') # Mensaje de error
        else:
             messages.error(request, 'Nombre de usuario o contraseña incorrectos.') # Mensaje de error
    else: # GET
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@require_POST # Asegura que el logout sea por POST
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.') # Mensaje informativo
    return redirect('index')

# --- NUEVAS Vistas para Inscripción y Mis Eventos ---

@login_required # Requiere login
def inscribir_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    usuario = request.user

    # Solo procesar si es método POST (desde el formulario)
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
            # Podrías redirigir a 'mis_eventos' después de inscribirse
            # return redirect('mis_eventos')

    # Si no es POST o después de procesar, redirigir a la lista de eventos
    return redirect('eventos')


@login_required # Requiere login
def mis_eventos(request):
    # Usamos el related_name 'eventos_inscritos'
    eventos_inscritos = request.user.eventos_inscritos.all().order_by('fecha')
    context = {
        'eventos': eventos_inscritos
    }
    return render(request, 'core/mis_eventos.html', context)