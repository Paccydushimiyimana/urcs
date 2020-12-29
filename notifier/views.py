from django.shortcuts import render
from django.http import HttpResponse
from announce.models import Announce
from chat.models import Chat_room

def unread_anct_view(request):
    user = request.user
    announcesall=Announce.objects.all()
    announces=[]
    unreads = 0
    for announcet in announcesall:
        if user in announcet.receiver.all():
            announces.append(announcet)
    for announce in announces:
        if announce.general==False and user not in announce.viewed_by.all():
            unreads += 1   
    # print('this is announce view',unreads)
    return HttpResponse(unreads)

def unread_chat_view(request):
    # time.sleep(.5)
    user = request.user
    all_rooms= Chat_room.objects.all()
    unreads = 0
    my_rooms = []
    for room in all_rooms:
        if user == room.me or user == room.other:
            my_rooms.append(room)
            for message in room.messages.all():
                if user != message.sender:
                    if user not in message.read_by.all():
                        unreads += 1  
    # print('this is chat view',unreads)
    return HttpResponse(unreads)

    
