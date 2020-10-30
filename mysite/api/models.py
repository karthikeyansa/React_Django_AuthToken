from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tasks(models.Model):
    taskName = models.CharField(max_length=50,null=False,blank=True)
    taskDetails = models.TextField(null=False)
    timeStamp = models.DateTimeField(null=False,auto_now_add=True)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='owner')

    def __repr__(self):
        return self.taskName