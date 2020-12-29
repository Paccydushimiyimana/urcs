from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import RegisterForm,UserUpdateForm
from .models import *

class MyUserAdmin(UserAdmin):
    add_form = RegisterForm
    form = UserUpdateForm
    model = MyUser
    list_display = ['username','email','first_name']

admin.site.register(MyUser,UserAdmin)
admin.site.register(College)
admin.site.register(School)
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Sub_category)  

