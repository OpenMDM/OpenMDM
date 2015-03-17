from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
import public_gate.views as views


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class HomeBasicTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='John', email='', password='Doe')

    def test_get_home_logged_out(self):
        # Create an instance of a GET request.
        request = self.factory.get('/public_gate/home/')
        request.user = AnonymousUser()
        response = views.home(request)
        is_logged_out = "Sign in" in response.content.decode()
        return self.assertTrue(is_logged_out)

    def test_get_home_logged_in(self):
        # Create an instance of a GET request.
        request = self.factory.get('/public_gate/home/')
        request.user = self.user
        response = views.home(request)
        is_logged_in = "Logout" in response.content.decode()
        return self.assertTrue(is_logged_in)