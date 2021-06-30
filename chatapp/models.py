#from typing_extensions import TypeVarTuple
from chatapp.managers import ThreadManager
from django.db import models
from datetime import datetime
from django.conf import settings 
from django.contrib.auth.models import User
 
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
   
    content = models.TextField(blank=True, null=True)
    date=models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self) -> str:
        return f'From <Thread - {self.thread}>'




# Create your models here.

class Messagepublic(models.Model):
    content=models.CharField(max_length=10000000,null=True)
    date=models.DateTimeField(default=datetime.now,blank=True)
    user=models.CharField(max_length=1000)
  
    
    class Meta:
        ordering=('date',)
       


class Room(models.Model):
    room=models.CharField(max_length=1000,unique=True)
    users = models.ManyToManyField('auth.User')

class Messagegroup(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.CharField(max_length=1000)
    content=models.CharField(max_length=10000000)
    date=models.DateTimeField(default=datetime.now,blank=True)
    room=models.CharField(max_length=500,null=True)
    class Meta:
        ordering=('date',)

class Notification(models.Model):
    PRIVATE='private'
    GROUP='group'
    CHOICES=(
        (PRIVATE,'private'),
        (GROUP,'group')
    )

    to_user=models.ForeignKey(User,related_name='notifications',on_delete=models.CASCADE)
    notification_type=models.CharField(max_length=20,choices=CHOICES)
    is_read=models.BooleanField(default=False)
    extra_id=models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,related_name='creatednotifications',on_delete=models.CASCADE)
    room=models.CharField(max_length=1000,null=True)

    class Meta:
        ordering=['-created_at']
