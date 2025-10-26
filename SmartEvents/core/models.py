from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Evento(models.Model):
    titulo = models.CharField(max_length=30)
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=30)
    imagen = models.ImageField(upload_to='eventos/')
    valor = models.IntegerField()
    cantidad = models.IntegerField()
    asistentes = models.ManyToManyField(User, related_name='eventos_inscritos', blank=True)
    def __str__(self):
        return self.titulo
