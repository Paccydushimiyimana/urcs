from django.db import models
from account.models import MyUser

# Create your models here.
class Chat_room(models.Model):
    me = models.ForeignKey(MyUser,related_name='chats',on_delete=models.CASCADE)
    other = models.ForeignKey(MyUser,related_name='+',on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(MyUser,related_name='messages',on_delete=models.CASCADE,null=True)
    room = models.ForeignKey(Chat_room, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(MyUser,related_name='reads',blank=True)

    # def __str__(self):
    #     return self.message
