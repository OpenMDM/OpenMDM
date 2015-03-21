from django.test import TestCase, RequestFactory, Client
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
            username='John Doe',
            email='',
            password='test')
        self.c = Client()

    def test_home_responds(self):
        # Create an instance of a GET request.
        request = self.factory.get('/public_gate/home/')
        response = views.home(request)
        return self.assertEqual(response.status_code, 200)

    def test_plists_responds(self):
        # Create an instance of a GET request.
        request = self.factory.get('/public_gate/property_list/')
        response = views.property_lists(request)
        return self.assertEqual(response.status_code, 200)

    def test_add_plist_select_responds(self):
        # Create an instance of a GET request.
        request = self.factory.get('/public_gate/property_list/add/')
        response = views.add_property_list(request)
        return self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Create an instance of a GET request.
        response = self.c.post("/login/", dict(login="John+Doe", password="test"), follow=True)
        return self.assertEqual(response.status_code, 200)