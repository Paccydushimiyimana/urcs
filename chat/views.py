import json
import time
import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from account.models import MyUser
from .models import Chat_room
from .forms import RoomForm

@login_required
def chat_index_view(request,user_name):
    _form = request.POST.get('form_name') 
    chat_form = RoomForm()
    pwd_form = PasswordChangeForm(request.user) 
    if _form == 'logout_form':
    # Logging out user
        user = request.user
        logout(request)
        messages.success(request, f'User {user} is logged out')
        return redirect('home')
    all_rooms = Chat_room.objects.all()
    user = request.user
    rooms=[]
    for room in all_rooms:
        if user == room.me or user == room.other:  
            rooms.append(room)
    if _form == 'chat_form':        
    #creating a new chat room
        chat_form = RoomForm(request.POST)
        if chat_form.is_valid():
            id_ = request.POST.get('other')
            me = request.user
            other= MyUser.objects.get(id=id_)
            count = 0
            for room in all_rooms:
                if (room.me==me and room.other==other) or (room.me==other and room.other==me):
                    count += 1
            print(count)
            if count == 0:
                Chat_room.objects.create(me=me,other=other)
                messages.success(request, f'Chat {me}-{other} created .!')
                return redirect('chat',user)
            else:
                messages.warning(request, f'Chat already exists!') 
    if _form == 'pwd_form':        
    # Changing password  
        pwd_form = PasswordChangeForm(request.user, request.POST) 
        if pwd_form.is_valid():
            user = pwd_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Your password was . updated!')
            return redirect('change_password')
        else:
            messages.warning(request, f'Please Correct the errors on the form!...')                
    if _form == 'delete_form':
    # Delete a chat room
        _id = request.POST.get('room_id')
        print(_id,request.POST.get('room_id'))
        room = Chat_room.objects.get(id=_id)
        room.delete()
        messages.success(request, f"Chatroom '{room.me}-{room.other}' deleted.")
        return redirect('chat',user)
    context = {'pwd_form':pwd_form,'chat_form':chat_form,'rooms':rooms,'user':user}
    return render(request,'chat_index.html',context) 

def passing_msg_view(request,room_pky):
    message = request.GET.get('msg') 
    sender = request.GET.get('sndr')
    user = request.user.username
    print(request.user)
    template = 'msg_in.html' 
    if user == sender:
        template = 'msg_out.html'
    context = {'message' : message,'msg_date': datetime.datetime.now()} 
    return render(request,template,context)

def passing_box_view(request,room_pky):
    user = request.user  
    room= Chat_room.objects.get(id=room_pky)
    for message in room.messages.all():
        if user not in message.read_by.all():
            message.read_by.add(user)        
    context = {'room':room, 'user':request.user}
    return render(request,'chat_log.html',context)    

def user_detail_view(request):
    _id=request.GET.get('id')
    user=MyUser.objects.get(id=_id)
    context={'user':user,'cat':user.category.name,'page':'detail'}
    return render(request,'modal_user_detail.html',context)

def del_chat_view(request):
    room_pky=request.GET.get('room')
    room = Chat_room.objects.get(id=room_pky)
    context={'room':room}
    return render(request,'modal_del_chat.html',context)

def unread(request):
    user = request.user
    pky=request.GET.get('room_id') 
    room= Chat_room.objects.get(id=pky)
    unreads = 0
    for message in room.messages.all():
        if request.user != message.sender:
            if user not in message.read_by.all():
                unreads += 1
    return HttpResponse(unreads)