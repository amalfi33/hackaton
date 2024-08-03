from .models import Friend, Message, Chat, GroupChat
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class GroupChatForm(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields = ['name', 'participants']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['friend']
