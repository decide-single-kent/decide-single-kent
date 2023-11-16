from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Comentario(models.Model):
    autor = models.CharField(max_length=100)
    texto = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.texto