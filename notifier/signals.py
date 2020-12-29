from chat.models import Message
from django.db.models.signals import post_save
from django.dispatch import receiver 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save,sender=Message)
def new_message(sender, instance, created, **kwargs):
    if created:
        # print('created')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'gossip',{
                'type':'user_gossip',
                'event':'New message',
                'username':instance.sender.username
                }
        )