from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout as logO,login as logG
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .models import Tasks
@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = authenticate(username = request.POST['username'],password = request.POST['password'])
        logG(request,user)
        return redirect(tasks)
    return render(request,'mysite/index.html')

def tasks(request):
    tasks = Tasks.objects.filter(owner = request.user)
    return render(request,'mysite/tasks.html',{'tasks':tasks})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        User.objects.create_user(username = request.POST['username'],password = request.POST['password'])
        messages.add_message(request, messages.SUCCESS, 'User created successfully')
        return redirect(login)
    return redirect(register)

@csrf_exempt
def addTask(request):
    if request.method == 'POST':
        Tasks(taskName=request.POST['taskname'],taskDetails=request.POST['taskdetail'],owner=request.user).save()
        messages.add_message(request, messages.SUCCESS, 'Task added successfully')
        return redirect(tasks)
    return redirect(tasks)

@csrf_exempt
def deleteTask(request,id):
    Tasks.objects.get(pk = id).delete()
    messages.add_message(request, messages.SUCCESS, 'Task Deleted successfully')
    return redirect(tasks)

def completedTask(request,id):
    task = Tasks.objects.get(pk = id)
    task.completed = True
    task.save()
    messages.add_message(request, messages.SUCCESS, 'Task %s Completed successfully'%task.taskName)
    return redirect(tasks)

def logout(request):
    logO(request)
    messages.add_message(request, messages.SUCCESS, 'Logged Out')
    return redirect(login)