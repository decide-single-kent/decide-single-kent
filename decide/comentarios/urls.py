from django.urls import path
from comentarios.views import agregar_comentario , ver_comentarios ,editar_comentario,borrar_comentario,votar_comentario,no_autenticado_view

urlpatterns = [
    path('ver-comentarios/', ver_comentarios, name='ver_comentarios'),
    path('agregar/', agregar_comentario, name='agregar_comentario'),
    path('editar/<int:comentario_id>/', editar_comentario, name='editar_comentario'),
    path('borrar/<int:comentario_id>/', borrar_comentario, name='borrar_comentario'),
    path('votar_comentario/<int:comentario_id>/<str:voto>/', votar_comentario, name='votar_comentario'),
    path('no_autenticado/', no_autenticado_view, name='no_autenticado'),
]
