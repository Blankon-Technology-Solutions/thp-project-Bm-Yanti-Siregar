from model_bakery import baker

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from todo.models import Todo
from todo.serializers import TodoSerializer, TodoDeserializer
from todo.views import TodoViewSet

User = get_user_model()


class TodoViewSetTestCase(APITestCase):
    def setUp(self):
        self.view = TodoViewSet
        self.factory = APIRequestFactory()

        # Create a test user
        self.user = baker.make(User)

        # Create some sample todos for testing
        self.todo1 = baker.make(Todo, user=self.user, title='Todo 1', description='Description 1', completed=False)
        self.todo2 = baker.make(Todo, user=self.user, title='Todo 2', description='Description 2', completed=True)

    def test_get_read_serializer_class(self):
        view = self.view()
        view.action = 'list'
        self.assertEqual(view.get_serializer_class(), TodoSerializer)
    
    def test_get_write_serializer_class(self):
        view = self.view()
        view.action = 'post'
        self.assertEqual(view.get_serializer_class(), TodoDeserializer)
    
    def test_get_queryset(self):
        view = self.view()
        request = self.factory.get('/')
        request.user = self.user
        view.request = request

        expected = [self.todo1.id, self.todo2.id]
        actual = view.get_queryset()

        self.assertQuerysetEqual(actual, expected, lambda item: item.id, ordered=False)

    def test_list(self):
        view = self.view.as_view({'get': 'list'})
        request = self.factory.get(reverse('todo-list'))
        force_authenticate(request, self.user)
        view.request = request
        response = view(request)

        self.assertEqual(len(response.data), 2)
        self.assertEqual([self.todo1.id, self.todo2.id], [todo['id'] for todo in response.data])
    
    def test_post(self):
        view = self.view.as_view({'post': 'create'})
        data = {
            "title": "title test",
            "description": "description",
            "completed": False
        }

        request = self.factory.post(reverse('todo-list'), data=data)
        force_authenticate(request, self.user)
        view.request = request
        response = view(request)

        self.assertEqual(response.data['title'], data['title'])
    
    def test_delete(self):
        view = self.view.as_view({'delete': 'destroy'})
        request = self.factory.delete(reverse('todo-detail', kwargs={'pk': self.todo1.pk}))
        force_authenticate(request, self.user)
        response = view(request, pk=self.todo1.pk)
        self.assertEqual(response.status_code, 204) 

    def test_update(self):
        new_title = "Updated Title"
        new_description = "Updated Description"
        view = self.view.as_view({'put': 'update'})
        data = {
            "title": new_title,
            "description": new_description,
            "completed": True
        }
        request = self.factory.put(reverse('todo-detail', kwargs={'pk': self.todo1.pk}), data=data)
        force_authenticate(request, self.user)
        response = view(request, pk=self.todo1.pk)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data['title'], new_title)
        self.assertEqual(response.data['description'], new_description)
        self.assertEqual(response.data['completed'], True)

    def test_get_detail(self):
        view = self.view.as_view({'get': 'retrieve'})
        request = self.factory.get(reverse('todo-detail', kwargs={'pk': self.todo1.pk}))
        force_authenticate(request, self.user)
        response = view(request, pk=self.todo1.pk)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data['id'], self.todo1.pk)
