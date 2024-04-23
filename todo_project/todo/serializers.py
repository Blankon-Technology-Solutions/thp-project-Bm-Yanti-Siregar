from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from drf_model_serializer import serializers as drf_serializers

from .models import Todo


class TodoDeserializer(drf_serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(pk_field=HashidSerializerCharField(source_field='todo.Todo.id'), read_only=True)

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'completed']
    
    def create(self, validated_data):
        # Explicitly set the user to the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TodoSerializer(drf_serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(pk_field=HashidSerializerCharField(source_field='todo.Todo.id'), read_only=True)
    
    class Meta:
        model = Todo
        fields = '__all__'