from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse
from django.test import TestCase

from base import mods
from .models import Auth
from .serializers import AuthSerializer

from django.utils.translation import activate
from django.utils.translation import gettext as _

class BaseTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.token = None
        mods.mock_query(self.client)

        user_noadmin = User(username='noadmin')
        user_noadmin.set_password('qwerty')
        user_noadmin.save()

        user_admin = User(username='admin', is_staff=True)
        user_admin.set_password('qwerty')
        user_admin.save()

    def tearDown(self):
        self.client = None
        self.token = None

    def login(self, user='admin', password='qwerty'):
        data = {'username': user, 'password': password}
        response = mods.post('authentication/login', json=data, response=True)
        self.assertEqual(response.status_code, 200)
        self.token = response.json().get('token')
        self.assertTrue(self.token)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def logout(self):
        self.client.credentials()

class AuthAPITestCase(BaseTestCase):
    def test_serialize_auth(self):
        auth = Auth.objects.create(name='Test Auth', url='https://test.com', me=False)
        serializer = AuthSerializer(auth)
        expected_data = {'name': 'Test Auth', 'url': 'https://test.com', 'me': False}
        self.assertEqual(serializer.data, expected_data)

class I18nTestCase(TestCase):

    def test_translations_index(self):
        languages = ['es', 'en', 'fr']

        for language in languages:
            with self.subTest(language=language):
                activate(language)

                # Realizar una solicitud a una vista que contenga cadenas traducibles
                url = reverse('core:index')  # Ajusta según tus rutas reales
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)

                # Verificar que las cadenas traducidas estén presentes en la respuesta
                self.assertContains(response, _('Home'))
                self.assertContains(response, _('¿Quienes somos?'))
                self.assertContains(response, _('Bienvenido'))