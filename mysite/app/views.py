from django.shortcuts import render,HttpResponse,get_list_or_404
from .serializers import UserSerializer, TodoSerializer
from .models import Todo
from django.contrib.auth.models import User


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny

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


    @action(detail=True, methods=['PUT'])
    def completed(self, request, pk=None):
        try:
            todo = Todo.objects.get(id = pk,owner = request.user)
            todo.completed = True
            todo.save()
            serializer = TodoSerializer(todo, many=False)
            response = {'message': 'task updated', 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Todo item missing'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        if 'name' and 'desc' in request.data:
            todo = Todo.objects.create(name = request.data['name'],desc = request.data['desc'],owner = request.user)
            serializer = TodoSerializer(todo, many=False)
            response = {'message': 'task created', 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)

    @action(detail = True,methods=['GET'])
    def myList(self, request,pk = None):
        todos = Todo.objects.filter(owner = request.user)
        serializer = TodoSerializer(todos, many=True)
        response = {'message': 'task Found', 'result': serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def destroy(self, request,pk=None, *args, **kwargs):
        Todo.objects.get(id=pk).delete()
        response = {'message': 'task deleted'}
        return Response(response, status=status.HTTP_200_OK)