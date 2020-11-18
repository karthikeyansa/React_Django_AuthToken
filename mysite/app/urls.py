from django.urls import path
from . import views
urlpatterns = [
    path('',views.login,name="login"),
    path('register',views.register,name="register"),
    path('tasks',views.tasks,name='tasks'),
    path('addtask',views.addTask,name="addTask"),
    path('delete/<int:id>',views.deleteTask,name="deleteTask"),
    path('completed/<int:id>',views.completedTask,name="completedTask"),
    path('logout',views.logout,name="logout"),
]
