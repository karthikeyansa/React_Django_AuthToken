from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from app.models import Tasks

# Create your views here.
#rest_framework
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .serializers import UserSerializers,TaskSerializers

@csrf_exempt
def UserLoginApi(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        user = authenticate(username = user_data['username'],password = user_data['password'])
        login(request,user)
        user_serializer = UserSerializers(user,many = False)
        return JsonResponse(user_serializer.data,safe=False)

@csrf_exempt
def UserRegisterApi(request):
    if request.method == 'POST':
        newuser_data = JSONParser().parse(request)
        User.objects.create_user(username = newuser_data['username'],password = newuser_data['password'])
        return HttpResponse("User created successfully")


@csrf_exempt
def AddTaskApi(request):
    #print(request.user)
    task_data = JSONParser().parse(request)
    if request.method == 'POST':
        Tasks(taskName = task_data['taskname'],taskDetails =task_data['taskdetail'],owner=request.user).save()
        return HttpResponse("Task Added Successfully")

@csrf_exempt
def DeleteTaskApi(request,id):
    if request.method == "DELETE":
        Tasks.objects.get(pk = id).delete()
        return HttpResponse("Task Deleted Successfully")

@csrf_exempt
def CompleteTaskApi(request,id):
    if request.method == "PUT":
        task = Tasks.objects.get(pk = id)
        task.completed = True
        task.save()
        return HttpResponse("task Completed Successfully")

@csrf_exempt
def TasksApi(request):
    tasks = Tasks.objects.filter(owner = request.user)
    task_Serializer = TaskSerializers(tasks,many = True)
    return JsonResponse(task_Serializer.data,safe=False)

@csrf_exempt
def LogoutApi(request):
    logout(request)
    return HttpResponse('Logged out')