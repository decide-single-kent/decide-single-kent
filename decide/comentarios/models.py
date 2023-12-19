# comentarios/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Comentario(models.Model):
    autor = models.CharField(max_length=100)
    texto = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)
    votos_positivos = models.IntegerField(default=0)
    votos_negativos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto

class Reporte(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.ForeignKey('comentarios.Comentario', on_delete=models.CASCADE)
    razon = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte {self.id} - {self.usuario.username}"
