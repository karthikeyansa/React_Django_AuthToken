from django.urls import path
from . import views
urlpatterns = [
    path('',views.login,name="login"),
    path('register',views.register,name="register"),
    path('addtask',views.addTask,name="addTask"),
    path('delete/<int:id>',views.deleteTask,name="deleteTask"),
    path('completed/<int:id>',views.completedTask,name="completedTask"),
    path('logout',views.logout,name="logout"),
    path('api/user',views.UserLoginApi),
    path('api/newuser',views.UserRegisterApi),
    path('api/addtask',views.AddTaskApi),
    path('api/deletetask/<int:id>',views.DeleteTaskApi),
    path('api/completetask/<int:id>',views.CompleteTaskApi),
    path('api/tasks',views.TasksApi),
    path('api/logout',views.LogoutApi)
]
