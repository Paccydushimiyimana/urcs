import re
import json
import datetime
import requests
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.contrib.auth import logout,login, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from twilio.rest import Client
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from twilio.rest import Client
from account.models import Category,MyUser,Sub_category,School,Department
from account.forms import LoginForm,ContactForm
from .models import Announce
from .forms import AnnounceForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from decouple import config

def home_view(request):
    announces = Announce.objects.filter(general=True)
    login_form = LoginForm()
    contact_form = ContactForm()
    pwd_form = PasswordChangeForm(request.user)
    _form = request.POST.get('form_name')
    if _form == 'login_form':
    # Loging in user
        login_form=LoginForm(request,request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data.get('username')
            password=login_form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'User {user} is logged in .')           
                return redirect('home')
        else:
            messages.warning(request, f'Invalid credentials!...Correct the errors on the form')           
    if _form == 'logout_form':
    # Logging out user
        user = request.user
        logout(request)
        messages.success(request, f'User {user} is logged out')
        return redirect('home')
    if _form == 'pwd_form':
    # Changing password  
        pwd_form = PasswordChangeForm(request.user, request.POST) 
        if pwd_form.is_valid():
            user = pwd_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Your password was . updated!')
            return redirect('change_password')
        else:
            messages.warning(request, f'Please correct the error on the form!...')
    context={'contact_form':contact_form,'login_form':login_form,'pwd_form':pwd_form,'announces':announces}
    return render(request,'index.html',context)

def modal_delete(request,pky):
    announce = get_object_or_404(Announce,pk=pky)
    context={'announce':announce}    
    return render(request,'modal_delete.html',context) 

@login_required
def inbox(request,user_name):
    create_form = AnnounceForm()
    pwd_form = PasswordChangeForm(request.user) 
    contact_form = ContactForm()
    user=request.user
    announcesall=Announce.objects.all().order_by('-id')
    announces=[]
    for announcet in announcesall:
        if announcet.general==False and user in announcet.receiver.all():
            announces.append(announcet)

    _form = request.POST.get('form_name')
    if _form == 'logout_form':
    # Logging out user
        user = request.user
        logout(request)
        messages.success(request, f'User {user} is logged out')
        return redirect('home')
    elif _form == 'pwd_form':        
    # Changing password  
        pwd_form = PasswordChangeForm(request.user, request.POST) 
        if pwd_form.is_valid():
            user = pwd_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Your password was . updated!')
            return redirect('change_password')
        else:
            messages.warning(request, f'Please correct the error on the form!...')
    elif _form == 'archive_form':
    # Hidding anct rows   
        annz = request.POST.getlist('announces')
        for ann in annz:
            announce = Announce.objects.get(id = ann)
            announce.archived_by.add(user)
            announce.save()
    context={'contact_form':contact_form,'page':'inbox','announces':announces,'pwd_form':pwd_form,'create_form':create_form}
    return render(request,'inbox.html',context)

@login_required
def board(request,user_name):
    create_form=AnnounceForm()
    pwd_form = PasswordChangeForm(request.user)   
    contact_form = ContactForm()
    user= request.user
    announces = Announce.objects.filter(sender=user.pk)
    categories= Category.objects.all()
    _form = request.POST.get('form_name') 
    if _form == 'logout_form':
    # Logging out user
        logout(request)
        messages.success(request, f'User {user} is logged out')
        return redirect('home') 
    elif _form == 'delete_form':
    # deleting an announcement
        _id = str(request.POST.get('announce_id'))
        announce = Announce.objects.get(id=_id)
        announce.delete()
        messages.success(request, f' Announce {announce} deleted .')
        return redirect('board',request.user)
    elif _form == 'pwd_form':        
    # Changing password  
        pwd_form = PasswordChangeForm(request.user, request.POST) 
        if pwd_form.is_valid():
            user = pwd_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Your password was . updated!')
            return redirect('change_password')
        else:
            messages.warning(request, f'Please correct the error on the form!...')
    elif _form == 'archive_form':
    # deleting multiple announcements 
        annz = request.POST.getlist('announces')
        for ann in annz:
            announce = Announce.objects.get(id = ann)
            announce.delete()
        messages.success(request, f' Announces {annz} deleted .')
        return redirect('board',request.user)    
    context={'page':'board','announces':announces,'name':user,'contact_form':contact_form,'pwd_form':pwd_form,'create_form':create_form,'categories':categories}
    return render(request,'board.html',context)

@login_required
def create_view(request,user_name):
    create_form =AnnounceForm()
    pwd_form = PasswordChangeForm(request.user)   
    contact_form = ContactForm()
    categories = Category.objects.all()
    _form = request.POST.get('form_name') 
    if _form == 'pwd_form':
    # Changing password  
        pwd_form = PasswordChangeForm(request.user, request.POST) 
        if pwd_form.is_valid():
            user = pwd_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Your password was . updated!')
            return redirect('change_password')
        else:
            messages.warning(request, f'Please correct the error on the form!...')
    elif _form == 'logout_form':
    # Logging out user
        user = request.user
        logout(request)
        messages.success(request, f'User {user} is logged out')
        return redirect('home') 
    elif _form == 'create_form':
    # creating an announce    
        create_form =AnnounceForm(request.POST, request.FILES )
        general=request.POST.get('genl')
        category=request.POST.get('Catgy')
        subcategory=request.POST.getlist('Sub_catgy')
        school=request.POST.getlist('Skl')
        department=request.POST.getlist('Depart')
        level=request.POST.getlist('Lv')
        user=request.user
        receivers=[]
        # print(category,std_sub_category,school,department,level)
        if create_form.is_valid():
            announce=create_form.save()
            announce.sender=user
            announce.save()
            if general:
                announce.general=True
                announce.save()
            else:
                if category == 'Student':
                    for sub in subcategory:
                        for skl in school:
                            for depart in department:
                                for lev in level:
                                    users=MyUser.objects.filter(category=Category.objects.get(name=category) , subcategory=Sub_category.objects.get(name=sub) , school=School.objects.get(name=skl) , department=Department.objects.get(name=depart) , level=lev)
                                    for user in users:
                                        receivers.append(user)

                elif category == 'Lecturer':
                    for sub in subcategory:
                        for skl in school:
                            for depart in department:
                                for lev in level:
                                    users=MyUser.objects.filter(category=Category.objects.get(name=category) , subcategory=Sub_category.objects.get(name=sub) , school=School.objects.get(name=skl) , department=Department.objects.get(name=depart) , level=lev)
                                    for user in users:
                                        receivers.append(user)
                                                        
                elif category == 'Department_council':
                    for sub in subcategory:
                        for skl in school:
                            for depart in department:
                                users=MyUser.objects.filter(category=Category.objects.get(name=category) , subcategory=Sub_category.objects.get(name=sub) , school=School.objects.get(name=skl) , department=Department.objects.get(name=depart))
                                for user in users:
                                    receivers.append(user)
                                    
                elif category == 'School_council':
                    for sub in subcategory:
                        for skl in school:
                            users=MyUser.objects.filter(category=Category.objects.get(name=category) , subcategory=Sub_category.objects.get(name=sub) , school=School.objects.get(name=skl))
                            for user in users:
                                receivers.append(user)
                                                            
                elif category == 'Academic council':
                    for sub in subcategory:
                        users=MyUser.objects.filter(category=Category.objects.get(name=category) , subcategory=Sub_category.objects.get(name=sub))
                        for user in users:
                            receivers.append(user)        

                elif category == 'College council':
                    for sub in subcategory:
                        users=MyUser.objects.filter(category=Category.objects.get(name=category) , subcategory=Sub_category.objects.get(name=sub))
                        for user in users:
                            receivers.append(user)  

                for receiver in receivers:
                # sending mails
                    if receiver.email:
                        pass
                        # mail_fx(request,receiver,announce)
                # sending sms
                    if receiver.phone:
                        pass
                        # sms_fx(request,receiver ,announce)
                    announce.receiver.add(receiver)
               
            # sending notification to websocket    
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'gossip',{
                        'type':'user_gossip',
                        'event':'New announce',
                        'id':announce.id,
                        }
                )

            # print(len(receivers),receivers)
            messages.success(request, f' Announce {announce} created .')
            return redirect('board',request.user)

    context={'create_form':create_form,'contact_form':contact_form,'categories':categories,'pwd_form':pwd_form}
    return render(request,'create.html',context)

@login_required
def edit_view(request,pky,user_name): 
    announce = Announce.objects.get(id=pky)
    pwd_form = PasswordChangeForm(request.user)  
    edit_form=AnnounceForm(instance=announce)
    contact_form = ContactForm()
    _form = request.POST.get('form_name') 
    if _form == 'edit_form':
    # Editing announcement
        edit_form=AnnounceForm(request.POST, request.FILES, instance=announce)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, f' Announce {announce} updated .')
            return redirect('board',request.user)
    if _form == 'pwd_form':
    # Changing password  
        pwd_form = PasswordChangeForm(request.user, request.POST) 
        if pwd_form.is_valid():
            user = pwd_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Your password was . updated!')
            return redirect('change_password')
        else:
            messages.warning(request, f'Please correct the error on the form!...')
    elif _form == 'logout_form':
    # Logging out user
        user = request.user
        logout(request)
        messages.success(request, f'User {user} is logged out')
        return redirect('home')         
    context={'contact_form':contact_form,'edit_form':edit_form,'pwd_form':pwd_form}    
    return render(request,'edit.html',context)   

@login_required
def view_announce(request,pky,_from):
    create_form=AnnounceForm()
    pwd_form = PasswordChangeForm(request.user)
    contact_form = ContactForm()
    user= request.user
    announce=get_object_or_404(Announce,pk=pky)
    if user not in announce.viewed_by.all() and user != announce.sender:
        announce.viewed_by.add(user)
    _form = request.POST.get('form_name') 
    if _form == 'edit_form':
    # editing an announcement
        _id = request.POST.get('announce_id')
        announce = Announce.objects.get(id=_id)
        form=AnnounceForm(request.POST, request.FILES, instance=announce)
        if form.is_valid():
            form.save()
            messages.success(request, f' Announce {announce} updated .')
            return redirect('board',request.user)
    elif _form == 'delete_form':
    # deleting an announcement
        _id = str(request.POST.get('announce_id'))
        announce = Announce.objects.get(id=_id)
        if request.method =='POST':
            announce.delete()
            messages.success(request, f' Announce {announce} deleted .')
            return redirect('board',request.user)
    elif _form == 'logout_form':
    # Logging out user
        user = request.user
        logout(request)
        messages.success(request, f'User {user} is logged out')
        return redirect('home')
    elif _form == 'pwd_form':        
    # Changing password  
        pwd_form = PasswordChangeForm(request.user, request.POST) 
        if pwd_form.is_valid():
            user = pwd_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Your password was . updated!')
            return redirect('change_password')
        else:
            messages.warning(request, f'Please correct the error on the form!...')
    context={'announce':announce,'user':user,'contact_form':contact_form,'pwd_form':pwd_form,'from':_from}
    return render(request,'view.html',context)
 
def zero(request):
    users=MyUser.objects.all()
    return render(request,'zero.html',{'users':users})    

def new_row_view(request):
    user = request.user
    _id = request.GET.get('_id')
    announce = Announce.objects.get(id=_id)
    # print(announce.receiver.all())
    # print(announce)
    if user in announce.receiver.all():
        return render(request,'new_row.html',context={'announce':announce})
    else:    
        return HttpResponse('No')
    
def view_general(request,pky):
    user = request.user
    announce=get_object_or_404(Announce,pk=pky)
    user_cur=str(user)
    if user_cur != 'AnonymousUser':
        if user not in announce.viewed_by.all() and user != announce.sender:
            announce.viewed_by.add(user)
    context={'announce':announce,'user':user}
    return render(request,'modal_general.html',context)
     
def archive_view(request):
    j_list=request.GET.get('rows')
    page=request.GET.get('page')
    liste = json.loads(j_list)
    announces = []
    for _id in liste:
        announces.append(Announce.objects.get(id=_id))
    context = {'announces':announces,'page':page}
    return render(request,'modal_checked.html',context)

def mail_fx(request,receiver,announce):
    context={'receiver':receiver,'announce':announce,'protocol':request.scheme,'domain':request.META['HTTP_HOST']}
    subject='New announcement'
    message=render_to_string('sms_mail.html',context)
    # Remove html tags and continuous whitespaces 
    plain_message = strip_tags(message)
    from_email= config('EMAIL_HOST_USER')
    to=[receiver.email]
    fail_silently=False
    send_mail(subject,plain_message,from_email,to,fail_silently)

def sms_fx(request,receiver,announce):
    context={'receiver':receiver,'announce':announce,'protocol':request.scheme,'domain':request.META['HTTP_HOST']}
    message = render_to_string('sms_mail.html',context)
    # Remove html tags and continuous whitespaces 
    msge = text_only = re.sub('[ \t]+', ' ', strip_tags(message))
    # Strip single spaces in the beginning of each line
    plain_message = msge.replace('\n ', '\n').strip()
   
    account_sid = 'AC0aaf8f36c3fbce2f8a9e4a84ede81dbd'
    auth_token = '946f746b66c571f73e3efa98176f9189'
    sender_id = '+16076006494'

    client = Client(account_sid,auth_token)
    sms = client.messages.create(body=plain_message,from_=sender_id,to='+25'+receiver.phone) 
   
# email with gmail
def sendmail(request):
    user=request.user
    ann=Announce.objects.last()
    context={'receiver':user,'announce':ann,'protocol':request.scheme,'domain':request.META['HTTP_HOST']}
    subject='My subject'
    message=render_to_string('sms_mail.html',context)
    plain_message = strip_tags(message)
    from_email= settings.EMAIL_HOST_USER
    to=['paccydev@gmail.com','paccydev@gmail.com']
    fail_silently=False
    send_mail(subject,plain_message,from_email,to,fail_silently)
    return render(request,'sms_mail.html',context)

# sms with twilio
def sendsms(request):
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    client = Client(account_sid,auth_token)
    message = client.messages.create(
        body='Using twilio in urcs project',
        from_=config('twilio_nbr'),
        to=['+250782644566','+250782644566']
    ) 
    return HttpResponse('Okay sent')

def script_view(request):
    announces=Announce.objects.filter(sender=request.user)
    for announce in announces:
        announce.sender=MyUser.objects.get(username='admin')   
        announce.save() 
    return HttpResponse('done!')