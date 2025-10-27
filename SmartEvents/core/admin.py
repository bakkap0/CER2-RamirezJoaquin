from django.contrib import admin
from .models import Evento
from django.utils.html import format_html

class AsistenteInline(admin.TabularInline):
    model = Evento.asistentes.through 
    verbose_name = "Asistente"
    verbose_name_plural = "Asistentes Registrados (Registros)"
    extra = 0 
    
    readonly_fields = ('user',) 
    fields = ('user',) 
 
    def get_readonly_fields(self, request, obj=None):
         return ('get_username',) 

    def get_username(self, instance):
         
         return instance.user.username
    get_username.short_description = 'Usuario' 


    fields = ('get_username',)
    readonly_fields = ('get_username',)



class EventoAdmin(admin.ModelAdmin):

    list_display = ('titulo', 'fecha', 'lugar', 'valor', 'cantidad_disponible', 'dinero_recaudado')
    list_filter = ('fecha', 'lugar')
    search_fields = ('titulo', 'lugar')

    inlines = [AsistenteInline]

    def cantidad_disponible(self, obj):
        return obj.cantidad
    cantidad_disponible.short_description = 'Plazas Disponibles'

    def dinero_recaudado(self, obj):
        inscritos = obj.asistentes.count()
        recaudado = inscritos * obj.valor
        return f"${recaudado:,.0f}".replace(",", ".")
    dinero_recaudado.short_description = 'Dinero Recaudado'

admin.site.register(Evento, EventoAdmin)