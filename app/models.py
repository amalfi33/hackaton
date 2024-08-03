from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE ,related_name='user_friend', verbose_name='Пользователь')
    friend = models.ForeignKey(User , on_delete=models.CASCADE, verbose_name='Друг', related_name='firend')

class Message(models)