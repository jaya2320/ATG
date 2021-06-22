from django.db import models
from datetime import datetime
# Create your models here.

class Message(models.Model):
    content=models.CharField(max_length=10000000)
    date=models.DateTimeField(default=datetime.now,blank=True)
    user=models.CharField(max_length=1000)
    room=models.CharField(max_length=500,null=True)
    class Meta:
        ordering=('date',)