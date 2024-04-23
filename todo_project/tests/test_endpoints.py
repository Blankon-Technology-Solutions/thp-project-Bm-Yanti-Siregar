from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class TestTodoEndpoint(APITestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.client.force_authenticate(self.user)
        self.todo = baker.make("Todo", user=self.user)

    def test_get(self):
        url = '/todo/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        url = '/todo/'
        data = {"title": "Test Title", "description": "Test Description"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        url = f'/todo/{self.todo.id}/'
        data = {"title": "Updated Title", "description": "Updated Description"}
        response = self.client.put(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])

    def test_delete(self):
        url = f'/todo/{self.todo.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
