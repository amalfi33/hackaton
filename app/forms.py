from .models import Friend, Message, Chat, GroupChat
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):   
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        fields = ['username','email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

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
