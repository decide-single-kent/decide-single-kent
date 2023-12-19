import random
import itertools
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client, TestCase
from voting.forms import AuthForm, QuestionForm, QuestionOptionFormSet, VotingForm
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from datetime import datetime
from django.utils.translation import activate


class VotingTests(TestCase):
    def setUp(self):
        # Crea un usuario para autenticación en las pruebas
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.question = Question.objects.create(desc='Pregunta de prueba')
        self.auth = Auth.objects.create(name='Nombre de autenticación', url='https://example.com')

    def test_voting_view_get_request(self):

        self.client.force_login(self.user)
        # Prueba que la vista responde correctamente a una solicitud GET
        response = self.client.get(reverse('create_voting'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voting.html')
        self.assertIsInstance(response.context['form'], VotingForm)

class QuestionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_question_view_authenticated_user(self):
        # Prueba que la vista carga correctamente para un usuario autenticado
        self.client.force_login(self.user)
        response = self.client.get(reverse('new_question'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_question.html')
        self.assertIsInstance(response.context['form'], QuestionForm)
        self.assertIsInstance(response.context['formset'], QuestionOptionFormSet)

class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_auth_view_get_request(self):
        # Inicia sesión con el usuario de prueba
        self.client.force_login(self.user)

        # Prueba que la vista responde correctamente a una solicitud GET
        response = self.client.get(reverse('new_auth'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_auth.html')
        self.assertIsInstance(response.context['form'], AuthForm)

    def test_auth_view_post_request_valid_form(self):
        # Prueba que la vista redirige correctamente después de una solicitud POST con un formulario válido
        self.client.force_login(self.user)

        # Reemplaza esto con datos válidos para tu formulario
        data = {'name': 'John Doe', 'url': 'https://example.com'}
        response = self.client.post(reverse('new_auth'), data)
        self.assertEqual(response.status_code, 302)  # 302 es el código de redirección
        self.assertRedirects(response, reverse('close_windows'))

    def test_auth_view_post_request_invalid_form(self):
        # Prueba que la vista no permite enviar el formulario cuando está en un estado inválido
        self.client.force_login(self.user)

        # Datos que generan un formulario inválido automáticamente
        data = {'name': '', 'url': 'Mal'}
        response = self.client.post(reverse('new_auth'), data)

        # Se espera que la vista regrese el mismo formulario, sin redirección
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_auth.html')
        self.assertIsInstance(response.context['form'], AuthForm)

        # Asegurarse de que el formulario no se ha guardado
        self.assertFalse(Auth.objects.exists())


class VotingCreationTests(TestCase):

    def setUp(self):
        # Crear un usuario para la autenticación
        self.usuario = User.objects.create_user(username='test', password='contraseña123')
        self.question = Question.objects.create(desc='¿Cuál es tu color favorito?')
        self.auth = Auth.objects.create(name='Auth Test', url='https://auth.example.com', me=False)

    def test_creacion_question_con_opciones(self):
        # Crear una pregunta con opciones
        self.question = Question.objects.create(desc='¿Cuál es tu color favorito?')

        # Crear dos instancias de QuestionOption para representar dos opciones
        option1 = QuestionOption(question=self.question, option='Rojo')
        option1.save()

        option2 = QuestionOption(question=self.question, option='Azul')
        option2.save()

        # Verificar que la pregunta se haya creado correctamente
        self.assertEqual(self.question.desc, '¿Cuál es tu color favorito?')

        # Verificar que las opciones se hayan creado correctamente
        self.assertEqual(option1.option, 'Rojo')
        self.assertEqual(option2.option, 'Azul')

    def test_creacion_auth_valida(self):
        # Crear un Auth válido
        self.auth = Auth.objects.create(name='Auth Test', url='https://auth.example.com', me=False)

        # Verificar que el Auth se haya creado correctamente
        self.assertEqual(self.auth.name, 'Auth Test')
        self.assertEqual(self.auth.url, 'https://auth.example.com')
        self.assertFalse(self.auth.me)

    def test_creacion_voting_valida(self):
        # Crear una votación válida
        voting = Voting.objects.create(
            name='Voting Test',
            desc='Descripción de la votación',
            question=self.question,
        )

        voting.auths.set([self.auth])

        # Verificar que la votación se haya creado correctamente
        self.assertEqual(voting.name, 'Voting Test')
        self.assertTrue(Voting.objects.filter(name='Voting Test').exists())

    def test_creacion_question_sin_opciones(self):
        # Crear una pregunta sin opciones
        question_sin_opciones = Question.objects.create(desc='¿Cuál es tu número favorito?')

        # Verificar que la pregunta se haya creado correctamente
        self.assertEqual(question_sin_opciones.desc, '¿Cuál es tu número favorito?')

        # Verificar que no haya opciones asociadas a la pregunta
        self.assertFalse(question_sin_opciones.options.exists())
        
    def test_crear_voting(self):
        # Crear un comentario
        voting = Voting.objects.create(
            name='PruebaTest',
            desc='Este es un test de prueba.',
            question=self.question,
        )

        voting.auths.set([self.auth])

        # Verificar que el comentario se haya creado correctamente
        self.assertEqual(voting.name, 'PruebaTest')
        self.assertEqual(voting.desc, 'Este es un test de prueba.')
        self.assertEqual(voting.question, self.question)
        self.assertIn(self.auth, voting.auths.all())



    def test_creacion_voting_sin_autenticacion(self):
        # Verificar que un usuario no autenticado no pueda crear una votación
        form_data = {
            'name': 'Voting Test',
            'desc': 'Descripción de la votación',
            'question': self.question,
            'auth': self.auth,
        }

        # Configurar un cliente sin autenticación
        unauthenticated_client = Client()

        response = unauthenticated_client.post(reverse('create_voting'), form_data)
        self.assertEqual(response.status_code, 302)  # Verificar redirección a la página de inicio de sesión

        # Verificar que la votación no se haya creado
        self.assertFalse(Voting.objects.filter(name='Voting Test').exists())


class VotingTestCase(BaseTestCase):

    def setUpLanguage(self):
        activate('es')

    def setUp(self):
        super().setUp()
        self.setUpLanguage()
    


    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        #login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        #login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 401)

        #login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        #login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        #STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        #STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        #STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        #STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')

class LogInSuccessTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def successLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")
        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/")

class LogInErrorTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def usernameWrongLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)
        
        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("usuarioNoExistente")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("usuarioNoExistente")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/p').text == 'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.')

    def passwordWrongLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("wrongPassword")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/p').text == 'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.')

class QuestionsTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def createQuestionSuccess(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.cleaner.get(self.live_server_url+"/admin/voting/question/add/")
        
        self.cleaner.find_element(By.ID, "id_desc").click()
        self.cleaner.find_element(By.ID, "id_desc").send_keys('Test')
        self.cleaner.find_element(By.ID, "id_options-0-number").click()
        self.cleaner.find_element(By.ID, "id_options-0-number").send_keys('1')
        self.cleaner.find_element(By.ID, "id_options-0-option").click()
        self.cleaner.find_element(By.ID, "id_options-0-option").send_keys('test1')
        self.cleaner.find_element(By.ID, "id_options-1-number").click()
        self.cleaner.find_element(By.ID, "id_options-1-number").send_keys('2')
        self.cleaner.find_element(By.ID, "id_options-1-option").click()
        self.cleaner.find_element(By.ID, "id_options-1-option").send_keys('test2')
        self.cleaner.find_element(By.NAME, "_save").click()

        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/voting/question/")

    def createCensusEmptyError(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.cleaner.get(self.live_server_url+"/admin/voting/question/add/")

        self.cleaner.find_element(By.NAME, "_save").click()

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div/form/div/p').text == 'Please correct the errors below.')
        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/voting/question/add/")