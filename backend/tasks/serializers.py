from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'user', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'user']
        
class BulkUpdateSerializer(serializers.Serializer):
    task_ids = serializers.ListField(child=serializers.IntegerField())
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)

class BulkDeleteSerializer(serializers.Serializer):
    task_ids = serializers.ListField(child=serializers.IntegerField())