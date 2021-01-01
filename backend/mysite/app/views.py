from django.shortcuts import render, HttpResponse, get_list_or_404
from .serializers import UserSerializer, TodoSerializer
from .models import Todo
from django.contrib.auth.models import User


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class TodoViewset(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if 'name' and 'desc' in request.data:
            todo = Todo.objects.create(name=request.data['name'], desc=request.data['desc'], owner=request.user)
            serializer = TodoSerializer(todo, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        todos = Todo.objects.filter(owner=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        Todo.objects.get(id=pk).delete()
        todo = Todo.objects.all()
        serializer = TodoSerializer(todo, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, name=None, desc=None, *args, **kwargs):
        todo = Todo.objects.get(id=pk)
        todo.name = request.data['name']
        todo.desc = request.data['desc']
        todo.save()
        todo = Todo.objects.all()
        serializer = TodoSerializer(todo, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None, *args, **kwargs):
        todo = Todo.objects.get(id=pk)
        todo.completed = True
        todo.save()
        todo = Todo.objects.all()
        serializer = TodoSerializer(todo, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)