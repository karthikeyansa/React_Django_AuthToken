from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('todos', views.TodoViewset)
router.register('users',views.UserViewset)

urlpatterns = [
    path('', include(router.urls)),
]