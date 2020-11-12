from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Tasks

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'