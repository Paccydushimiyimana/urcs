
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from announce.views import *

urlpatterns = [
    path('script/', script_view,name='login'),
    path('sms/', sendsms,name='sendsms'),
    path('mail/',sendmail,name='sendmail'),

    path('', home_view,name='home'),
    path('<int:pky>/',view_general,name='view_general'),  
    path('zero/', zero,name='zero'),
    
    path('admin/', admin.site.urls), 
    path('announces/', include('announce.urls')),
    path('accounts/', include('account.urls')),
    path('chats/', include('chat.urls')),    
    path('notifier/',include('notifier.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)