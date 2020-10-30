from django.urls import path
from . import views
urlpatterns = [
    path('api/user',views.UserLoginApi),
    path('api/newuser',views.UserRegisterApi),
    path('api/addtask',views.AddTaskApi),
    path('api/deletetask/<int:id>',views.DeleteTaskApi),
    path('api/completetask/<int:id>',views.CompleteTaskApi),
    path('api/tasks',views.TasksApi),
    path('api/logout',views.LogoutApi)
]
