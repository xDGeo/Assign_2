from django.test import TestCase, SimpleTestCase
from .forms import UserRegistrationForm
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .models import Invitation, Game, Question
from .views import register, login_view, logout_view, invite, accept_invitation, reject_invitation, game_view, result


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.question = Question.objects.create(question_text='What is the capital of France?', answer='Paris')

    def test_invitation_creation(self):
        invitation = Invitation.objects.create(from_user=self.user1, to_user=self.user2)
        self.assertEqual(str(invitation), f'Invitation from {self.user1} to {self.user2}')

    def test_game_creation(self):
        game = Game.objects.create(player1=self.user1, player2=self.user2)
        self.assertEqual(str(game), f'{self.user1} vs {self.user2} - ongoing')

    def test_question_creation(self):
        self.assertEqual(str(self.question), 'What is the capital of France?')

class FormsTestCase(TestCase):
    def test_user_registration_form(self):
        form_data = {
            'username': 'newuser',
            'password': 'pass',
            'password_confirm': 'pass'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration_form_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'password': 'pass',
            'password_confirm': 'wrongpass'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.client.login(username='user1', password='pass')

    def test_register_view(self):
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'testpass', 'password_confirm': 'testpass'})
        self.assertEqual(response.status_code, 302)

    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'pass'})
        self.assertEqual(response.status_code, 302)

    def test_invite_view(self):
        response = self.client.post(reverse('invite'), {'username': 'user2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Invitation.objects.count(), 1)

    def test_accept_invitation_view(self):
        invitation = Invitation.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.login(username='user2', password='pass')
        response = self.client.get(reverse('accept_invitation', args=[invitation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Game.objects.count(), 1)

    def test_game_view(self):
        game = Game.objects.create(player1=self.user1, player2=self.user2)
        response = self.client.get(reverse('game', args=[game.id]))
        self.assertEqual(response.status_code, 200)

    def test_result_view(self):
        game = Game.objects.create(player1=self.user1, player2=self.user2, status='finished', player1_score=5, player2_score=3)
        response = self.client.get(reverse('result', args=[game.id]))
        self.assertEqual(response.status_code, 200)

class UrlsTestCase(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login_view)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout_view)

    def test_invite_url_resolves(self):
        url = reverse('invite')
        self.assertEqual(resolve(url).func, invite)

    def test_accept_invitation_url_resolves(self):
        url = reverse('accept_invitation', args=[1])
        self.assertEqual(resolve(url).func, accept_invitation)

    def test_reject_invitation_url_resolves(self):
        url = reverse('reject_invitation', args=[1])
        self.assertEqual(resolve(url).func, reject_invitation)

    def test_game_url_resolves(self):
        url = reverse('game', args=[1])
        self.assertEqual(resolve(url).func, game_view)

    def test_result_url_resolves(self):
        url = reverse('result', args=[1])
        self.assertEqual(resolve(url).func, result)