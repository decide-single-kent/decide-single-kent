# En comentarios/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Comentario
from comentarios.views import ver_comentarios

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'texto', 'ver_comentarios_button')

    def ver_comentarios_button(self, obj):
        url = reverse('ver_comentarios')  
        return format_html('<a class="button" href="{}">Ver Comentarios</a>', url)
