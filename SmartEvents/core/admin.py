from django.contrib import admin
from .models import Evento
from django.utils.html import format_html 

class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'lugar', 'valor', 'cantidad_disponible', 'listado_asistentes', 'dinero_recaudado') 
    list_filter = ('fecha', 'lugar') 
    search_fields = ('titulo', 'lugar') 

    def cantidad_disponible(self, obj):
        return obj.cantidad
    cantidad_disponible.short_description = 'Plazas Disponibles' 

    def listado_asistentes(self, obj):
 
        asistentes = obj.asistentes.all()
        if not asistentes.exists():
            return "Ninguno"
        return format_html("<br>".join([user.username for user in asistentes[:5]]) + ("<br>..." if asistentes.count() > 5 else ""))
    listado_asistentes.short_description = 'Asistentes (primeros 5)' 

    def dinero_recaudado(self, obj):
        inscritos = obj.asistentes.count()
        recaudado = inscritos * obj.valor

        return f"${recaudado:,.0f}".replace(",", ".")
    dinero_recaudado.short_description = 'Dinero Recaudado' 


admin.site.register(Evento, EventoAdmin)