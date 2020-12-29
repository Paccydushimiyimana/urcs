from django.urls import path
from django.conf.urls import url
from account import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('profile/<str:name>/',views.profile_view,name='profile'),
    
    path('load_category/',views.load_category, name='load_category'),
    path('load_departments/',views.load_departments, name='load_departments'),
    path('load_levels/',views.load_levels, name='load_levels'),

    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]