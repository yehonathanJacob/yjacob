from django.test import Client
from django.contrib.auth.models import User
from django.test import TestCase

from .models import Poll, Choice


# Create your tests here.
class BasicTest(TestCase):
    def setUp(self):
        # self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()

    def assert_success(self, response):
        self.assertEqual(response.status_code, 200, f"Expected 200 status code in request: {response.request}")
        self.assertEqual(response.headers['Content-Type'], 'application/json', "Expected JSON result.")

        self.assertEqual(response.json()['status'], 'success', f"Expected 'success' status. Got: {response.json()}")

    def assert_failed(self, response):
        self.assertEqual(response.status_code, 200, f"Expected 200 status code in request: {response.request}")
        self.assertEqual(response.headers['Content-Type'], 'application/json', "Expected JSON result.")

        self.assertEqual(response.json()['status'], 'failed', f"Expected 'failed' status. Got: {response.json()}")

class APITest(BasicTest):
    def setUp(self):
        super(BasicTest, self).setUp()

        Poll.objects.create(title='Do you like ice-cream?')

        Choice.objects.create(poll_id=1, description='Yes')
        Choice.objects.create(poll_id=1, description='No')


    def test_connection(self):
        response = self.client.get('/api/test_connection/')
        self.assert_success(response)

    def test_poll_creation(self):
        response = self.client.get('/api/set_new_poll/')
        self.assert_failed(response)

        response = self.client.get('/api/set_new_poll/', {'title':'Simple poll'})
        self.assert_success(response)

    def test_choice_creation(self):
        response = self.client.get('/api/set_new_choice/1/')
        self.assert_failed(response)

        response = self.client.get('/api/set_new_choice/1/', {'description':'Maybe'})
        self.assert_success(response)


    def test_get_poll_options(self):
        response = self.client.get('/api/get_poll_options/1/')
        self.assert_success(response)
        response_data = response.json()
        self.assertTrue(len(response_data['choices']) == 2)

    def test_set_new_vote(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/api/set_new_vote/1/1/')
        self.assert_success(response)

    def test_get_poll_results(self):
        response = self.client.get('/api/get_poll_results/1/')
        self.assert_success(response)
        response_data = response.json()
        self.assertTrue(len(response_data['results']) == 2)

