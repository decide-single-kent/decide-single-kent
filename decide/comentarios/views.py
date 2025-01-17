
from django.shortcuts import render

from django.shortcuts import redirect
from .models import Comentario
from .forms import ComentarioForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .bad_words import contiene_palabra_inapropiada
from .models import Reporte
from voting.models import Voting


@login_required(login_url='/no_autenticado')
def ver_comentarios(request):
    comentarios = Comentario.objects.all()
    votaciones = Voting.objects.filter(end_date__isnull=False)
    return render(request, 'comentarios/ver_comentarios.html', {'comentarios': comentarios,'votings': votaciones})


@login_required(login_url='/no_autenticado')
def agregar_comentario(request):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            form.instance.autor = request.user
            nuevo_comentario = form.cleaned_data['texto']

            if contiene_palabra_inapropiada(nuevo_comentario):
                messages.warning(request, 'Tu comentario contiene palabras inapropiadas y puede ser eliminado. ¡Por favor, sé respetuoso!')
                return redirect('ver_comentarios')
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
            nuevo_comentario = form.cleaned_data['texto']

            if contiene_palabra_inapropiada(nuevo_comentario):
                messages.warning(request, 'Tu comentario contiene palabras inapropiadas y puede ser eliminado. ¡Por favor, sé respetuoso!')

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
def crear_reporte(request, comentario_id):
    if request.method == 'POST':
        usuario = request.user
        comentario = Comentario.objects.get(id=comentario_id)
        razon = request.POST['razon']

        Reporte.objects.create(usuario=usuario, comentario=comentario, razon=razon)

        messages.success(request, '¡Reporte enviado con éxito!')
        return redirect('ver_comentarios')

    return render(request, 'comentarios/crear_reporte.html')
