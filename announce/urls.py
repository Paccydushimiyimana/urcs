from django.urls import path
from . import views

urlpatterns = [

    path('inbox/new_row/',views.new_row_view,name='new_row'),
    path('inbox/archive_rows/',views.archive_view,name='archive_rows'),
    path('inbox/<str:user_name>/',views.inbox,name='inbox'),

    path('board/<str:user_name>/',views.board,name='board'),
    path('board/new/<str:user_name>/',views.create_view,name='create'),
    path('board/<int:pky>/delete/',views.modal_delete,name='modal_delete_pass'),
    path('<str:_from>/<int:pky>/detail/',views.view_announce,name='view'),
    path('board/<int:pky>/edit/<str:user_name>/',views.edit_view,name='edit'),
]