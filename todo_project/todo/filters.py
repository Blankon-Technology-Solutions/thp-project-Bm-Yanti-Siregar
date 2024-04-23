import django_filters

from .models import Todo

class TodoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    completed = django_filters.BooleanFilter(field_name='completed')

    class Meta:
        model = Todo
        fields = ['title', 'completed']
