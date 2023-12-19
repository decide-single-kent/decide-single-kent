# En comentarios/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Comentario
from django.contrib.messages import get_messages
from .models import Reporte
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

class ComentariosViewsTestCase(TestCase):
    def setUp(self):
        # Crea un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Inicia sesión con el usuario de prueba
        self.client.login(username='testuser', password='testpassword')

        # Crea un comentario de prueba asociado al usuario
        self.comentario = Comentario.objects.create(autor=self.user, texto='Este es un comentario de prueba')

        # Crea algunos comentarios de prueba asociados al usuario
        Comentario.objects.create(autor=self.user, texto='Comentario 1')
        Comentario.objects.create(autor=self.user, texto='Comentario 2')

        # Imprime la cantidad de comentarios en la base de datos

    def test_editar_comentario_view(self):
        # Realiza una solicitud POST para editar el comentario
        url = reverse('editar_comentario', args=[self.comentario.id])
        response = self.client.post(url, {'texto': 'Texto modificado'})

        # Verifica que la respuesta sea un redireccionamiento
        self.assertEqual(response.status_code, 302)
        # Actualiza el objeto de comentario desde la base de datos
        self.comentario.refresh_from_db()

        # Verifica que el texto del comentario se haya actualizado correctamente
        self.assertEqual(self.comentario.texto, 'Texto modificado')

    def test_ver_comentarios_view(self):
        # Realiza una solicitud GET para ver los comentarios
        url = reverse('ver_comentarios')  # Ajusta el nombre de la vista según tu configuración
        response = self.client.get(url)

        # Verifica que la respuesta sea un código 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verifica que los comentarios se muestren en la respuesta
        self.assertContains(response, 'Comentario 1')
        self.assertContains(response, 'Comentario 2')
    def test_eliminar_comentario_view(self):
        # Realiza una solicitud POST para eliminar el comentario
        url = reverse('borrar_comentario', args=[self.comentario.id])  # Utiliza el nombre correcto de la vista
        response = self.client.post(url)

        # Verifica que la respuesta sea un redireccionamiento (código 302)
        self.assertEqual(response.status_code, 302)

        # Verifica que el comentario se haya eliminado correctamente de la base de datos
        with self.assertRaises(Comentario.DoesNotExist):
            Comentario.objects.get(pk=self.comentario.id)

        # Verifica que se haya redirigido a la vista 'ver_comentarios' (o ajusta según tu lógica)
        self.assertRedirects(response, reverse('ver_comentarios'))

    def test_crear_reporte(self):
        # Crea un comentario de prueba asociado al usuario
        comentario = Comentario.objects.create(autor=self.user, texto='Este es un comentario de prueba')

        # Realiza una solicitud POST para crear un reporte para el comentario
        url = reverse('crear_reporte', args=[comentario.id])
        response = self.client.post(url, {'razon': 'Contenido ofensivo'})

        # Verifica que la respuesta sea un redireccionamiento
        self.assertEqual(response.status_code, 302)

        # Verifica que se haya creado un reporte en la base de datos
        self.assertEqual(Reporte.objects.count(), 1)

        # Obtiene el último reporte creado
        nuevo_reporte = Reporte.objects.latest('creado_en')

        # Verifica que el reporte esté asociado al usuario y al comentario correctos
        self.assertEqual(nuevo_reporte.usuario, self.user)
        self.assertEqual(nuevo_reporte.comentario, comentario)
        self.assertEqual(nuevo_reporte.razon, 'Contenido ofensivo')

        # Verifica que se haya mostrado el mensaje de éxito en la respuesta
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn('¡Reporte enviado con éxito!', messages)

        # Verifica que se haya redirigido a la vista 'ver_comentarios'
        self.assertRedirects(response, reverse('ver_comentarios'))

    def test_votar_comentario(self):
        # Realiza una solicitud POST para votar positivo en el comentario
        url = reverse('votar_comentario', args=[self.comentario.id, 'positivo'])
        response = self.client.post(url)

        # Verifica que la respuesta sea un código 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Actualiza el objeto de comentario desde la base de datos
        self.comentario.refresh_from_db()

        # Verifica que el comentario tenga un voto positivo
        self.assertEqual(self.comentario.votos_positivos, 1)
        self.assertEqual(self.comentario.votos_negativos, 0)

        # Realiza una solicitud POST para votar negativo en el comentario
        url = reverse('votar_comentario', args=[self.comentario.id, 'negativo'])
        response = self.client.post(url)

        # Verifica que la respuesta sea un código 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Actualiza el objeto de comentario desde la base de datos
        self.comentario.refresh_from_db()

        # Verifica que el comentario tenga un voto positivo
        self.assertEqual(self.comentario.votos_positivos, 0)
        self.assertEqual(self.comentario.votos_negativos, 1)