from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    name =  models.CharField(max_length=50,null = False,blank= False)
    desc =  models.TextField(null = False,blank= False)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


