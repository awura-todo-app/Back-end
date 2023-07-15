from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    User_email  = models.EmailField(max_length=70,blank=True,unique=True)
    password    = models.CharField(max_length=12)


    def __str__(self):
        return self.user.username
    

class Task(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE )
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete']


