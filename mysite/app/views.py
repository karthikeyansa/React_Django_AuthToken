from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#rest_framework
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .serializers import UserSerializers,TaskSerializers
# Create your views here.
from .models import Tasks,User
from .forms import UserForm

@csrf_exempt
def login(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username,password = password)
            if user:
                request.session['user_id'] = user.id
                tasks = Tasks.objects.filter(owner = user)
                return render(request,'mysite/tasks.html',{'tasks': tasks})
        else:
            messages.add_message(request, messages.WARNING, 'Invalid Credentials')
            return redirect(login)
    return render(request,'mysite/index.html',{'form': form})
@csrf_exempt
def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username = username,password = password)
            if user:
                messages.add_message(request, messages.SUCCESS, 'User %s created successfully'%username)
                return redirect(login)
        return redirect(register)
    return render(request,'mysite/index.html',{'form': form})

@csrf_exempt
def addTask(request):
    user = User.objects.get(pk = request.session['user_id'])
    tasks = Tasks.objects.filter(owner = user)
    if request.method == 'POST':
        taskname = request.POST['taskname']
        taskdesc = request.POST['taskdetail']
        task = Tasks(taskName=taskname,taskDetails=taskdesc,owner=user)
        task.save()
        messages.add_message(request, messages.SUCCESS, 'Task %s added successfully'%taskname)
        return redirect(addTask)
    return render(request,'mysite/tasks.html',{'tasks':tasks})

@csrf_exempt
def deleteTask(request,id):
    task = Tasks.objects.get(pk = id)
    messages.add_message(request, messages.SUCCESS, 'Task %s Deleted successfully'%task.taskName)
    task.delete()
    return redirect(addTask)

def completedTask(request,id):
    task = Tasks.objects.get(pk = id)
    task.completed = True
    task.save()
    messages.add_message(request, messages.SUCCESS, 'Task %s Completed successfully'%task.taskName)
    return redirect(addTask)

def logout(request):
    del request.session['user_id']
    messages.add_message(request, messages.SUCCESS, 'Logged Out')
    return redirect(login)
  
@csrf_exempt
def UserLoginApi(request,username='',password=''):
    if request.method == 'PUT':
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
    if request.method == 'PUT':
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
    if request.method == 'PUT':
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