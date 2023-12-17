from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from django.utils.translation import activate
from django.utils.translation import gettext as _

class CoreViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_home_view(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_signup_view(self):
        response = self.client.get(reverse('core:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')

        response = self.client.post(reverse('core:signup'), {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get(reverse('core:logout'))
        self.assertEqual(response.status_code, 302)  # 302 indica una redirección

    def test_assigned_census_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:assigned_census'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/assigned_census.html')


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

