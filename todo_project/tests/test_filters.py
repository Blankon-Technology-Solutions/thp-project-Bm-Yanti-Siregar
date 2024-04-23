from model_bakery import baker

from django.test import TestCase
from django_filters import CharFilter, BooleanFilter
from django.contrib.auth import get_user_model

from todo.models import Todo
from todo.filters import TodoFilter

User = get_user_model()


class TodoFilterTestCase(TestCase):
    def test_filter_fields(self):
        # Create a test user
        self.user = baker.make(User)

        # Create some sample todos for testing
        self.todo1 = baker.make(Todo, user=self.user, title='test 1', description='Description 1', completed=False)
        self.todo2 = baker.make(Todo, user=self.user, title='test 2', description='Description 2', completed=True)

        # Initialize the filter with data
        filter_data = {'title': 'test', 'completed': True}
        filter_set = TodoFilter(data=filter_data, queryset=Todo.objects.all())

        # Check if filter set is valid
        self.assertTrue(filter_set.is_valid())

        # Check if expected filters are present
        self.assertIsInstance(filter_set.filters['title'], CharFilter)
        self.assertIsInstance(filter_set.filters['completed'], BooleanFilter)

        # Check if filtering works as expected
        filtered_queryset = filter_set.qs
        self.assertEqual(filtered_queryset.count(), 1)
