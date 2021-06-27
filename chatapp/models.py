#from typing_extensions import TypeVarTuple
from chatapp.managers import ThreadManager
from django.db import models
from datetime import datetime
from django.conf import settings 
 
class Profile (models.Model):
    user = models.OneToOneField (settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'profile')
    status = models.BooleanField (default = False)
    profile_image=models.ImageField(upload_to="media",null=True,default='media/default.png')
    

class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Thread(TrackingModel):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group')
    )

    name = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='group')
    users = models.ManyToManyField('auth.User')

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'

class Message(TrackingModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
   
    content = models.TextField(blank=False, null=False)
    date=models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self) -> str:
        return f'From <Thread - {self.thread}>'




# Create your models here.

class Messagepublic(models.Model):
    content=models.CharField(max_length=10000000,null=True)
    date=models.DateTimeField(default=datetime.now,blank=True)
    user=models.CharField(max_length=1000)
    #file=models.FileField(upload_to='media',null=True)
    #room=models.CharField(max_length=500,null=True)
    class Meta:
        ordering=('date',)
       