from django import forms
from .models import Announce

class AnnounceForm(forms.ModelForm):
    class Meta:
        model = Announce
        fields = ['title','file','content']
                    
    def __init__(self, *args, **kwargs):
        super(AnnounceForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = " "
        