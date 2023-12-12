from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Comentario
from .forms import ComentarioForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='/no_autenticado')
def ver_comentarios(request):
    comentarios = Comentario.objects.all()
    return render(request, 'comentarios/ver_comentarios.html', {'comentarios': comentarios})


@login_required(login_url='/no_autenticado')
def agregar_comentario(request):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_comentarios')
    else:
        form = ComentarioForm()
    return render(request, 'comentarios/agregar_comentario.html', {'form': form})

@login_required(login_url='/no_autenticado')
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

@login_required(login_url='/no_autenticado')
def borrar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    tiempo_transcurrido = timezone.now() - comentario.timestamp
    if tiempo_transcurrido.total_seconds() > 300:  # 5 minutos en segundos
        return render(request, 'comentarios/no_borrar_comentario.html')
    
    comentario.delete()
    return redirect('ver_comentarios')

@login_required(login_url='/no_autenticado')
def votar_comentario(request, comentario_id, voto):
    try:
        comentario = Comentario.objects.get(pk=comentario_id)

        # Obtener el voto actual del usuario (si existe)
        voto_anterior = request.session.get(f'voto_{comentario_id}', None)

        if voto_anterior is None:
            # El usuario no ha votado antes, vota positivo
            if voto == 'positivo':
                comentario.votos_positivos = 1
            else:
                comentario.votos_negativos =1
                
        else:
            # El usuario ya ha votado
            if voto == 'negativo':
                # Votó negativo, resta 1 a positivos y suma 1 a negativos (no puede ser menos de 0)
                comentario.votos_positivos = max(0, comentario.votos_positivos - 1)
                comentario.votos_negativos = 1
                
            else :
                comentario.votos_negativos= max(0, comentario.votos_negativos - 1)
                comentario.votos_positivos = 1

            # Guardar el voto actual en la sesión del usuario
            request.session[f'voto_{comentario_id}'] = voto
            comentario.save()

            return JsonResponse({
                'success': True,
                'votos_positivos': comentario.votos_positivos,
                'votos_negativos': comentario.votos_negativos
            })

        # Guardar el voto actual en la sesión del usuario
        request.session[f'voto_{comentario_id}'] = voto
        comentario.save()

        return HttpResponse('Votos actualizados correctamente')


    except Comentario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Comentario no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def no_autenticado_view(request):
        return render(request, 'comentarios/no_autenticado.html')
