from rest_framework import serializers
from .models import Tasks,User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'