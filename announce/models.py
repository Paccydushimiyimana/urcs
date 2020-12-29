from datetime import datetime
from django.db import models
from account.models import MyUser
from django.urls import reverse
from ckeditor.fields import RichTextField

class Announce(models.Model):
    title=models.CharField(max_length=100)
    content=RichTextField()
    file = models.FileField(upload_to='documents/',null=True,blank=True)
    sender=models.ForeignKey(MyUser,related_name='+',on_delete=models.SET_NULL,null=True)
    receiver=models.ManyToManyField(MyUser, related_name='+',blank=True)
    date=models.DateTimeField(auto_now_add=True)
    # due_date = models.DateTimeField(default=datetime.now())
    viewed_by=models.ManyToManyField(MyUser,related_name='views',blank=True)
    archived_by = models.ManyToManyField(MyUser, related_name='archives',blank=True)
    general = models.BooleanField(default=False)

    def __str__(self):
        return self.title
  