from model_bakery import baker

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.serializers import ErrorDetail, ValidationError
from todo.models import Todo
from todo.serializers import TodoSerializer, TodoDeserializer
from todo.views import TodoViewSet

User = get_user_model()


class TodoSerializerTestCase(APITestCase):
    def setUp(self):
        self.view = TodoViewSet
        self.factory = APIRequestFactory()

        # Create a test user
        self.user = baker.make(User)

        # Create some sample todos for testing
        self.todo1 = baker.make(Todo, user=self.user, title='Todo 1', description='Description 1', completed=False)
        self.todo2 = baker.make(Todo, user=self.user, title='Todo 2', description='Description 2', completed=True)

    def test_read(self):
        expected = {
            'id': self.todo1.id,
            'user': self.todo1.user.id,
            'title': self.todo1.title,
            'description': self.todo1.description,
            'completed': self.todo1.completed,
            'created_at': self.todo1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
        actual = TodoSerializer(instance=self.todo1).data

        self.assertDictEqual(expected, actual)

class TodoDeserializerTestCase(APITestCase):
    def setUp(self):
        self.view = TodoViewSet
        self.factory = APIRequestFactory()

        # Create a test user
        self.user = baker.make(User)

        # Create some sample todos for testing
        self.todo1 = baker.make(Todo, user=self.user, title='Todo 1', description='Description 1', completed=False)

    def test_write(self):
        data = {
            'user': self.user,
            'title': "title",
            'description': "description",
        }
        request = self.factory.post('/', data)
        request.user = self.user
        context = {'request': request}

        deserializer = TodoDeserializer(data=data, context=context)

        try:
            deserializer.is_valid(raise_exception=True)
        except ValidationError:
            self.fail('Test failed')

        instance = deserializer.save()

        self.assertTrue(instance.id is not None)
        self.assertEqual(instance.user, self.user)
        self.assertEqual(instance.title, "title")
        self.assertEqual(instance.description, 'description')
        self.assertEqual(instance.completed, False)

    def test_update(self):
        data = {
            'title': 'Todo 1 Updated',
            'completed': True,
            'description': "Description Updated"
        }
        request = self.factory.put('/', data)
        request.user = self.user
        context = {'request': request}

        deserializer = TodoDeserializer(data=data, context=context)

        try:
            deserializer.is_valid(raise_exception=True)
        except ValidationError:
            self.fail('Test failed')

        instance = deserializer.save()

        self.assertTrue(instance.id, self.todo1.id)
        self.assertEqual(instance.user, self.user)
        self.assertEqual(instance.title, "Todo 1 Updated")
        self.assertEqual(instance.completed, True)

    def test_missing_parameters(self):
        data = {}
        request = self.factory.post('/', data)
        request.user = self.user
        context = {'request': request}

        deserializer = TodoDeserializer(data=data, context=context)

        with self.assertRaises(ValidationError) as cm:
            deserializer.is_valid(raise_exception=True)

        self.assertEqual(
            cm.exception.detail,
            {'title': [
                ErrorDetail(string='This field is required.', code='required')],
            'description': [
                ErrorDetail(string='This field is required.', code='required')],
                }
        )