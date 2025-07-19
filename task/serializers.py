from rest_framework import serializers
from .models import Task, AuditTask
from django.contrib.auth.models import User
from apitask.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'description', 'status', 'user', 'user_id', 'created_at', 'updated_at']


class AuditTaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(queryset = Task.objects.all())
    class Meta:
        model = AuditTask
        fields = ['id', 'status', 'user', 'user_id', 'task', 'task_id', 'created_at', 'updated_at']
