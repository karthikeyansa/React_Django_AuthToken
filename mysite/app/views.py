from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

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