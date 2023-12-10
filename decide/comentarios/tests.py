# En comentarios/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from comentarios.models import Comentario
class ComentarioModelTest(TestCase):

    def setUp(self):
        # Crear un usuario para el autor del comentario
        self.usuario = User.objects.create_user(username='autor_prueba', password='contraseña123')

    def test_crear_comentario(self):
        # Crear un comentario
        comentario = Comentario.objects.create(
            autor=self.usuario,  # Usar el usuario creado en setUp
            texto='Este es un comentario de prueba.',
            votos_positivos=0,
            votos_negativos=0,
        )

        # Verificar que el comentario se haya creado correctamente
        self.assertEqual(comentario.autor, self.usuario)
        self.assertEqual(comentario.texto, 'Este es un comentario de prueba.')
        self.assertEqual(comentario.votos_positivos, 0)
        self.assertEqual(comentario.votos_negativos, 0)
