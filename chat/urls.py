
from django.urls import path
from .views import *

urlpatterns = [
    path('unreadz/',unread,name='unreadz'),
    path('del_chat/',del_chat_view,name='del_chat'),
    path('user_detail/',user_detail_view,name='user_detail'),    
    path('<str:user_name>/',chat_index_view, name='chat'),
    path('<int:room_pky>/pass_message/',passing_msg_view, name='passing_msg'),
    path('<int:room_pky>/passing_box/',passing_box_view,name='passing_box'),

]