from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Comentario
from .forms import ComentarioForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponseForbidden




def ver_comentarios(request):
    comentarios = Comentario.objects.all()
    return render(request, 'comentarios/ver_comentarios.html', {'comentarios': comentarios})

def agregar_comentario(request):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_comentarios')
    else:
        form = ComentarioForm()
    return render(request, 'comentarios/agregar_comentario.html', {'form': form})

def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    tiempo_transcurrido = timezone.now() - comentario.timestamp
    if tiempo_transcurrido.total_seconds() > 300:  # 5 minutos en segundos
        return render(request, 'comentarios/no_editar_comentario.html')
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('ver_comentarios')
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, 'comentarios/editar_comentario.html', {'form': form, 'comentario': comentario})

def borrar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    tiempo_transcurrido = timezone.now() - comentario.timestamp
    if tiempo_transcurrido.total_seconds() > 300:  # 5 minutos en segundos
        return render(request, 'comentarios/no_borrar_comentario.html')
    
    comentario.delete()
    return redirect('ver_comentarios')