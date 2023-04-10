from django.db import models

# Create your models here.
# A model represents the data in an application.

class Thread(models.Model):
    alias = models.TextField(default='')
    subject = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    

class Message(models.Model):
    alias = models.TextField(default='')
    text = models.TextField(default='')
    thread = models.ForeignKey(Thread, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    
    