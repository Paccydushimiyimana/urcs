from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserChangeForm,UserCreationForm
from .models import MyUser,Category

class LoginForm(AuthenticationForm):
 
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)     
        self.fields['username'].label = "User ID"    

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    image = forms.ImageField(required=False)
    phone = forms.CharField(required=False)
            
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Password must contain at least 8 characters."
        self.fields['password2'].label = "Password confirm"
        self.fields['username'].help_text = " Letters and digits."      
        self.fields['username'].label = "User ID"         

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name','username','email','phone','password1', 'password2']

class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(required=False)
    image = forms.ImageField(required=False)
    phone = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = " Letters and digits."
        self.fields['username'].label = "User ID"
        self.fields['image'].label = ""

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name','username','email','phone','image']

class ContactForm(forms.Form):
    names=forms.CharField()
    email=forms.EmailField()
    message=forms.CharField(widget=forms.Textarea)