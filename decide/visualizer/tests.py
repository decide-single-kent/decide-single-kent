from django.test import TestCase
from django.urls import reverse
from django.http import Http404
from unittest.mock import patch
from django.utils.translation import activate

class VisualizerViewTest(TestCase):

    def setUpLenguage(self):
        activate('es')


    def setUp(self):
        super().setUp()
        self.setUpLenguage()

        
    def tearDown(self):
        super().tearDown()


    def test_visualizer_view(self):
        # Simula la respuesta de la API que se utiliza en tu vista
        with patch('base.mods.get') as mock_get:
            mock_get.return_value = [{'id': 1, 'name': 'Voting 1', 'start_date': '2023-01-01', 'end_date': '2023-01-10'}]

            # Supongamos que tienes una URL llamada 'visualizer' con un parámetro de ID
            url = reverse('visualizer', args=[1])

            # Simula una solicitud GET a la vista
            response = self.client.get(url)

            # Verifica que la solicitud fue exitosa (código de respuesta 200)
            self.assertEqual(response.status_code, 200)

            # Verifica que el contenido de la respuesta contiene elementos específicos de tu plantilla
            self.assertContains(response, 'Decide')
            self.assertContains(response, 'Voting 1')

            # Verifica que el contexto contiene la información correcta
            self.assertIn('voting', response.context)
            self.assertEqual(response.context['voting'], '{"id": 1, "name": "Voting 1", "start_date": "2023-01-01", "end_date": "2023-01-10"}')


    def test_visualizer_view_with_invalid_id(self):
        # Simula una respuesta de la API cuando se proporciona un ID de votación no válido
        with patch('base.mods.get') as mock_get:
            mock_get.side_effect = Http404()
            
            url = reverse('visualizer', args=[999])

            # Simula una solicitud GET a la vista con un ID no válido
            response = self.client.get(url)

            # Verifica que la vista devuelve un error 404
            self.assertEqual(response.status_code, 404)