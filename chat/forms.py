from django import forms
from .models import Chat_room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Chat_room
        fields = ['other']