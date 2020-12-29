from django import forms
from .models import Announce
# from django_markdown.widget import MarkdownWidget
# from django_markdown.fields import MarkdownFormField
# from martor.fields import MartorFormField
# from mdeditor.fields import MDTextFormField

class AnnounceForm(forms.ModelForm):
    class Meta:
        model = Announce
        fields = ['title','file','content']
                    
    def __init__(self, *args, **kwargs):
        super(AnnounceForm, self).__init__(*args, **kwargs)
        # self.fields['file'].label = " "
        # self.fields['password2'].label = "Password confirm"
        # self.fields['username'].help_text = " Letters, digits and @/./+/-/_ only."               
