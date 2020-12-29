from django.urls import path
from . import views

urlpatterns = [
    path('unreads_anct/',views.unread_anct_view,name='unreads_anct'),
    path('unreads_chat/',views.unread_chat_view,name='unreads_chat'),
    ]