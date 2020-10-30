from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .models import Tasks,User
# Create your views here.
#rest_framework
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .serializers import UserSerializers,TaskSerializers


@csrf_exempt
def UserLoginApi(request,username='',password=''):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        print(user_data['username'],user_data['password'])
        user = authenticate(username = user_data['username'],password = user_data['password'])
        print(user)
        if user:
            request.session['user_id'] = user.id
            tasks = Tasks.objects.filter(owner = user)
            task_Serializer = TaskSerializers(tasks,many = True)
            return JsonResponse(task_Serializer.data,safe=False)

@csrf_exempt
def UserRegisterApi(request):
    if request.method == 'POST':
        newuser_data = JSONParser().parse(request)
        try:
            newuser = User.objects.create_user(username = newuser_data['username'],password = newuser_data['password'])
            if newuser:
                return HttpResponse("User created successfully")
        except:
            return HttpResponse("Error !! Try different username")

@csrf_exempt
def AddTaskApi(request):
    try:
        user = User.objects.get(pk = request.session['user_id'])
    except:
        return HttpResponse("No User Credentials Found")
    tasks = Tasks.objects.filter(owner = user)
    task_data = JSONParser().parse(request)
    if request.method == 'POST':
        try:
            newtask = Tasks(taskName = task_data['taskname'],taskDetails =task_data['taskdetail'],owner=user)
            newtask.save()
            return HttpResponse("Task Added Successfully")
        except:
            return HttpResponse("Task construction Error")
@csrf_exempt
def DeleteTaskApi(request,id):
    if request.method == "DELETE":
        try:
            user = User.objects.get(pk = request.session['user_id'])
        except:
            return HttpResponse("No User Credentials Found")
        try:
            task = Tasks.objects.get(pk = id)
            task.delete()
            return HttpResponse("Task Deleted Successfully")
        except:
            return HttpResponse("Task not found")
@csrf_exempt
def CompleteTaskApi(request,id):
    try:
        user = User.objects.get(pk = request.session['user_id'])
    except:
        return HttpResponse("No User Credentials Found")
    try:
        if request.method == "PUT":
            task = Tasks.objects.get(pk = id)
            task.completed = True
            task.save()
            return HttpResponse("task Completed Successfully")
    except:
        return HttpResponse("task not found")
@csrf_exempt
def TasksApi(request):
    try:
        user = User.objects.get(pk = request.session['user_id'])
    except:
        return HttpResponse("No User Credentials Found")
    tasks = Tasks.objects.filter(owner = user)
    task_Serializer = TaskSerializers(tasks,many = True)
    return JsonResponse(task_Serializer.data,safe=False)

@csrf_exempt
def LogoutApi(request):
    try:
        del request.session['user_id']
        return HttpResponse("User Logged out Successfully")
    except:
        return HttpResponse("No User Active")